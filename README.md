### Hexlet tests and linter status:
[![Actions Status](https://github.com/tpl-86/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/tpl-86/python-project-83/actions)

Page Analyzer is a site that analyzes specified pages for SEO suitability, similar to PageSpeed ​​Insights.

Step 1: Clone the repository
    First, clone the repository to your local machine:
    git clone <repository URL>
    cd <project folder>

Step 2: Installing Dependencies
    2.1 Creating a Virtual Environment
        To isolate dependencies, create a virtual environment.

        For Linux/MacOS:
        python3 -m venv .venv

        For Windows:
        python -m venv .venv
    
    2.2 Activate virtual environment
    
Step 3: Setting up the database
    Import database schema:
    psql -U <user> -d <database_name> -f database.sql

    Setting Environment Variables
    DATABASE_URL=postgres://<user>:<password>@localhost/<database_name>
    SECRET_KEY=<random_key_for_security>
    DATABASE_SSL_MODE=disable # or 'require' to use SSL

Step 4: Commands for work:
    4.1 To install dependencies and sync:
        make install
    4.2 To run linting:
        make lint
    4.3 To run the application in development mode:
        make dev
    4.4 To run your application in production mode with Gunicorn:
        make start
    4.5 To run using Gunicorn for rendering:
        make render-start

https://python-project-83-n1p3.onrender.com