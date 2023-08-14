# Online Food Store

This repository contains the code for the "Online Food Store" web application. Below is a detailed description of the project and the technologies used.

Video Preview:

[![Video Preview](https://img.youtube.com/vi/ooV965zULPk/0.jpg)](https://www.youtube.com/watch?v=ooV965zULPk)

## Project Overview

The "Online Food Store" is an online grocery store where users can order food products. The project provides the following features:

- User registration and authentication.
- Language selection option (English or Ukrainian) for user convenience.
- Sorting of products based on various parameters.
- Payment processing through the Stripe payment system.
- The following database was used [Neon](https://console.neon.tech/): postgresql
- For caching [Redis](https://app.redislabs.com/)

## Technologies Used

The "Online Food Store" project utilizes the following technologies and libraries:

- Django: A popular Python web framework for developing web applications.
- Celery: A library for asynchronous task execution in the background, used for sending email notifications.
- Redis: A caching system used for storing and accessing frequently sold products and recommendations.
- Cloudinary: A cloud-based service for storing and optimizing images, used for storing product images in the project.
- Django Rest Framework: to build an API service for orders.

## Deployment
1. [Koyeb](https://pivfabrucaty-goit.koyeb.app/en/): https://pivfabrucaty-goit.koyeb.app

2. Or you can run in the docker container with the following command:
- docker-compose up
- python pastyshop/manage.py migrate
- python pastyshop/manage.py createsuperuser
(You must create super user.)
- python pastyshop/manage.py loaddata pastyshop/mydata.json


## Used Technologies

- [Python](https://www.python.org/): ^3.11
- [Django](https://www.djangoproject.com/): ^4.2.1
- [Pillow](https://python-pillow.org/): ^9.5.0
- [Celery](https://docs.celeryproject.org/): 5.2.7
- [django-environ](https://github.com/joke2k/django-environ): ^0.10.0
- [Flower](https://github.com/mher/flower): ^1.2.0
- [Stripe](https://stripe.com/): 4.0.2
- [WeasyPrint](https://weasyprint.org/): 56.1
- [Redis](https://redis.io/): 4.3.4
- [django-rosetta](https://github.com/mbi/django-rosetta): 0.9.8
- [django-parler](https://django-parler.readthedocs.io/): ^2.3
- [django-localflavor](https://django-localflavor.readthedocs.io/): ^4.0
- [cloudinary](https://cloudinary.com/): ^1.33.0
- [django-cloudinary-storage](https://pypi.org/project/django-cloudinary-storage/): ^0.3.0
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/): ^2.9.6
- [whitenoise](https://pypi.org/project/whitenoise/): 6.4.0
- [djangorestframework](https://www.django-rest-framework.org/): ^3.14.0

## Author

The "Online Food Store" project was developed by [Ihor Voitiuk](https://github.com/ihor-vt).

---
