# Skatertron 9000 #
**An organization system for high volume media storage aimed at the USFS and Entryeeze standards of skate order sheets**

## Table of contents
* [Introduction](#introduction)
* [Technologies](#technologies)
* [Setup](#setup)
* [Launch](#launch)

## Introduction
The aim of this project is to help my client, a high volume sports media company, to store their footage in a digital format. Of primary concern is ease of use for non-techinal end-users, persistance and reliability of data extraction, speed of use, and the ability to integrate into a larger software ecosystem in planning. The project is currently in a pre-alpha state and is limited to a console based interface that will be used to debug and create user logs in the future.

## Technologies
This project makes use of the following languages and packages:
* Python version: 3.10.2
    * ~SQLite version: 3.35.5~
    * psycopg2 version: 2.9.8 
    * SQLAlchemy version: 2.0.21 
    * Tkinter version: 8.6
    * pdfminer.six version: 20221105
    * Hypothesis version: 6.87.0
    * Unidecode version: 1.3.7

## Setup
To setup this repository, install the specified version of Python, launch your command line and change your directory to the repository root and run:
```
$ python3.10 -m venv /path/to/new/virtual/environment
$ source <venv>/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
```


## Launch
To run this project please execute the *../skaterton/controller.py* module. In order to make use of the full functionality the user must have access to USFS or EntryEeze formatted skate order sheets in PDF format. None are included in this repository for the purposes of maintaining the privacy of competitors. In future releases I will include an edited bank of PDF documents with redacted indentifying information so that the full functionality of this program can be explored.


## Up Next
* Fully migrate database to postgresql
* Rearrange project architecture
    * Make a __main__.py
    * Break out controller into several controller modules inside a "~/skatertron/Skatertron/controllers" directory
    * Break out models into several services modules inside a "~/skatertron/Skatertron/services" directory
    * Move pdf_scraper to a "~/skatertron/Skatertron/utilities" directory
* Expand UI
    * Add Desktop App UI
        * PyQT/TKInter?
    * Add webapp UI
        * Create "~/skatertron/Skatertron/views" or "~/skatertron/Skatertron/UI" directory
            * Elements
            * Events
            * etc...