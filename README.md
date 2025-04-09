### Hexlet tests and linter status:
[![Actions Status](https://github.com/tpl-86/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/tpl-86/python-project-83/actions)

**Page Analyzer is a site that analyzes specified pages for SEO suitability, similar to PageSpeed ​​Insights**

1. Clone the repository
    git clone <repository URL>
    cd <project folder>

2. Creating and activate virtual environment
    python3 -m venv .venv
    source .venv/bin/activate

3. Setting up the database
    - Import database schema:
        psql -U <user> -d <database_name> -f database.sql

    - Setting Environment Variables
        DATABASE_URL=postgres://<user>:<password>@localhost/<database_name>
        SECRET_KEY=<random_key_for_security>
        DATABASE_SSL_MODE=disable # or 'require' to use SSL

4. Commands for work:
    - To install dependencies and sync:
        make install
    - To run linting:
        make lint
    - To run the application in development mode:
        make dev
    - To run your application in production mode with Gunicorn:
        make start
    - To run using Gunicorn for rendering:
        make render-start

https://python-project-83-n1p3.onrender.com