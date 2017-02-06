# Diplomatool

*Explanations for the images are available below*

**Tests** *(image is a link)* : [![Build Status](https://travis-ci.org/olety/Diplomatool.svg?branch=master)](https://travis-ci.org/olety/Diplomatool) 

**Documentation** *(image is a link)* : [![Documentation Status](https://readthedocs.org/projects/diplomatool/badge/?version=latest)](http://diplomatool.readthedocs.io/?badge=latest) *text link* [http://diplomatool.readthedocs.io/](http://diplomatool.readthedocs.io/)
                
**[Link to the site](http://207.154.202.19/)**                

### User credentials

Admin credentials:
* Login: admin@site.site
* Password: `password123`

Student credentials:
* Login: stud@site.site
* Password: `password123`

Reviewer credentials:
* Login: rev@site.site
* Password: `password123`

### Explanations

#### Tests

We've used a continious integration tool called Travis-CI for testing. It's a very popular test automation tool, 
that runs test after every commit, and notifies you if they fail. 

It executes `python3 manage.py test`, which automatically runs our tests (both unit and integration). Test sources are in [site_app/tests.py](site_app/tests.py).

Automation of integration tests was possible by using a `Client` class in Django to simulate the behaviour of a users browser.

Our page on there is available by clicking [![Build Status](https://travis-ci.org/olety/Diplomatool.svg?branch=master)](https://travis-ci.org/olety/Diplomatool)

#### Documentation

We've used a `Sphinx` package to generate documentation from the python docstrings (comments underneath the class, 
something similar to C#'s `summary` comments) and hosted it on [ReadTheDocs](http://readthedocs.io) - a very popular 
and widely used documentation hosting service. 

Our page on there is available by clicking on the 
[![Documentation Status](https://readthedocs.org/projects/diplomatool/badge/?version=latest)](http://diplomatool.readthedocs.io/?badge=latest) image.

## Other

Software System Development project for the Wroclaw University of Technology.

### Authors
* Oleksii Kyrylchuk  
* Piotr Fudali
