API for Backlog Fighter:

Note that these are all very rough ideas that are subject to change.

Goals:
* Have a locally created databasae that is lightweight and efficient
* A table for all backlog items, as well as a table for backlog item types
* * This way we have a many to one ratio to help sort out which table each backlog belongs to while avoiding creating multiple tables(?)
* Additional information as needed
* For common types, give option on a way to access them:
* * For things like games, have a path to the .exe
* * Anime/Manga could be a local path to the file itself or a web url
* Have something that will randmonly pull an entry from the backlog
* Have backlog priorities that will affect what randmonly gets pulled
* Have a difficulty associated with each backlog item
* Have a completed backlog(?) May take up space

But before I do any of that, need to learn flask :'^)

Dependencies:
Python 3.8, and flask installed.
I recommend installing flask onto a venv (many guides exist online, typically I just do python3 -m venv venv, then . venv/bin/activate)

How to work on:
Note these instructions are for linux only
To start the api server:
* Type into terminal: export FLASK_APP=flaskr
* Then: flask run

To start the front end website:
* cd client
* npm run serve


TODO:
* Properly take input on Page.vue
* Document the current routes/api and what they do
