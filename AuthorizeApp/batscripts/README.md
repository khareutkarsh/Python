# Batch scripts for automation 

These scripts are written to provide automated building of the project and running test cases

##Execution

- Rename the scripts from .txt to .sh and then execute the respective files

```
AuthorizeApp/shellscirpts>ren build_egg.txt build_egg.bat
AuthorizeApp/shellscirpts>build_egg.bat
```
##Script Details
#### install_pytest.txt
This file is used to install the pytest module
#### build_egg.txt
This file is used to build the egg file of the project
### run_pytest.txt
This file is used to run the unit test cases
### run_integration_test.txt
This file is used to run the integration tests when a fresh instance of server is running