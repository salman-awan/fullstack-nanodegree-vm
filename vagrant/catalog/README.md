Item Catalog
============

AUTHOR
------
Salman Awan


INTRODUCTION
------------
This folder contains the submission for Project 3 of the Udacity Full Stack Devleoper Nanodegree. This project contains code for an item catalog website which supports CRUD operations and OAuth authentication.


SETTING UP THE VM
-----------------
The source code for this project is on the GitHub repository: git@github.com:salman-awan/fullstack-nanodegree-vm.git

After cloning this GitHub repository, the vagrant VM files are present in the folder: /vagrant. The following commands should be run on a command window to run the VM:

vagrant up (powers on the virtual machine)
vagrant ssh (opens a secure terminal to the virtual machine)


REQUIREMENTS
-------------
You will need to install Python 2.7.x and Pip 1.5.x (Python package manager) on your VM to run this project.

Other than the modules that are already available with Python 2.7.x, the following additional modules are required:

Flask == 0.10.1
SQLAlchemy == 0.8.4
oauth2client == 1.5.1
requests == 2.2.1
httplib2 == 0.9.2

NOTE: The required modules are listed in the file '/vagrant/catalog/requirements.txt'. You can run the following single command to install them all:

pip install -r requirements.txt


SETTING UP THE DATABASE
-----------------------
In folder /vagrant/catalog, run the following command:

python populate_db.py

This will create the item catalog SqlLite database in the file catalog.db and populate it with sample items


RUNNING THE APPLICATION
-----------------------
In folder /vagrant/catalog, run the following command:

python application.py

This will start the website which can be accessed with this URL: http://localhost:5000


USAGE
-----
You can use the links in the main catalog page to view the categories and items within those categories.

Only logged in users can add items, and then edit or delete the items they have added.

This project uses Google sign in for authentication. After clicking the Login link, you will need to use your Google account to log in and allow access for this application.

Once logged in, the relevant web pages will allow you to add new items and later edit or delete those items.
