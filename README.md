# Digital Water Audit Tool

Digital Water Audit Tool is a web application designed to facilitate efficient water management and auditing processes. It integrates various technologies to provide a comprehensive platform for analyzing water usage and implementing water conservation strategies.

## Technical Features

- **Real-Time Data Processing**: Leverage real-time data handling to provide up-to-date water audit results.
- **Interactive Dashboards**: Utilize Dash and Plotly for creating interactive, real-time visualizations of water usage statistics.
- **Responsive Design**: Ensure a responsive web interface compatible with various devices, using Django and Dash Bootstrap Components.
- **Advanced Data Analytics**: Incorporate NumPy and Pandas for sophisticated data analysis and operations.
- **Application**: Utilize Django for building a scalable application.
- **Security Features**: Implement OAuth2 with Django Allauth for secure authentication processes.
- **PDF Reporting**: Use ReportLab for generating customizable, downloadable PDF reports of audit results.
- **Flowchart Visualization**: Integrate Reactflow Dash for creating interactive flowcharts of water usage processes.

## Tools Used

- Django
- ReactJS
- ReactFlow
- PostgreSQL
- Pandas
- Plotly and Plotly Dash
- Pydeck
- Bootstrap
- TailwindCSS
- ReportLab

- **Back-end Framework**: Django 5.0.3
- **Front-end Framework**: TailwindCss, Bootstrap, Javascript, ReactJS, Reactflow Dash with Django-Plotly-Dash integration
- **Database**: PostgreSQL by Render (Setup not included in this README)
- **Version Control**: Git

## Application Setup

### Prerequisites

- Python 3.8 or above
- pip and virtualenv
- Sqlite (if setting up with a local database)

### Application Setup

- Clone the repository
    > `git clone https://github.com/ArohanP/Digital_water_audit`
- Create a virtual environment
    > `python3 -m venv env`
- Activate the virtual environment
    > `source env/bin/activate`
- Install the requirements
    > `pip install -r requirements.txt`
- Create a `.env` file in the application directory along with `setting.py` file
    > `touch .env`

- Setup environment variables
    - Add the following to the `.env` file
    > `SECRET_KEY=your_secret_key`
    > `DEBUG=True`
    <!-- - `DB_NAME=your_db_name`
    - `DB_USER=your_db_user`
    - `DB_PASSWORD=your_db_password`
    - `DB_HOST=your_db_host`
    - `DB_PORT=your_db_port` -->

<!-- ### Database Setup

- Create a database in PostgreSQL
    - `CREATE DATABASE your_db_name;`
- Create a user in PostgreSQL
    - `CREATE USER your_db_user WITH PASSWORD 'your_db_password';`
- Grant all privileges to the user
    - `GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;` -->

### Running the application

- Run the migrations
    > `python manage.py makemigrations`
    >
    > `python manage.py migrate`
- Run the server
    > `python manage.py runserver`

### Setup Google Authentication

- Everytime we migrate a new database, we need to register our site from django's admin portal on **Sites** and then register that site with google on **Social Applications** in Django admin. Then only authentication will work.


### Workspace Structure
The workspace is organized into several directories and files. Here's a brief overview:

- **frontend/:** Contains the React application for the frontend of the project. This includes the `src/` directory where the source code resides, and the public/ directory which contains the static files.
waterflow/: Contains the Django application for the backend of the project. This includes Python files for models, views, forms, and serializers.

- **wat/:** Contains the Django settings for the project.

- **waterflow/:** Contains the Django application for the backend of the project. This includes Python files for models, views, forms, and serializers.

- **templates/:** Contains HTML templates for the Django application.

- **static/:** Contains static files for the Django application.

- **manage.py:** Django's command-line utility for administrative tasks.

- **requirements.txt:** Lists the Python dependencies required for the project.

- **README.md:** Provides an overview of the project and setup instructions.

- [build.sh](frontend/README.md): A shell script for building the project.

- **db.sqlite3:** The SQLite database file.

- **.gitignore:** Specifies files and directories to be ignored by Git.


## Backend

The backend of the application is built using Django. The main entry point of the application is `views.py` in the `waterflow/` directory. The backend is responsible for handling requests, processing data, and interacting with the database.

The backend is integrated with the frontend using Django templates and Controllers/Views.



## Frontend

Most of the frontend is built using Django templates and Bootstrap. The main entry point of the application is `home.html` in the templates folder. The frontend is integrated with Django using the `base.html` template file in the templates folder which is base structure for all the templates, provides fix header and footer for remaining templates.

### Flowchart Using Reactflow

The frontend to show flowchart of the application is built with React. It resides in the `frontend/` directory and was bootstrapped with Create React App. The main entry point of the application is frontend/public/index.html, which includes a div with the id `root` >where the React application is injected. Then this application is integrated with Django using `flowchart.html` template file in the templates folder.

Resides in the frontend folder. To run the flowchart, navigate to the frontend folder and run the following commands:

- Install the dependencies
    > `npm install`
- Run the flowchart
    > `npm start`

## Deployment
The application has been deployed to Render. The deployment process involves setting up a PostgreSQL database, configuring environment variables, and deploying the application using the Render dashboard. The account used for the deployment is `datascienceiccw@iccwindia.org`.

## Contributors

- [Arohan Paul]()
- [Viraj Sharma]()
- [Manaswita Mandal]()