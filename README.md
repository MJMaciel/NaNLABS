# NaNLABS

* In order to use this app with your trello account you need to replace the TOKEN, KEY and BOARD_NAME
* in the functions.py file inside the tasks folder.
Now is filled with my credentials and the name of the board 'spaceX' that's the one I have been using
to test the endpoints.


* To run the application go to the main folder and execute the next commands:
python manage.py migrate
python manage.py runserver 3000


* After running the app you can use the endpoint to create the 3 types of tasks:
http://localhost:3000/


* You can also use the django rest_framework frontend accessing the url in a chrome tab.