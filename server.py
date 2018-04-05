"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)




@app.route("/register")
def register_form():
    """Show registration form"""

    return render_template("register_form.html")




@app.route("/register", methods=["POST"])
def register_process():
    """Processes registration form"""
    email = request.form["email"]
    password = request.form["password"]
    age = request.form["age"]
    zipcode = request.form["zipcode"]

    #User.query.filter_by(email=email)
       # print "This mail already exists."

    user = User(email=email, password=password, age=age, zipcode=zipcode)
    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.route("/login")
def login_form():
    """Show login form"""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_process():
    """Processes login form"""
    print "enter the login_process"
    email = request.form["email"]
    print "reached the email"
    password = request.form["password"]
    print "reached the password"

    db_email = User.query.filter_by(email=email).first()


    if not db_email:
        return redirect("/register")
    else:
        user_email = db_email.email
        if password == db_email.password:

            session['user_id'] = db_email.user_id

            flash('You were successfully logged in.')
            return redirect("/")

@app.route("/logout")
def logout_form():
    """Show login form"""
    del session["user_id"]
    flash('You were successfully logged out.')
    return redirect("/")







if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    app.config['SQLALCHEMY_ECHO'] = True
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
