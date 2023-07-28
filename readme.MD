# Backend Credit Card

This is a CRUD API for credit cards with 95% of coverage tests. Some business rules have been applied:

- **exp_date**<br>
  -- Check if it is a valid date.<br>
  -- If valid, it cannot be less than "today's" date.<br>
  -- In the database, this date should be recorded in the format yyyy-MM-[last_day_of_month], for example: 02/2022, should be 2022-02-28
- **holder**<br>
  -- It should be a required field and must have more than 2 characters.
- **number**<br>
  -- Check if the credit card number is valid, using the lib [https://github.com/MaisTodos/python-creditcard](https://github.com/MaisTodos/python-creditcard)<br>
  -- To install, use `pip install git+https://github.com/maistodos/python-creditcard.git@main`<br>
  -- This field should be stored in an encrypted way in the database.
- **cvv**<br>
  -- This field is not required, but if present in the payload, it must have a length between 3 and 4 characters.<br>
  -- This is a numeric field.

## Fast way to test the application

1.  `git clone https://github.com/devmeurer/backend-python-creditcard`
2.  `cd backend-python-creditcard`
3.  Rename the `".env-example"` file to `".env"`
4.  With make, build/run application and the unit/integration tests with: `make test`. You gonna see the tests results and coverage report.
5.  Now you can access [http://localhost:8000/docs](http://localhost:8000/docs) to test endpoints manually.
6.  Click on /login endpoint
7.  Click on "Try it out"
8.  Insert username(username) and password(password) and click on execute.
9.  You gonna receive a access_token: copy it.
10. On top of page, on right side, click on "Authorize" and paste the token there, finally click in Authorize.
11. Now you can use all endpoints authenticated(20 minutes time expiration for token).

P.S: In case of receive problems building application, like ERROR 137(memory), please use `make clear` and, after that, `make test` again, so we gonna rebuild application and execute the tests/coverage.

## Architecture

📦backend-python-creditcard<br>
┣ 📂alembic<br>
┃ ┣ 📂versions<br>
┃ ┣ 📜env.py<br>
┃ ┣ 📜README<br>
┃ ┗ 📜script.py.mako<br>
┣ 📂app<br>
┃ ┣ 📂api<br>
┃ ┃ ┗ 📂v1<br>
┃ ┃ ┃ ┣ 📂auth<br>
┃ ┃ ┃ ┃ ┣ 📜auth_bearer.py<br>
┃ ┃ ┃ ┃ ┣ 📜auth_handler.py<br>
┃ ┃ ┃ ┃ ┗ 📜**init**.py<br>
┃ ┃ ┃ ┣ 📂endpoints<br>
┃ ┃ ┃ ┃ ┣ 📜credit_card.py<br>
┃ ┃ ┃ ┃ ┣ 📜login.py<br>
┃ ┃ ┃ ┃ ┗ 📜**init**.py<br>
┃ ┃ ┃ ┗ 📜**init**.py<br>
┃ ┣ 📂core<br>
┃ ┃ ┣ 📜database.py<br>
┃ ┃ ┣ 📜settings.py<br>
┃ ┃ ┗ 📜**init**.py<br>
┃ ┣ 📂models<br>
┃ ┃ ┣ 📜credit_card.py<br>
┃ ┃ ┗ 📜**init**.py<br>
┃ ┣ 📂schemas<br>
┃ ┃ ┣ 📜credit_card.py<br>
┃ ┃ ┗ 📜**init**.py<br>
┃ ┣ 📜main.py<br>
┃ ┗ 📜**init**.py<br>
┣ 📂tests<br>
┃ ┣ 📂integration_tests<br>
┃ ┃ ┗ 📜test_credit_card_integration.py<br>
┃ ┣ 📂unit_tests<br>
┃ ┃ ┗ 📜test_credit_card.py<br>
┃ ┗ 📜**init**.py<br>
┣ 📜.coverage<br>
┣ 📜.coveragerc<br>
┣ 📜.env<br>
┣ 📜.env-example<br>
┣ 📜.gitignore<br>
┣ 📜alembic.ini<br>
┣ 📜docker-compose.yaml<br>
┣ 📜Dockerfile<br>
┣ 📜Makefile<br>
┣ 📜readme.MD<br>
┗ 📜requirements.txt<br>

My project's architecture is organized following some principles of the Domain-Driven Design (DDD) and the clean architecture. Here's a quick overview:

- **alembic**: This folder contains the Alembic configurations and migrations. Alembic is a database migration tool that I use to track changes in my database schema and helps manage schema migration scripts.
- **app**: This is where the main application logic resides. It's broken down into several subdirectories:

  - **api**: It contains the API versioning and its endpoints. In my case, the version v1 of the API.

    - **auth**: This is where the authentication logic is handled. I have different modules for different authentication functionalities.
    - **endpoints**: It contains the different API endpoints.

  - **core**: This directory holds my project's core functionality, such as database connections and settings.
  - **models**: It includes the database models. These are Pythonic representations of my database tables.
  - **schemas**: It contains Pydantic models. Pydantic models allow for data parsing, validation, and serialization (converting it into JSON).

- **tests**: This directory contains all my test cases, divided into unit, integration, and stress tests.
- **.env and .env-example**: These files are used to store environment variables.
- **docker-compose.yaml and Dockerfile**: These files are used to containerize the application and manage services, providing an isolated environment for running the app.
- **Makefile**: A simple way to organize code compilation. It contains a set of directives used by a make build automation tool to generate a target/goal.
- **requirements.txt**: This file lists all of the Python library dependencies that need to be installed using pip install.

The benefits of this architecture include:

1.  **Separation of Concerns**: Each part of the application has a specific job, making the code easier to understand, maintain, and develop.
2.  **Testability**: With separate sections for different aspects of the app, it's easier to test individual units of code.
3.  **Scalability**: With Docker and modular code, it's easier to scale up the application as needed.
4.  **Organization**: Code is easier to find in a well-structured project.
5.  **Version Control**: The separation also helps in managing version control, as changes can be isolated to specific areas of the project.
6.  **Database migration management**: With Alembic, database schema changes are tracked and managed effectively. This simplifies schema evolution and version control.
7.  **Reusability**: With a well-defined structure, it's easier to reuse components as needed.
8.  **Security**: Storing sensitive data in environment variables (.env file) protects the information from being exposed.

## Stack

| Tool     | Reason                                                                                                                                              |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Python   | Programming language with high readability and not verbose: helps in the maintenance and creation of codes with few lines and greater productivity. |
| FastApi  | Framework for creating APIs, automated documentation, and pydantic schema validation                                                                |
| Postgres | Database                                                                                                                                            |
| Alembic  | Tool that abstracts greater complexities for creating migrations                                                                                    |
| Pytest   | Python unit testing framework                                                                                                                       |

The application can also be run using make, with the following commands and helpers:
|Tool | Reason
|----------------|-------------------------------|
| `make test`| Build, run application and run unit/integration and coverage tests |
| `make clear`| Down and clean all docker images, volumes and containers |
| `make down` | Takes down the application|
| `make isort` | Applies isort throughout the repository to sort imports |
| `make black` | Applies the black linter |

## Database

The database has 2 tables:

- alembic_version: versions of Alembic migrations.
- credit_cards: data of our credit cards in the endpoint `'/credit-card'` [GET]

## Endpoints

The extensive documentation of all kinds of input and output can be found at [https://localhost/8000/docs](https://localhost/8000/docs) as indicated on how to run the application.

| Endpoint                        | Método | Retorno                                      |
| ------------------------------- | ------ | -------------------------------------------- |
| `/api/v1/login`                 | POST   | Performs user login and returns access token |
| `/api/v1/credit-card`           | POST   | Creates a new credit card                    |
| `/api/v1/credit-card`           | GET    | Returns all registered credit cards          |
| `/api/v1/credit-card/{card_id}` | GET    | Returns details of a specific credit card    |
| `/api/v1/credit-card/{card_id}` | DELETE | Deletes a specific credit card               |
| `/api/v1/credit-card/{card_id}` | PUT    | Updates details of a specific credit card    |

Please replace `{card_id}` with the ID of the credit card you want to get, delete, or update."
