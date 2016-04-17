# OfficeLunch
HackDFW 2016 Project

Office Lunch is a web application that based on input provides lunch options everyone is in the mood for and can enjoy. Leveraging AWS EC2 instances for the web server, application server, and DB server the team is able to serve the application in a stable environment that we configured and manage. 

### The Application: 

Main Functions: The User is part of a group, event, or creates a new group that he/she can manage. The user sets a group name, an origin location, and distance or time. Once a group is created & the user starts an event he/she can enter tags which the members of the group agree upon. These tags are sent to the back-end to query the Yelp API for restraunts that fall into the tags category, but also are within the set distance/origin location configured for the group. Once a list of restraunts is built the group members can all seperately vote for a restraunt of their choice. The gain of using our app is no matter which restraunt wins the selection will have food options for all members to enjoy and no one will feel left out(based on the tags they entered).

### What we used: 

Leveraging vanilla Javascript, Jquery, HTML5, and a CSS stylesheet that we modified to fit our needs we built the pages our web server(http://ec2-52-11-89-254.us-west-2.compute.amazonaws.com/) is serving. Leveraging AJAX from the web server to an application server() hosting a Flask python server the team can GET current user data allowing the app to provide accurate information from our stored DB data. 

### The Servers:

Using AWS's Linux build(Essentially a RHEL build) we configured apache for the web server and for the application server configured apache to point at a flask server instance running on the box. The team used Mongo for our DB service. 
