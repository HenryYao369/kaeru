Kaeru
=====

Files for the [Kaeru Language](http://www.kaeru-lang.org) website.
Eventually, these should be on a dedicated branch of this repository, but for now I guess this is fine.

How to Update the Site
----------------------

The user-facing website is at http://www.kaeru-lang.org, which is hosted on [Cornell Systems Lab](http://www.systems.cs.cornell.edu) servers.
Use the following workflow to push updates to the main site:

1. Clone this repository locally.
2. Hack, hack, hack. View the site _locally_ until you're ready to make the changes live.
3. Push your updates to the main repo with `git push origin master`.
4. Log into the server via `ssh <your-name>@www.kaeru-lang.org`. Enter your username and password.
5. Change into the Kaeru director with `cd /var/www/kaeru-lang.org`.
6. Pull the new changes with `git pull origin master`.

Enjoy!
