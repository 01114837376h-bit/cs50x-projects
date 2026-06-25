import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db = SQL(f"sqlite:///{os.path.join(BASE_DIR, 'finance.db')}")

# Initialize required tables safely at startup
db.execute("""
    CREATE TABLE IF NOT EXISTS portfolio (
        user_id INTEGER, 
        symbol TEXT, 
        shares INTEGER
    )
""")
db.execute("""
    CREATE TABLE IF NOT EXISTS history (
        user_id INTEGER, 
        symbol TEXT, 
        shares INTEGER, 
        price NUMERIC, 
        transacted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Get user's current cash
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    
    # Get user's stock groupings
    portfolio_db = db.execute("SELECT symbol, SUM(shares) as total_shares FROM portfolio WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", session["user_id"])
    
    portfolio = []
    grand_total = user_cash

    # Build the portfolio with LIVE prices
    for row in portfolio_db:
        stock = lookup(row["symbol"])
        total_value = stock["price"] * row["total_shares"]
        grand_total += total_value
        
        portfolio.append({
            "symbol": stock["symbol"],
            "name": stock["name"],
            "shares": row["total_shares"],
            "price": stock["price"],  # Unformatted for template logic, or format here if needed
            "total": total_value
        })

    return render_template("index.html", portfolio=portfolio, cash=user_cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("shares must be a positive integer", 400)

        shares = int(shares)
        stock = lookup(symbol)
        
        if stock is None:
            return apology("invalid symbol", 400)

        # Get user's cash balance
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        total_cost = stock["price"] * shares

        if user_cash < total_cost:
            return apology("can't afford", 400)

        # Execute transaction
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, session["user_id"])
        
        # Update portfolio
        db.execute("INSERT INTO portfolio (user_id, symbol, shares) VALUES (?, ?, ?)", 
                   session["user_id"], stock["symbol"], shares)
        
        # Update history (Positive shares for buy)
        db.execute("INSERT INTO history (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], stock["symbol"], shares, stock["price"])

        flash("Bought!")
        return redirect("/")
    
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    try:
        rows = db.execute("SELECT symbol, shares, price, transacted FROM history WHERE user_id = ? ORDER BY transacted DESC", session["user_id"])
    except Exception as e:
        rows = []
    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol", 400)

        quote = db.execute(
            "SELECT * FROM stocks WHERE symbol = ?",
            symbol.upper()
        )

        if len(quote) == 0:
            return apology("invalid symbol", 400)

        quote = quote[0]

        return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        usern = request.form.get("username")
        passw = request.form.get("password")
        passw2 = request.form.get("confirmation")

        if not usern:
            return apology("must provide username", 400)
        elif not passw:
            return apology("must provide password", 400)
        elif not passw2:
            return apology("must provide password confirmation", 400)
        elif passw != passw2:
            return apology("passwords do not match", 400)

        hash_pw = generate_password_hash(passw)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", usern, hash_pw)
            session["user_id"] = db.execute("SELECT id FROM users WHERE username = ?", usern)[0]["id"]
            flash("Registered successfully!")
            return redirect("/")
        except:
            return apology("username already exists", 400)
        
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("shares must be a positive integer", 400)

        shares = int(shares)

        # Check how many shares the user actually owns
        owned_query = db.execute("SELECT SUM(shares) as total_shares FROM portfolio WHERE user_id = ? AND symbol = ? GROUP BY symbol", 
                                 session["user_id"], symbol)
        
        if len(owned_query) == 0 or owned_query[0]["total_shares"] < shares:
            return apology("you don't have enough shares", 400)

        stock = lookup(symbol)
        sale_value = stock["price"] * shares

        # Update user's cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", sale_value, session["user_id"])

        # Update portfolio (Insert negative shares to offset)
        db.execute("INSERT INTO portfolio (user_id, symbol, shares) VALUES (?, ?, ?)", 
                   session["user_id"], symbol, -shares)

        # Update history (Negative shares for sell)
        db.execute("INSERT INTO history (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], symbol, -shares, stock["price"])

        flash("Sold!")
        return redirect("/")

    else:
        # Populate dropdown with stocks the user currently owns
        portfolio = db.execute("SELECT symbol FROM portfolio WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
        return render_template("sell.html", stocks=portfolio)


if __name__ == "__main__":
    app.run(debug=False)