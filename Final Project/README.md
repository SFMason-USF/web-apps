# Student Site Rating Site

This website will allow instructors to manage student web projects and students to rate those
projects.

### Prerequisites

Python 3

### Installing

Install flask and passlib python libraries.

```
pip install flask
```

```
pip install passlib
```

That's it! See deployment for further instructions.

## Deployment

Run app.py.

Your server will now be running on localhost port 5000.

To view this app in a browser on the machine it is running, go to the url http://localhost:5000

Now to start the database off as an admin, go to your site running on port 5000 and log in with the
following credentials:

* username: admin

* password: admin

From there, you can access the instructor dashboard, and most importantly, upload a csv file
containing login information. This way you can establish your own instructor account, as well as the
necessary student accounts.

Note: Any instructor account can add new logins to the database The preexisting admin account is
there to get you up and running as the site administrator.

Once you have your accounts uploaded, you can access the site.

## Built With

* [jQuery](http://jquery.com/) - Front-end JavaScript library
* [Bootstrap](https://getbootstrap.com/) - Front-end style library
* [Flask](http://flask.pocoo.org/) - Back-end server client library

## Authors

* **Spenser Mason** - Front-end design - [SFMason](https://github.com/SFMason)
* **Jacob Kleinsorge** - Back-end development -
  [JacobKleinsorge](https://github.com/JacobKleinsorge)
