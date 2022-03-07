# SwIRL-Shared-Space

TAMU CSCE606 project


## Development Guide

It is recommended to use Cloud9 as the development environment. The project uses ```pipenv``` as the dependency management tool. 
Below are the instructions on Cloud9. 

### Create a new Cloud9 environment with Ubuntu 18.04

In Cloud9, create a new environment. All configurations are default except for the 'Platform'. Choose 'Ubuntu Server 18.04 LTS' instead of 'Amazon Linux 2 (recommended)'.

### Install pipenv
Run the following command to install pipenv:

```
pip3 install pipenv
```



### Run Application

First, run ```pipenv shell``` to activate the virtual Python environment.

Then, run the following to start the application:

```
python manage.py runserver $IP:$PORT
```