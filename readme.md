# Django Project Installation Guide

Welcome to the Django Project! This guide will help you set up and run the project on your local machine.

## Prerequisites

Ensure you have the following installed:

- Python (version 3.8 or higher)

- Git (for version control)

- MySql

## Installation Steps

Follow these steps to get the project up and running:

### Cloning the Repository

First, clone the repository from GitHub:

```bash
git clone <current repo link>
```

### Setup Project Dependencies

Install project dependencies

```
pip install -r requirements.txt
```

Setup the mysql database named django_blog and run the following command

```
python manage.py makemigrations
python manage.py migrate
```

### Run the development server

```
python manage.py runserver
```

### To visit the Django admin pannel

```
First create super user with your email and password  : py manage.py createsuperuser
Then vist the url : http://127.0.0.1:8000/admin
```

### Some command may differ if you are using operating system other than windows.
