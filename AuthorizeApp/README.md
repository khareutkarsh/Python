# Authorize App

This is a streaming application that authorizes a transaction for a specific account following a set of predefined rules.

## Design Approach

This application is built in python using socket streaming which starts a server to authorize transactions based on the requirement given in spec.md

- the application uses in-memory data structure to hold the data till the application is reset
- __main__.py is the main entry point of the code to start the server
- StreamingClient(second project) is a client application which can be used to send command line messages to the server


## Installation

#### Applicaiton installion
- unzip the AuthorizeApp project
- execute below command from the root folder of the project to build the egg file
```shell script
$AuthorizeApp>python setup.py bdist_egg
```
- Navigate to the AuthorizeApp/dist folder in the root directory of the project
```shell script
$AuthorizeApp>cd dist
```
- Execute the AuthorizeApp-1.0.0-py3.7.egg (py3.7 python version can differ based on installation) file using below command to start the server
```shell script
$AuthorizeApp/dist>python AuthorizeApp-1.0.0-py3.7.egg.egg
```
####Client installation

- Unzip the StreamingClient project and execute the below command to start the client
```shell script
$StreaminClient>python pycripts/streaming_client.py
```
####pytest Installation
For installing pytest execute the below command
```shell script
$>pip install -U pytest
```

## Tests
####Unit tests
To run the unit tests execute the following command or execute the shellscripts/run_pytest.sh

```shell script
pytest AuthorizeApp/tests/unit
```
####Integration tests
- Integration test can be tested once the server is up an running.
- It reads a file AuthorizeApp/tests/integration/integration_testdata.txt. This file is a | delimited and contains two columns, first is input and second is expected output.
```shell script
$AuthorizeApp/tests/integration>head integration_testdata.txt
{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}|{"account": null, "violations": ["account-not-initialized"]}
{"account": {"active-card": true, "available-limit": 100}}|{"account": {"active-card": true, "available-limit": 100}, "violations": []}
...........................................................
...........................................................
``` 
- integration_testdata file is created based on the scenarios given in spec.md
- This test validates the output received from server with the expected outputs
- On execution it prints all the test step results as PASS/FAIL
```shell script
$AuthorizeApp/tests/integration>python authorizeapp_integration_test.py
input : {"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}} expected : {"account": null, "violations": ["account-not-initialized"]} test result:PASS 
```
- If there is no error means the test is successful otherwise if any scenario FAILs it will break the integration test
- To run the integration tests execute the below command(as mentioned in assumptions a fresh instance of the server is required to run the test)

```shell script
$AuthorizeApp>python AuthorizeApp/tests/integration/authorizeapp_integration_test.py
```

## Usage

- Start the server  by executing the egg file as illustrated in the installation steps
- Once the server starts it will display the below message
```shell script
20/16/02 00:02:14 INFO     streaming_server[streaming_server.py:68] Serving on ('127.0.0.1', 2222)
```

- Start the client as illustrated in the installation steps
- Once the client has started type/paste the message to be sent and hit enter
 
```json
enter the message: {"account": {"active-card": true, "available-limit": 100}}
```
## Assumptions

  - This project is built in Python 3.7 so assuming python is already installed
  - Client is a separate project that will send and receive command line messages(for details refer README.md of client project)
  - Server will run forever till the time it is terminated or window is closed   
  - Application uses the same IP and PORT as the server was configured, which can be changed in the constants according to our needs
  - Once constants are updated one needs to re-build the eggfile 
  - Integration test to be run after starting the server
  - Validations for input message format are not added as per spec.md
  - sqllite db (which comes with python) was not used as it was mentioned not to use any external data base. But can be integrated easily if asked to extend the application at a later stage
  - The JSON format of input and output messages is taken from the spec.md
  - pytest is used to create unit test cases
  - Account status can be changed to 'card-not-active' if available-limit becomes 0
  - Account can be reactivated by sending the account details with active-card and available-limit
  - The violated transactions are also maintained in-memory for later use
  - There are shellscripts and batscripts folders, with their specific README.md, present in both the projects to automate the installation and testing process
  - These shellscitps and batscripts have been changed to .txt file to avoid mail blockers