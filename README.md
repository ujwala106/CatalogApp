# Countries and TouristPlaces Catalog
* This is simple Catalog App which shows the details of countries and the tourist Places in each country.
* If an authenticated user is logged in, The authentication is done from google's oauth client. and an access token    is generated.
* If the user is authenticated, he can add, edit and delete the places which the user has added.
* If the user is not not authenticated, He is not allowed to add, edit or delete the places.


## Prerequisites
* Python
* psql 
* Vagrant
* VirtualBox

## System Setup
This project makes use of Udacity's Linux-based virtual machine (VM) configuration which includes all of the necessary software to run the application.<br>
The configuration of the VM comes along with python, psql, and other neccesary packages related to the working of the project.

#### Download VirtualBox and install<br>
VirtualBox is the software that actually runs the virtual machine.<br>
You can download it from [here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)   

#### Download Vagrant and install<br>
Vagrant is the software that configures the VM and lets you share files between host and the VM's filesystem.<br>
You can downlaod it from [here](https://www.vagrantup.com/downloads.html)

#### Download the VM configuration<br>
you can use Github to fork and clone [this](https://github.com/udacity/fullstack-nanodegree-vm) repository.<br>
Change your directory to this repository and do ***cd vagrant***<br>

#### Start the virtual machine<br>
From your terminal, inside the vagrant subdirectory, run the command ***vagrant up***<br>
This will cause Vagrant to download the Linux operating system and install it.<br>
When vagrant up is finished running, you will get your shell prompt back.<br>
At this point, you can run ***vagrant ssh*** to log in to your newly installed Linux VM!


### How to Run this application
1. Clone this repository
2. place the project folder folder in your /vagrant directory.
3. The project needs to be kept in /vagrant folder because this folder can be shared between host machine and VM. So, the changes made to the project from the host machine can be reflected in vm and can be dynamically seen from browser of Host machine.
4. Launch Vagrant
```
$ Vagrant up 
```
4. Login to Vagrant
```
$ Vagrant ssh
```
5. Change directory to `/vagrant`
```
$ Cd /vagrant
```
6. Initialize the database
```
$ Python database_setup.py
```
7. Populate the database with some initial data
```
$ Python data.py
```
9. Launch application

* The application of consists of database_setup.py file to create database with required tables and specified column names and constraints.
* It also consists of data.py file to populate the database with the sample data to be populated to the tables.
* It consists project.py file that consists of code related to google login and app functionality
* The templates folder consists of the html templates to be rendered.
* clients_secrets.json file consists of the client secret for google authentication.

```
$ Python project.py
```
10. Open the browser and go to http://localhost:8000

### JSON endpoints
#### Returns JSON of all country

```
/catalog.json
```
#### Returns JSON of specific country

```
/catalog/country<int:country_id>/json
```
#### Returns JSON of specific places in a country

```
/catalog/country<int:country_id>/palces<int:places_id>/json
```
