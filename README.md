# Water Audit Tool

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

- Everytime we migrate a new database, we need to register our site from django's admin portal on **Sites** and then register that site with google on **Social Applications**. Then only authentication will work.