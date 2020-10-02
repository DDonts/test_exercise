# "To do list" REST application

## Installation
pip install -r requirements.txt

Set mysql URI and secret key in ".env" file

## Run
python app.py

## Usage

Before first request, three tables(users, cases and statuses) will be created in in a manually created database.

"users" table contains user's usernames, encrypted passwords and ids of cases.

"cases" table contains information about user's cases like name, description, start and end datetime, id of status.

"statuses" table initializes on first request to API and contains 4 statuses of cases: New, Planned, In progress and Completed.  


"REST TEST.postman_environment.json" file for PostMan contains all necessary environment variables to test API. 
"REST TEST.postman_collection.json" file for PostMan contains all requests to test API. 

"Login" and "Refresh token" requests contains tests that automatically sets access_token and refresh_token as environment variables of PostMan.

#### Registration
Creates a new user in application.

    URL: http://{{server_url}}/register
    METHOD: POST
    
    Headers:
        Content-Type: application/json
    Input: {
        "username": "preferred username"
        "password": "preferred password"
    }
    return: JSON of report message
    
    
#### Login in
Logging user in. Create a access_token and refresh_token for access to api.

Also recreate access_token and refresh_token if it expired.
    
    URL: http://{{server_url}}/login
    METHOD: POST
    
    Headers:
        Content-Type: application/json
    Input: {
        "username": "max length 80",
        "password": "max length 80"
    }
    return: JSON of fully fresh "access-" and "refresh-" tokens
    
 
#### Log out  
Logging user out by access_token of user. Appending his access_token to blacklist.

    URL: http://{{server_url}}/logout
    METHOD: POST
    
    Headers:
        Authorization: "Bearer {{access_token}}"
    Input: {}
    
    return: JSON of report message
    

#### Refresh access token
Refreshing expired access_token by refresh_token of user.
 
    URL: http://{{server_url}}/refresh
    METHOD: POST
    
    Headers:
        Content-Type: application/json
        Authorization: "Bearer {{refresh_token}}"
    Input: {}
    
    return: JSON of a new access_token
    
   
#### Change password
Changing user's password by access_token of user.

    URL: http://{{server_url}}/change_password
    METHOD: POST
    
    Headers:
        Content-Type: application/json
        Authorization: "Bearer {{access_token}}"
    Input: {
        "username": "username of a current user",
        "new_password": "new required password"
    }
    
    return: JSON of a new access_token
    

#### Get cases by optional condition
Getting list of user's cases by access_token of user. Also you can provide optional fields(status or end_time) to filter by them.

    URL: http://{{server_url}}/case
    METHOD: GET
    
    Headers: Authorization: "Bearer {{access_token}}"
    Input: {
        "status": "new/planned/in_progress/completed"   (optional)
        "end_time": "Hour:Minutes Day.Month.Year"       (optional)
    }
    return: List of cases
 
#### Add new case
Creating a new case by access_token of user.

You have to provide access_token in Authorization header, name, description and end_time of case.


        URL: http://{{server_url}}/case
        METHOD: POST
        
        Headers:
            Content-Type: application/json
            Authorization: "Bearer {{access_token}}"
        
        Input: {
            "name": "name of the required case",
            "description": "some description"
            "end_time": "Hour:Minutes Day.Month.Year",
        }
    return: JSON of created case.

#### Delete case
Deleting case by name and access_token of user.

    URL: http://{{server_url}}/case
    METHOD: DELETE
    
    Headers:
        Content-Type: application/json
        Authorization: "Bearer {{access_token}}"
    
    Input: {
        "name": "name of the required case"
    }
    return: JSON of report message
    
#### Update case
Update case by name and access_token of user. Yor can provide optional fields (new_name, new_description, status and end_time)

    URL: http://{{server_url}}/case
    METHOD: PUT
    
    Headers:
        Content-Type: application/json
        Authorization: "Bearer {{access_token}}"
    
    Input: {
        "name": "name of the required case",
        "new_name": "new name of the case"               (optional)
        "new_description": "some new some description"   (optional)
        "status": "new/planned/in_progress/completed",   (optional)
        "end_time": "Hour:Minutes Day.Month.Year",       (optional)
    }
    return: JSON of edited case

#### Getting case history
Getting case history/logs by name of case and access_token of user.

    URL: http://{{server_url}}/case_history
    METHOD: POST

    Headers:
        Content-Type: application/json
        Authorization: "Bearer {{access_token}}"

    Input: {
        "name": "name of the required case"
    }
    return: JSON of history of case.

