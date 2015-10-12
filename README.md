Tournament Results
==================

AUTHOR
------
Salman Awan

INTRODUCTION
------------
This repository contains the submission for Project 2 of the Udacity Full Stack Devleoper Nanodegree. This project contains code to implement the Swiss system for pairing up players in each round of a tournament. The player info and match results are stored in a relational database.

Your README does not include all the steps required to run the application. For example, it should include:

ENVIRONMENT
-----------
This project requires Virtual Box and Vagrant to be installed on your system.

SETTING UP THE VM
-----------------
The vagrant VM files are present in the folder: /vagrant. The following commands should be run on a command window to run the VM:

vagrant up (powers on the virtual machine)
vagrant ssh (logs into the virtual machine)

SETTING UP THE DATABASE
-----------------------
In folder /vagrant/tournament, run the psql command line interface and then run the following command:

vagrant=> \i tournament.sql

This will create the tournament database and all required tables and views.

RUNNING THE APPLICATION
-----------------------
In folder /vagrant/tournament, run the following command:

python tournament_test.py

This will run all the tests for the swiss pairing code.
