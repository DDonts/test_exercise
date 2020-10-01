# "To do list" REST application

## Installation
pip install -r requirements.txt

Set mysql URI and secret key in ".env" file

## Run
python app.py

## Usage
Before first request, two tables(users and cases) will be created in in a manually created database.

#### Registration
    URL: http://{{server_url}}/register
    METHOD: POST
    
    Headers:
        Content-Type: application/json
        Authorization: "Bearer {{access_token}}"
    Input: {
        "username": "preferred username"
        "password": "preferred password"
    }
    return: JSON of report message
    
#### Login in
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
    URL: http://{{server_url}}/logout
    METHOD: POST
    
    Headers:
        Authorization: "Bearer {{access_token}}"
    Input: {}
    
    return: JSON of report message

#### Refresh access token
    URL: http://{{server_url}}/refresh
    METHOD: POST
    
    Headers:
        Content-Type: application/json
        Authorization: "Bearer {{access_token}}"
    Input: {}
    
    return: JSON of a new access_token
   
#### Change password
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
    URL: http://{{server_url}}/case
    METHOD: GET
    
    Headers: Authorization: "Bearer {{access_token}}"
    Input: {
        "status": "new/planned/in_progress/completed"   (optional)
        "end_time": "Hour:Minutes Day.Month.Year"       (optional)
    }
    return: List of cases
 
#### Add new case
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






