# coastal-image-browser
REST API for coastal images

[![Requirements Status](https://requires.io/github/openearth/coastal-image-browser/requirements.svg?branch=master)](https://requires.io/github/openearth/coastal-image-browser/requirements/?branch=master)
[![CircleCI](https://circleci.com/gh/openearth/coastal-image-browser.svg?style=svg)](https://circleci.com/gh/openearth/coastal-image-browser)

This is a Django web application with REST API to serve the coastal images as collected from field stations with the coastal-image-archive (https://github.com/openearth/coastal-image-archive).

# Getting started

Install mysqldb, e.g. in Ubuntu:
```sh
$ sudo apt-get install python-mysqldb
```
Or in CentOS:
```sh
$ sudo yum install MySQL-python
```

Create virtualenv

Install requirements
```sh
$ pip install -r requirements.txt
```

Create a ```.my-images.cnf``` file using ```.my-images.cnf.tmpl``` as a template

Run application
```sh
python manage.py runserver
```
