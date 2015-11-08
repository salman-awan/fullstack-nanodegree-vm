Item Catalog
============

AUTHOR
------
Salman Awan

INTRODUCTION
------------
This folder contains the submission for Project 3 of the Udacity Full Stack Devleoper Nanodegree. This project contains code for an item catalog website which supports CRUD operations and OAuth authentication.

ENVIRONMENT
-----------
This project requires Virtual Box and Vagrant to be installed on your system. Please run the vagrant VM (vagrant up) and then open an SSH terminal to the VM (vagrant ssh).

SETTING UP THE DATABASE
-----------------------
In folder /vagrant/catalog, run the following command:

python populate_db.py

This will create the item catalog SqlLite database in the file catalog.db

RUNNING THE APPLICATION
-----------------------
In folder /vagrant/catalog, run the following command:

python application.py

This will start the website which can be accessed with this URL: http://localhost:5000
