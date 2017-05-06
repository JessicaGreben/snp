[![Build Status](https://travis-ci.org/JessicaGreben/snp.svg?branch=master)](https://travis-ci.org/JessicaGreben/snp) [![Coverage Status](https://coveralls.io/repos/github/JessicaGreben/snp/badge.svg)](https://coveralls.io/github/JessicaGreben/snp)

## Synopsis
An application about investing as an alternative to spending.  

## Get App Running Locally

#### To run this application locally you can do it the old fashion way or with docker.

### Old Fashion Way

Clone the repo:
    
    git clone git@github.com:JessGreben/snp.git
  
Install the dependencies:

    pip install -r snp/app/requirements.txt
    
Postgres expects these environment variable exist:

    DB_HOST=localhost
    DB_USER=<user>
    
Where `DB_USER` is the user name to connect as. Defaults to be the same as the operating system name of the user running the application. See [Postgres docs](https://www.postgresql.org/docs/9.3/static/libpq-connect.html) for more details if needed.

You may need to start the [postgres database server](https://www.postgresql.org/docs/8.3/static/server-start.html):

    pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start

Start the web server. From the `snp/app/` dir run:

    python server.py
    
### Using Docker (assumes you already have docker installed)
    
Pull down the docker container
    
    docker pull jessicagreben/snp

Run the Docker container and expose port 8080

    docker run -p 8080:8080 jessicagreben/snp
    
View app at 127.0.0.1:8080

    
## Tests

Run the unit tests from `snp/app/` directory with the following command:

    pytest test/
 
For unit test coverage report to print to the terminal, run:

    pytest --cov-report term-missing --cov .
    
For unit test coverage report to write to a html file, run:

    pytest --cov-report html --cov .
    
You can view the coverage file in the browser by running the following from the snp/app/ directory:

    open htmlcov/index.html
