# SwIRL-Shared-Space

TAMU CSCE606 project


# Getting Started

It is recommended to use Cloud9 as the development environment. The project uses ```pipenv``` as the dependency management tool. 
Please note that all the instructions below are based on the Cloud9 environment. If you seek to develop on the other platforms, you might need to some of the commands below to fit your own platform.

## 1. Create a new Cloud9 environment with Ubuntu 18.04

On Cloud9, create a new environment. All configurations are default except for the 'Platform'. **Choose 'Ubuntu Server 18.04 LTS' instead of 'Amazon Linux 2 (recommended)'**.

## 2. Configure Postgresql on Cloud9 (Ubuntu)

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
> **NOTE**: You can set your own password, but remember to set this password in the environment variable ```$SHARED_SPACE_POSTGRES_PASSWORD```. Or you can use the password in the secret file named ```SHARED_SPACE_POSTGRES_PASSWORD``` (which we used in the project). To learn about how to decrypt the secret file, please read later sections.
``` 
alter user postgres password <SHARED_SPACE_POSTGRES_PASSWORD>; 
```

### v. Create database
``` 
create database sharedspace; 
```
(For testing prupose, if you want to reset the database, use ``` drop database sharedspace; ``` to delete it first and create it again)


To exit psql, use ```\q```. To exit postgres terminal, use ```exit```.


## 3. Install Python Environment

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

## 4. Run Application (Locally)

### i. Migrate database

All migrations are included in the ```reservation/migrations``` folder. To migrate the database, run: 
``` 
./manage.py migrate 
```
> **NOTE**: There are 2 migration files in ```reservation/migrations```. ```0001_initial.py``` is generated with ```./manage makemigrations```. ```0002_auto_20220314_1558.py``` is manually configured to write some pre-assigned data into the database. If you make any change to the model file and want to re-generate the migartion files, you must keep the ```0002_auto_20220314_1558.py``` and only re-generate ```0001_initial.py```. To do so, move ```0002_auto_20220314_1558.py``` to somewhere else. Then, run ```./manage.py makemigrations```. Finally, move ```0002_auto_20220314_1558.py``` back to ```reservation/migrations```. This is the current suggested solution.

### ii. Decrypt secrets
There are several secrets (e.g. API secret and default admin password) that the application needs to read from environment variables. The secrets are encrypted in ```secrets.gpg```. Please first ask the instructor for the passphrase and then run ```gpg -d secrets.gpg``` to get the secrets.

### iii. Setup Environment Variables

After getting the secrets. Setup the following environment variables before running the application:

```
export SHARED_SPACE_GOOGLE_CLIENT_ID=<Client ID from the secret file>
export SHARED_SPACE_GOOGLE_SECRET=<Secret from the secret file>
export SHARED_SPACE_ADMIN_PASSWORD=<Default admin password>
export SHARED_SPACE_SECRET_KEY=<Django serect key>
export SHARED_SPACE_POSTGRES_PASSWORD=<PostgreSQL password>
```
You need to put these environment variables at the end of ```~/.bashrc``` and then run ```source ~/.bashrc``` to activate them.

> **NOTE**: For initial setup, you can simply use the password/API keys/secrets we have provided. For future development, you need to create your own Google APIs Project to generate the API keys/secrets. The procedures can be found at https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid

Below are the usage of those variables:
- SHARED_SPACE_GOOGLE_CLIENT_ID: **[Generate it yourself in the future]** Google API Client ID generated at Google Cloud Platform. Used for calling Google APIs
- SHARED_SPACE_GOOGLE_SECRET: **[Generate it yourself in the future]** Same as above.
- SHARED_SPACE_ADMIN_PASSWORD: The default admin account password (Default admin username is ```admin```). You can set your own password if you like.
- SHARED_SPACE_SECRET_KEY: The Django secret key. You can use any valid string to replace it (Avoid including special characters such as ```$@#!```)
- SHARED_SPACE_POSTGRES_PASSWORD: The password of the database. Set your own password if you like.




> **NOTE**: Those environment variables also need to be set on Heroku (You need to do this if you deploy on your own Heroku environment) for deployment and on Github for CI/CD (Already set up and you can check them in the repository ```Settings/Secrets/Actions``` page)
> - To setup environment variables on Heroku, in the project ```Setttings```, click ```Reveal Config Vars``` in ```Config Vars``` and then add the environment variables.
> - To setup environment variables on Github, you need to set them in the ```.github/workflow/django.yml``` (under the ```env``` tag). Since this is file can be seen by everyone, you should not directly put those secrets in the file. Instead, put them in Github Secrets and read them though ```${{ secrets.YOUR_SECRET_NAME }}```. In the project ```Settings/Secrets/Actions```, click ```New repository secret``` to add the secrets. (For more information about the Github workflow, please read https://docs.github.com/en/actions/using-workflows/about-workflows)

### iv. Run Server

Finally, run the following command to start the application:

```
./manage.py runserver $IP:$PORT
```

> **NOTE**: To use google login, you need to send me your aws hostname, e.g., 629260b04e324c2e8370ad27004c4609.vfs.cloud9.us-east-1.amazonaws.com. Only after adding your url into the white list, you can use the Google API in the application. Thus, creating your own Google API project and replace the client ID, secret in the environment variables is strongly suggested.


## 5. Deploy on Heroku

### i. Setup Heroku



#### **a. Create Heroku Project**
Create a heroku account at https://www.heroku.com/.

Log in to the Heroku. Then Click ```New``` to create a new app. 

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