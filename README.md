# API Development and Documentation Final Project

## Full Stack Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. 

## Getting Started

This project uses **React** and **Node** for the frontend and **Flask**, **SQLAlchemy**, **PostgreSQl** and **Flask-CORS** for the backend. To be able to run this program on your local machine you need to install all aforementioned packages must be installed.


### Backend

#### Installation guide
- Install the latest python on your machine through the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
- Create a virtual environment for your project, you can figure out how to create a virtual environment for your platform in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
- Install the required dependencies by navigating to the `/backend` directory and running: ```bash pip install -r requirements.txt ```

#### Setting up the Database
- Install Postgres on your machine through the [postgres docs](https://www.postgresql.org/docs/current/tutorial-start.html)
- Create a `trivia` database: ```bash createdb trivia```, populate your database with the `trivia.psql` file provided in the `backend` folder in terminal: ```bash psql trivia < trivia.psql```

#### Run the Server
- From within the `./src` directory first ensure you are working using your created virtual environment.
- To run the server, execute: 
```
    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run
```
Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically. Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

#### Testing
- Create a test database: ```bash createdb trivia_test```
- Populate the test database with the `trivia_test.psql` file provided in the `backend` folder in terminal: ```bash psql trivia_test < trivia_test.psql```
- Run the tests: ```bash python test_flaskr.py```



### Frontend

#### Installation guide
- This project uses Node and Node Package Manager (npm) to install the necessary dependencies. You must install Node to continue (including NPM) from the [node docs](https://nodejs.org/en/download/).
- Install the necessary dependencies by navigating to the `/frontend` directory and running: ```bash npm install```

#### Run the frontend server
- From within the `./frontend` directory run the command: ```bash npm start```
- After the server has started, you can navigate to the `http://localhost:3000` URL in your browser.

## API Reference

[View the README.md in the backend folder for the API documentation](./backend/README.md)

## Author

- Chima Onumaegbu

## Acknowledgement

- The entire Udacity team!