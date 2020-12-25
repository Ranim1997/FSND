
# Casting Agency
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

## Motivation
This is a Casting Agency Capstone Project for Udacity Full Stack Web Developer Nanodegree Program.

This project covers: Data modeling using `postgres`, API development and testing using `Flask`, Authentication using `Auth0`, Authorization with `Role-Based Access Control`, and API deployment using `Heroku`.

## Live API

This app uses Auth0 as Authentication provider. JWTs for different role can be accessed by login to the link with the credential provided below https://ranim1997.us.auth0.com/authorize?audience=castingagency&response_type=token&client_id=2FzDxkRIbdMZ1z5YXwsNX0ER3DlnMb1s&redirect_uri=https://127.0.0.1:5000/actors

- Casting Assistant:
    - User: `casting_assistant@test.com`
    - Password: `Test@1234`
- Casting Director:
    - User: `casting_director@test.com`
    - Password: `Test@1234`
- Executive Producer
    - User: `executive_producer@test.com`
    - Password: `Test@1234`

Test the endpoints with the following link: [https://fsndcastingagencyapp.herokuapp.com](https://fsndcastingagencyapp.herokuapp.com)

## API Endpoints
This application contains the following endpoints:
- Actors
	-  `GET /actors`
	-  `POST /actors`
	-  `PATCH /actors/int:id`
	-   `DELETE /actors/int:id`
- Movies
	-   `GET /movies`
	-   `POST /movies`
	-   `PATCH /movies/int:id`
	-   `DELETE /movies/int:id`

## Permissions
Role-Based Access Control was applied in this project. Thus, there are three type of users: 
- Casting Assistant can:
	-   `GET /actors`
	-   `GET /movies`

-  Casting Director can:
	-   `GET /actors`
	-   `GET /movies`
	-   `POST /actors`
	-   `PATCH /actors/int:id`
	-   `PATCH /movies/int:id`
	-   `DELETE /actors/int:id`
	
- Executive Producer can:
	-   `GET /actors`
	-   `GET /movies`
	-   `POST /actors`
	- 	`POST /movies`
	-   `PATCH /actors/int:id`
	-   `PATCH /movies/int:id`
	- 	`DELETE /actors/int:id`
	- 	`DELETE /movies/int:id`


## API Endpoints Documentation
First you need to set TOKEN value to the `access_token` value in the URL that appear after login. 

#### GET /actors
- Return a list of all actors with details
- Curl -i -X GET -H "Authorization: Bearer ${TOKEN}" https://fsndcastingagencyapp.herokuapp.com/actors
- Response:
```
{"Actors": [
			{
			"age":23,
			"id":2,
			"name":"mohammed"
			}
], "success":true }
```

#### GET /movies
- Return a list of all movies 
- Curl -i -X GET -H "Authorization: Bearer ${TOKEN}" https://fsndcastingagencyapp.herokuapp.com/movies
- Response:
```
{
"Movies": [{
		"id":2,
		"releas date":"Wed, 21 Nov 2018 04:05:06 GMT",
		"title":"excellent life"}],
"success": true
}
```

#### POST /actors
- Insert a new actor
- Curl -i -X POST -H "Authorization: Bearer ${TOKEN}" -H "Content-Type:application/json" -d "{\"name\":\"john\",\"age\":"20",\"gender\":\"male\"}" https://fsndcastingagencyapp.herokuapp.com/actors
- Response:
```
{
"actor": [
	{
	"actor":"john",
	}
], "success": true}
```

#### POST /movies

- Insert a new Movie
- Curl -i -X POST -H "Authorization: Bearer ${TOKEN}"  -H "Content-Type:application/json" -d "{\"title\":\"Travel\", \"release_date\": \"2018-11-21\"}" https://fsndcastingagencyapp.herokuapp.com/movies
- Response:
```
{"movies":"Travel","success":true}
```

#### PATCH /actors/int:id

- Update an existing actor's details
-  Curl -i -X PATCH -H "Authorization: Bearer ${TOKEN}"  -H "Content-Type:application/json" -d "{\"age\":23}"  https://fsndcastingagencyapp.herokuapp.com/actors/2
- Response:

```
{"actors":"mohammed","success":true}
```

#### PATCH /movies/int:id

- Update an existing movie details
-  Curl -i -X PATCH -H "Authorization: Bearer ${TOKEN}"  -H "Content-Type:application/json" -d "{\"title\":\"Travel, gratitude\"}"  https://fsndcastingagencyapp.herokuapp.com/movies/2
- Response:
```
{"movie":"Travel, gratitude","success":true}
```


#### DELETE /actors/int:id

- Delete an existing actor
- Curl -i -X DELETE -H "Authorization: Bearer ${TOKEN}" https://fsndcastingagencyapp.herokuapp.com/actors/6  
- Response:
```
{"delete":"6","success":true}
```

#### DELETE /movies/int:id

- Delete an existing movie
- Curl -i -X DELETE -H "Authorization: Bearer ${TOKEN}" https://fsndcastingagencyapp.herokuapp.com/movies/5 
- Response:
```
{"delete":"5","success":true}
```

## Dependencies to Run Locally

### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight SQLite database.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. 

#### Python
Install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Environment
This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies:
`pip install -r requirements.txt`
This will install all of the required packages we selected within the `requirements.txt` file.

### Running the server
Each time you open a new terminal session, run: `FLASK_APP=app.py`
To run the server, execute:`flask run --reload`

The `--reload` flag will detect file changes and restart the server automatically.

## Reference
https://auth0.com/docs/quickstart/backend/python/01-authorization 