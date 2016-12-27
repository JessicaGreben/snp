## Synopsis
An application about investing as an alternative to spending.  

## Installation

To get this application running locally:
1.clone the repo
    git clone git@github.com:JessGreben/snp.git
2. build the docker container (assuming docker is installed)
From the snp dir:
    docker build -t snp .
3. run the docker container
    docker run -p 8080:8080 snp
4. To view app:
If using docker on OSX, you will need to use the IP of the docker-machine to view the running application.
Get the IP of docker-machine by running:
    docker-machine ip default
In the web browser navigate to [docker-machine-ip]:8080
    
## Tests

You can run tests with:

    trial test/
