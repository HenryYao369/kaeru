Kaeru
=====

Files for the [Kaeru Language](http://www.kaeru-lang.org) website.
Implemented using [Django 1.5.1](https://docs.djangoproject.com/en/1.5/) on [Python 2.7](https://docs.python.org/2.7/).
Hosted by [systems.cs.cornell.edu](http://www.systems.cs.cornell.edu/)

How to Update the Site
----------------------

Use the following workflow to push updates to the main site:

1. Clone this repository locally.
2. Hack, hack, hack. View the site _locally_ by starting the Django server via `python manage.py runserver`.
3. Push your updates to the main repo with `git push origin master`.
4. Log into the syslab server with `ssh www.kaeru-lang.org`. Enter your username and password.
5. Use `git pull` to update the existing files on the site.
6. Admire your changes at http://www.kaeru-lang.org

Enjoy!
