My personal website
===================

This is a little Django test that turned into my personal webpage. Feel free to copy and reuse!

Here are some details about the applications you'll find here:

- *polls*: this application is the one explained in the Django tutorial (https://docs.djangoproject.com/en/1.7/intro/tutorial01/). It shows how to get data from a form and store it in a database, and how to retrieve data from the database and display it on a web page.
- *weather*: this application is just a test to use web based services (REST - JSON) in Python
- *imageconv*: the aim of this application is to use a form to load media files, use form validation and use a background process to handle time-consuming tasks. It also stores temporary files to Amazon S3.

*** Getting started ***

First make sure the requirements are fulfilled:
- Python 2.7
- pip (python-pip)
- postgresql 
- image libraries (libjpeg-dev, zlib1g-dev, libpng12-dev)
- redis (redis-server)
- the following environment variables are defined:
    - SECRET_KEY : Django secret key
    -   AWS_ACCESS_KEY : Amazon AWS credentials
    -   AWS_SECRET_KEY : Amazon AWS credentials
    -   S3_BUCKET : S3 bucket where the temporary files will be stored. A policy has to be created to make all the objects created in this bucket public. Also, it is recommended to set an expiration period for all the objects in the bucket to avoid filling up all the available memory.

Clone the repository to your computer
```
git clone https://github.com/gregoryfryns/personal_website.git
```

Go to the project root directory and create a virtual environment
```
pip install virtualenv
virtualenv venv
```

Activate the virtual environment and download the dependencies
```
source activate venv/bin/activate
pip install -r requirements.txt --allow-all-external
```
Run the local server using foreman
```
foreman start
```

Once done, you can leave the virtual environmant using this command
```
deactivate
```
