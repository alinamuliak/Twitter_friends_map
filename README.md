# twitter_project

In this task is realized a module that develop a web-application with which you can display on the map data about friends (people you are subscribed to) of the specified account on Twitter.


The web application is also deployed on the service https://www.pythonanywhere.com by the link:

## http://alinamuliak.pythonanywhere.com/


When the program start or when the user open the page on http://alinamuliak.pythonanywhere.com/ it is offered to user to enter a certain Twitter username and bearer token. If there are some problems with the input, user will see a message that informs him about the problem.

    Otherwise, by using

1. requests module - to get the information from Twitter
2. json module - to convert the needed data about user's friends, theirs nicknames and location for comfortable use;
3. geopy module - to find the coordinates of the certain place;
4. folium module - to built a map;
5. and flask - to realize GET and POST requests which make it easier for user to navigate through the application;

    map will be generated and displayed to user.

Markers on the map also contain the name of the friends whose location it is.

## With this application it is easy for user to check his/her friends' location and see it on the map.
