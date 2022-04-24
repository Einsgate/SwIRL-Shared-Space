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

### Configure Postgresql on Cloud9 (Ubuntu)

#### 1. Install and configure postgres

Install postgres
	``` sudo apt-get install postgresql ```

Switch to postgres account
	``` sudo -u postgres -i ```

Connect to postgres
	``` psql -U postgres ```

Set password
	``` alter user postgres password 'postgres'; ```


If you have created sharedspace database, use ``` drop database sharedspace; ``` to delete it first

Create database
``` 
create database sharedspace; 
```


#### 2. Update dependencies
``` 
pipenv install 
```


#### 3. Migrate database
``` 
./manage.py migrate 
```

#### 4. Runserver
``` 
./manage.py runserver $IP:$PORT 
```


NOTE: To use google login, you need to send me your aws hostname, e.g., 629260b04e324c2e8370ad27004c4609.vfs.cloud9.us-east-1.amazonaws.com. After adding your url into the white list, you can use the google auth.


### Deploy on Heroku
Login
``` heroku login -i ```

Reset database
``` heroku pg:reset ```

Deploy with a given branch
``` git push heroku testbranch:main ```
