## Synopsis
An application about investing as an alternative to spending.  

## Get App Running Locally

#### To run this application locally you can do it the old fashion way or with docker.

### Old Fashion Way

1. clone the repo

    git clone git@github.com:JessGreben/snp.git
  
2. install the dependencies

    pip install -r snp/app/requirements.txt
    
3. start the web server. From the snp/app/ dir run:

    python server.py
    
### Using Docker
    
1. Pull down the docker container
    
    docker pull jessicagreben/snp

2. Run the Docker container and expose port 8080

    docker run -p 8080:8080 jessicagreben/snp
    
3. View app at 127.0.0.1:8080
    
## Tests

You can run tests from the snp/app/ directory:

    trial test/
