from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Country, TouristPlaces, Users

# Create database and create a shortcut for easier to update database
engine = create_engine('sqlite:///country_catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Creating an user
user_1 = Users(name="admin", email="admin@admin.com")
session.add(user_1)
session.commit()

# India
country_1 = Country(user_id=1, name="India")
session.add(country_1)
session.commit()


# Australia
country_2 = Country(user_id=1, name="Australia")
session.add(country_2)
session.commit()

# England
country_3 = Country(user_id=1, name="England")
session.add(country_3)
session.commit()

# Paris
country_4 = Country(user_id=1, name="Paris")
session.add(country_4)
session.commit()

# USA
country_5 = Country(user_id=1, name="USA")
session.add(country_5)
session.commit()

# Mexico
country_6 = Country(user_id=1, name="Mexico")
session.add(country_6)
session.commit()

# SriLanka
country_7 = Country(user_id=1, name="Srilanka")
session.add(country_7)
session.commit()

# MAldives
country_8 = Country(user_id=1, name="Maldives")
session.add(country_8)
session.commit()

# Adding touristAttractions to Countries
places = TouristPlaces(user_id=1, name="Taj Mahal",
                      description="Taj Mahal is mausolem by Mughal ruler Shah Jahan for his Wife Mumtaz Mahal "
                      "It is bultby using white marbel",
                      country=country_1)
session.add(places)
session.commit()

places = TouristPlaces(user_id=1, name="Red Fort",
                 description="Red fort is the histroric fort in the city of Delhi,India."
                 "It is the main residence of the emperors of mughal Dynasty.",
                 country=country_1)
session.add(places)
session.commit()

places = TouristPlaces(user_id=1, name="Canberra",
                 description="It is the home for National GAllery of Australia"
                 "and a wide varierty of cultural and historic sites",
                 country=country_2)
session.add(places)
session.commit()

places = TouristPlaces(user_id=1, name="Perth",
                 description="The west side ofAustralia is home to the city of Perth"
                 "It is bordered by Indian Ocean",
                 country=country_2)
session.add(places)
session.commit()

places = TouristPlaces(user_id=1, name="Tower Of London",
                 description="It is one of the world Heritage site"
                 "Other highlights are Crown Jewels Exhibition",
                 country=country_3)
session.add(places)
session.commit()

places = TouristPlaces(user_id=1, name="British Museum",
                 description="It contains the collection of worlds finest antiquites"
                 "The famous artifacts are Eglin marbles",
                 country=country_3)
session.add(places)
session.commit()

places = TouristPlaces(user_id=1, name="Eiffel Tower",
                 description="The Eiffel-tower is wrought iron lattice"
                 "It is named after the Engineer Gustav Eiffel",
                 country=country_4)
session.add(places)
session.commit()

places = TouristPlaces(user_id=1, name="places of Versallies",
                 description="The Palce of Versallies is the Principle Royal"
                 "residence.",
                 country=country_4)
session.add(places)
session.commit()

places = TouristPlaces(user_id=1, name="Grand Canyon Village",
                 description="Grand Canyon is located in south Rim of Grand Canyon"
                 "It is focussed on accomadating tourists visiting Grand Canyon",
                 country=country_5)
session.add(places)
session.commit()

places = TouristPlaces(user_id=1, name="Statue if Liberty",
                 description="Statue of Liberty is Colossal neo-classical sculpture"
                "In New-york Hourbor Newyork",
                 country=country_5)
session.add(places)
session.commit()

places = TouristPlaces(user_id=1, name="Mexico City",
                 description="Mexico city is densely populated and high altitude capital Of Mexico"
                 "It is the home for zoo,Muesuem of modern Art.",
                 country=country_6)
session.add(places)
session.commit()

places = TouristPlaces(user_id=1, name="Tulum",
                 description="Tulum is a town in the Carribean coatline of Mexico"
                 "It is well-known for beaches and ruins of Ancient Mayan port city",
                 country=country_6)
session.add(places)
session.commit()

places = TouristPlaces(user_id=1, name="Colombo",
                 description="It is the Capital city of Srilanka"
                 "It sheritage is reflected in its Architecture",
                 country=country_7)
session.add(places)
session.commit()

places = TouristPlaces(user_id=1, name="Kandy",
                 description="Kandy is the largest city of central Sri Lanka."
                 "It is surrounded by mountains which is home to tea Plantations.",
                 country=country_7)
session.add(places)
session.commit()

places = TouristPlaces(user_id=1, name="Male",
                 description="It is among the tooped tourist Attractions of Maldives"
                 "It has considerably moderate tempaerature through out the year",
                 country=country_8)
session.add(places)
session.commit()

places = TouristPlaces(user_id=1, name="Sun Island",
                 description="It is adorned with some sparkling beaches"
                 "beuatigul flowers and lavish greenary that pulls a great number of tourists",
                 country=country_8)
session.add(places)
session.commit()

print("added countries and Tourist Places added")
