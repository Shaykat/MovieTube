# Movie Tube

This Application can be run in Linux, Windows and Mac OS. We developed this project in Mac OS and also deployed it on a Linux server. It will perform better in the Linux environment.


## Configuration For Linux:
First download the necessary packages: 
```sudo add-apt-repository ppa:jonathonf/python-3.6 
sudo apt-get update 
sudo apt-get install python3.6 python-pip python-dev libpq-dev postgresql postgresql-contrib ffmpeg
```
## Create PostgreSQL Database and User
login as postgres console
```
sudo su postgres psql
```

Create Database
```
CREATE DATABASE db_name
```
Create User
```
CREATE USER db_user WITH PASSWORD ‘****’
```

Provide Privileges
```
GRANT ALL PRIVILEGES ON DATABASE db_name TO db_user;
```

Exit from postgres console
```
\q exit
```


## Install Virtual Environment
Update pip and install virtual environment:
```
sudo pip install --upgrade pip 
sudo apt-get install virtualenv 
sudo pip install --upgrade virtualenv
```
## Create a project directory:
```
mkdir/MovieTube 
cd /MovieTube
```

## Create virtual environment and activate:
```
virtualenv --python=python3.6 venv 
source venv/bin/activate
```

## Install Python Packages:
```
pip install psycopg2 django==3.0.3 psycopg2==2.8.4 Pillow==7.0.0 pandas==1.0.3
or
pip install -r req_lib.txt
```

## Clone The Project and Setup
Clone The Project:
```
Git clone https://github.com/Shaykat/MovieTube
```

### Update Database settings
Change the Django database setting with your database information in movieTube/settings.py file
```
DATABASES = {
'default' :
{
'ENGINE' : 'django.db.backends.postgresql_psycopg2' ,
'NAME' : 'db_name' ,
'USER' : db_user ,
'PASSWORD' : **** ,
'HOST' : 'localhost' ,
'PORT' : '' ,
}
}
```

### Set Static Root and URL:
```
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static" ) MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media" )
```

### Allowed Hosts:
```
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'www.localhost']
```
### Make Migrations for Generate Database According to Model:
```
cd MovieTube 
Python manage.py makemigrations 
Python manage.py migrate
```

### Collect all the static files:
```
Python manage.py  collectstatic
```

### Create Super User
```
Python manage.py createsuperuser
```

### Run The Application:
```
Python manage.py runserver
```

## For Mac OS 
```
just install packages using Brew
```
