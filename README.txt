HOW TO RUN THE APP
==================

STEP 1 - Install MySQL
**********************
Go to https://dev.mysql.com/downloads/mysql/ and download MySQL for your operating system.
Follow the installer. At some point it will ask you to set a root password - remember this password, you will need it later.


STEP 2 - Install Python dependencies
**************************************
In your terminal, navigate to the project folder and run:
    pip install flask mysql-connector-python werkzeug


STEP 3 - Set your database password in the project
**************************************************
Open the file called "__init__.py" and find this section near the top:

    DB_CONFIG = {
        "host": "localhost",
        "user": "root",
        "password": "yourPassword",
        "database": "RWD"
    }

Replace "yourPassword" with the password you chose in Step 1.

Do the same in the file called "models.py".


STEP 4 - Run the app
********************
In your terminal, make sure you are in the project folder, then run:
    python run.py

The app will automatically create the database, set up all the tables, and fill them with test data.

Open your browser and go to: http://localhost:5000