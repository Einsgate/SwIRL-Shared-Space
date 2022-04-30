# SwIRL-Shared-Space

TAMU CSCE606 project


# Development Guide

It is recommended to use Cloud9 as the development environment. The project uses ```pipenv``` as the dependency management tool. 
Please note that all the instructions below are based on the Cloud9 environment. If you seek to develop on the other platforms, you might need to some of the commands below to fit your own platform.

## Create a new Cloud9 environment with Ubuntu 18.04

On Cloud9, create a new environment. All configurations are default except for the 'Platform'. **Choose 'Ubuntu Server 18.04 LTS' instead of 'Amazon Linux 2 (recommended)'**.

## Configure Postgresql on Cloud9 (Ubuntu)

### i. Install postgres
``` 
sudo apt-get install postgresql 
```

### ii. Switch to postgres account
``` 
sudo -u postgres -i 
```

### iii. Connect to postgres
``` 
psql -U postgres 
```

### iv. Set password
``` 
alter user postgres password 'postgres'; 
```

### v. Create database
``` 
create database sharedspace; 
```
(For testing prupose, if you want to reset the database, use ``` drop database sharedspace; ``` to delete it first and create it again)


To exit psql, use ```\q```. To exit postgres terminal, use ```exit```.


## Install Python Environment

The required default Python3 version on Cloud9 is 3.6, which is used in this project. The project uses ```pipenv``` to manage the Python invironment.

### Install pipenv

Run the following command to install pipenv:

```
pip3 install pipenv
```

After installation, switch to the root directory of the project. Then, run
```
pipenv shell
```
to enter the virtual environment for development. NOTE: Every time you open Cloud9 and before development, you need to execute this command first to enter the virtual environment.

### Install dependencies

All the dependencies are included in the ```Pipfile```. To install them, under the root directory of the project, simply run:

```
pipenv install
```

## Run Application (Locally)

### Migrate database

All migrations are included in the ```reservation/migrations``` folder. To migrate the database, run: 
``` 
./manage.py migrate 
```
NOTE: There are 2 migration files in ```reservation/migrations```. ```0001_initial.py``` is generated with ```./manage makemigrations```. ```0002_auto_20220314_1558.py``` is manually configured to write some pre-assigned data into the database. If you make any change to the model file and want to re-generate the migartion files, you must keep the ```0002_auto_20220314_1558.py``` and only re-generate ```0001_initial.py```. To do so, move ```0002_auto_20220314_1558.py``` to somewhere else. Then, run ```./manage.py makemigrations```. Finally, move ```0002_auto_20220314_1558.py``` back to ```reservation/migrations```. This is the current suggested solution.



### Setup Environment Variables

Some of the secrets (e.g. API secret and default admin password) are read from the environment variables. Below are the variables you need to setup before running the application:

```
export SHARED_SPACE_GOOGLE_CLIENT_ID=<Client ID from the secret file>
export SHARED_SPACE_GOOGLE_SECRET=<Secret from the secret file>
export SHARED_SPACE_ADMIN_PASSWORD=<Default admin password>
export SHARED_SPACE_SECRET_KEY=<Django serect key>
```

Those secrets can be found in the encrypted file ```secrets.zip```.

### Run Server

Finally, run the following command to start the application:

```
./manage.py runserver $IP:$PORT
```

NOTE: To use google login, you need to send me your aws hostname, e.g., 629260b04e324c2e8370ad27004c4609.vfs.cloud9.us-east-1.amazonaws.com. Only after adding your url into the white list, you can use the Google API in the application. Thus, creating your own Google API project and replace the client ID, secret in the environment variables is strongly suggested.


## Deploy on Heroku

### i. Setup Heroku

#### Create Heroku Project
TODO: Finish this.

#### Setup Heroku Environment Variables
TODO: Finish this.

### i. Login
First, you need to log in to your Heroku account:
``` 
heroku login -i 
```
Then, enter your username and password to log in.

### ii. Reset database (Optional. Do this if you changed your model. **Be careful, this operation will reset the database and you will lose all data in it. It is ONLY used for test environment.** \)
``` 
heroku pg:reset 
```

### iii. Deploy with a given local branch
``` 
git push heroku <local_branch>:main 
```

or if you want to simply deploy the main branch, switch to ```main``` branch, then use:
```
git push heroku
```