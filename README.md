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
    * alembic version: 1.13.1 
    * pydantic version: 2.5.3 
    * fastapi version: 0.109.1 
    * uvicorn version: 0.26.0

## Setup
To setup this repository, install the specified version of Python, launch your command line and change your directory to the repository root and run:
```
$ python3.10 -m venv /path/to/new/virtual/environment
$ source <venv>/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
```


## Launch
To run this project please run the following command in your terminal from the *./Skatertron* directory: 
```
 uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
In order to make use of the full functionality the user must have access to USFS or EntryEeze formatted skate order 
sheets in PDF format. None are included in this repository for the purposes of maintaining the privacy of competitors. 
In future releases I will include an edited bank of PDF documents with redacted identifying information so that the 
full functionality of this program can be explored.


## Up Next
* Add validation to the */files/* POST endpoint to only accept valid video and photo files
* Change the data model for files to include a column for filepath and a column for filetype (video/photo)
* Add an hx-get request to use the *media_player.html* element as a preview for the selected video/photo
* Add a data model for orders
* Add front end functionality to add files to an order object
* Add back end functionality to upload the files in an order 
* Make the CSS positioning grid based
* Rename file data model to something clearer
