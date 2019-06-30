#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash, g
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from database_setup import Base, TouristPlaces,Country, Users
from flask import session as login_session
from functools import wraps
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Country & TouristPlaces"

engine = create_engine('sqlite:///country_catalog.db')
Base.metadata.bind = engine

# Creating anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        # Upgrading the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # validating the access token
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for the given application.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already \
            connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Storing this access token in the session
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Getting user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h2>Hello, '
    output += login_session['username']
    output += '!!</h2>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 200px; height: 200px;border-radius: \
    150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


def createUser(login_session):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    new_user = Users(name=login_session['username'], email=login_session[
        'email'])
    session.add(new_user)
    session.commit()
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    user = session.query(Users).filter_by(id=user_id).one()
    return user


def getUserID(email):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except NoResultFound:
        return None

# DISCONNECT
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(
            json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # If the given token was invalid notice the user.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON API
@app.route('/catalog.json')
def catalogJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    countrylist = session.query(Country).all()
    return jsonify(countrylist=[r.serialize for r in countrylist])


@app.route('/catalog/country<int:country_id>/json')
def categoryJSON(country_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    country = session.query(Country).filter_by(id=country_id).one()
    places = session.query(TouristPlaces).filter_by(country_id=country.id)
    return jsonify(Places=[i.serialize for i in places])


@app.route('/catalog/country<int:country_id>/places<int:places_id>/json')
def itemJSON(country_id, places_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    places = session.query(TouristPlaces).filter_by(id=places_id).one()
    return jsonify(placesDetails=[places.serialize])


# Login Required function
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized access")
            return redirect('/login')
    return decorated_function


# Home Page
@app.route('/')
@app.route('/catalog')
def showCatalog():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    country = session.query(Country).all()
    places = session.query(TouristPlaces).order_by(
        TouristPlaces.id.desc()).limit(10)
    if 'username' not in login_session:
        return render_template('public_catalog.html', country=country,
                               places=places)
    else:
        return render_template('catalog.html', country=country,
                               places=places)


# Adding new places
@app.route('/catalog/new', methods=['GET', 'POST'])
@login_required
def newPlace():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        newPlaces = TouristPlaces(name=request.form['name'],
                             description=request.form['description'],
                             country_id=request.form['country_id'],
                             user_id=login_session['user_id'])
        session.add(newPlaces)
        session.commit()
        flash("New places Added!")
        return redirect(url_for('showCatalog'))
    else:
        return render_template('new_place.html')


# show the places in respective country
@app.route('/catalog/<int:country_id>')
def showCountry(country_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    totalCountry = session.query(Country).all()
    country = session.query(Country).filter_by(id=country_id).one()
    places = session.query(TouristPlaces).filter_by(country_id=country.id)
    return render_template('country.html', country=country, places=places,
                           totalcountry=totalCountry)


# Show the places details
@app.route('/catalog/<int:country_id>/<int:places_id>')
def showPlaces(country_id, places_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    country = session.query(Country).filter_by(id=country_id).one()
    places = session.query(TouristPlaces).filter_by(id=places_id).one()
    if 'username' not in login_session or \
            places.user_id != login_session['user_id']:
        return render_template('public_places.html', country=country,
                               places=places)
    else:
        return render_template('places.html', country=country, places=places)


# Edit places
@app.route('/catalog/<int:country_id>/<int:places_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editplaces(country_id, places_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editedplaces = session.query(TouristPlaces).filter_by(id=places_id).one()
    if editedplaces.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized"\
            "to edit this places. Please add your places in order to edit.');"\
            "window.location = '/';}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name'] == "":
            editedplaces.name = editedplaces.name
        else:
            editedplaces.name = request.form['name']

        if request.form['description'] == "":
            editedplaces.description = editedplaces.description
        else:
            editedplaces.description = request.form['description']

        if request.form['country_id'] == "":
            editedplaces.country_id = editedplaces.country_id
        else:
            editedplaces.country_id = request.form['country_id']

        session.add(editedplaces)
        session.commit()
        flash("places edited successfully!")
        return redirect(url_for('showPlaces', country_id=country_id,
                                places_id=places_id))
    else:
        return render_template('edit_places.html', country_id=country_id,
                               places_id=places_id, places=editedplaces)


# Delete the places
@app.route('/catalog/<int:country_id>/<int:places_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteplaces(country_id, places_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    placesToDelete = session.query(TouristPlaces).filter_by(id=places_id).one()
    if placesToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized "\
         "to delete this places. Please add your places in order to delete"\
         " .');window.location = '/';}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(placesToDelete)
        session.commit()
        flash("places deleted successfully!")
        return redirect(url_for('showCountry', country_id=country_id))
    else:
        return render_template('delete_places.html', country_id=country_id,
                               places_id=places_id, places=placesToDelete)


# logout
@app.route('/disconnect')
def disconnect():
    if 'username' in login_session:
        gdisconnect()
        flash("You have been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
