# Technical test Solution
##### Author: Abdulvahab Kharadi Date:10/09/2020 


## Usage:
#### Setup environment and install dependency, run test and start application locally

`cd everis-tech-test`

`pip install -r requirements.txt`

`invoke test`

`python core.py product_id`

#### run application in docker container

`docker build ./ -t everis-tech-test`

`docker run -it -d --name everis-tech-test everis-tech-test`

`docker exec -it everis-tech-test bash`
`invoke test`

`python core.py product_id`





