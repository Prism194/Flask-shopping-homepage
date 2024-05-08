import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

app = Flask(__name__)
app.debug = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///info.db")

@app.route('/')
def home():
  # You can add logic for your homepage here if needed
  # database -> image, product name, price
  return render_template('index.html')  # Assuming you have an index.html

@app.route('/about')
def about():
  # You can pass data to product1.html if needed using variables here
  return render_template('about.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        product_name = request.form.get("product_name")
        quantity = request.form.get("quantity")
        price = request.form.get("price")
        db.execute("INSERT INTO products (productname, quantity, price) VALUES(?, ?, ?)", product_name, quantity, price)
        return redirect("/")
    else:
        return render_template("add.html")
    
@app.route('/product1')
def product1():
  # You can pass data to product1.html if needed using variables here
  return render_template('product1.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("Please input your username")
        check = db.execute("SELECT username FROM users WHERE username == ?", username)
        if check:
            return apology("Your username is redundant")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password:
            return apology("Please input your password")
        if password != confirmation:
            return apology("Your password is not identical with confirmation")
        hash = generate_password_hash(password, method='pbkdf2', salt_length=16)
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")   

if __name__ == '__main__':
    app.run()