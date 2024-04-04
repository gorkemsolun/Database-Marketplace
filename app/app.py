import re
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.secret_key = "abcdefgh"

app.config["MYSQL_HOST"] = "db"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "cs353hw4db"

mysql = MySQL(app)


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM customer WHERE name = % s AND cid = % s",
            (
                username,
                password,
            ),
        )
        user = cursor.fetchone()
        if user:
            session["loggedin"] = True
            session["userid"] = user["cid"]
            session["username"] = user["name"]
            message = "Logged in successfully!"
            return redirect(url_for("main"))
        else:
            message = "Please enter correct email / password !"
    return render_template("login.html", message=message)


@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM customer WHERE name = % s", (username,))
        account = cursor.fetchone()
        cursor.execute("SELECT * FROM customer WHERE cid = % s", (password,))
        accountPassword = cursor.fetchone()
        if account:
            message = "Choose a different username!"

        elif accountPassword:
            message = "Choose a different password(cid)!"

        elif len(password) != 5:
            message = "Password must be 5 characters!"

        elif not username or not password:
            message = "Please fill out the form!"

        else:
            cursor.execute(
                "INSERT INTO customer (cid, name) VALUES (% s, % s)",
                (password, username),
            )
            mysql.connection.commit()
            message = "User successfully created!"

    elif request.method == "POST":

        message = "Please fill all the fields!"
    return render_template("register.html", message=message)


@app.route("/main")
def main():
    if session["loggedin"]:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT account.aid, branch, balance, openDate, city FROM account, owns WHERE owns.aid = account.aid AND cid = %s",
            [session["userid"]],
        )
        accounts = cursor.fetchall()
        return render_template(
            "main.html", accounts=accounts, username=session["username"]
        )
    return render_template("login.html")


@app.route("/moneyTransfer")
def moneyTransfer():

    if session["loggedin"]:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT account.aid, branch, balance, openDate, city FROM account, owns WHERE owns.aid = account.aid AND cid = %s",
            [session["userid"]],
        )
        userAccounts = cursor.fetchall()
        cursor.execute("SELECT * FROM account")
        allAccounts = cursor.fetchall()
        return render_template(
            "moneyTransfer.html",
            userAccounts=userAccounts,
            allAccounts=allAccounts,
        )

    return render_template("login.html")


@app.route("/moneyTransferProcess", methods=["GET", "POST"])
def moneyTransferProcess():
    fromAid = request.form["fromAccountId"]
    toAid = request.form["toAccountId"]
    amount = float(request.form["amount"])
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "SELECT account.aid, branch, balance, openDate, city FROM account, owns WHERE owns.aid = account.aid AND cid = %s AND account.aid = %s",
        [session["userid"], fromAid],
    )
    fromAccount = cursor.fetchone()

    if fromAccount is None:
        return render_template(
            "message.html",
            message="There is no account associated with that ID. Please go back and try again with a valid account ID that belongs to you.",
            isPositive=False,
        )

    cursor.execute(
        "SELECT aid, branch, balance, openDate, city FROM account WHERE aid = %s",
        [toAid],
    )
    toAccount = cursor.fetchone()
    if toAccount is None:
        return render_template(
            "message.html",
            message="There is no account associated with that ID. Please go back and try again with a valid account ID.",
            isPositive=False,
        )

    if fromAid == toAid:
        return render_template(
            "message.html",
            message="You cannot transfer money to the same account. Please go back and try again with a different account ID.",
            isPositive=False,
        )

    if fromAccount["balance"] < amount:
        return render_template(
            "message.html",
            message="You do not have enough balance to make this transfer. Please go back and try again with a lower amount.",
            isPositive=False,
        )

    cursor.execute(
        "UPDATE account SET balance = balance - %s WHERE aid = %s", [amount, fromAid]
    )
    cursor.execute(
        "UPDATE account SET balance = balance + %s WHERE aid = %s", [amount, toAid]
    )
    mysql.connection.commit()

    return render_template(
        "message.html",
        message="You have successfully transferred $ %s from account %s to account %s."
        % (amount, fromAid, toAid),
        isPositive=True,
    )


@app.route("/closeAccount/<aid>", methods=["GET", "POST"])
def closeAccount(aid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM owns WHERE aid = %s", [aid])
    cursor.execute("DELETE FROM account WHERE aid = %s", [aid])
    mysql.connection.commit()
    return render_template(
        "message.html",
        message="You have successfully closed the account with ID %s." % aid,
        isPositive=True,
    )


@app.route("/accountSummary")
def accountSummary():

    if session["loggedin"]:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT account.aid, account.branch, account.balance, account.openDate FROM owns JOIN account ON owns.aid = account.aid WHERE owns.cid = %s ORDER BY account.openDate ASC;",
            [session["userid"]],
        )
        dateOrderQuery = cursor.fetchall()
        cursor.execute(
            "SELECT account.aid, account.balance, account.openDate FROM owns JOIN account ON owns.aid = account.aid WHERE owns.cid = %s AND account.openDate > '2015-12-31' AND account.balance > 50000;",
            [session["userid"]],
        )
        dateAfterHighBalanceQuery = cursor.fetchall()
        cursor.execute(
            "SELECT account.aid, account.balance FROM owns JOIN account ON owns.aid = account.aid JOIN customer ON owns.cid = customer.cid WHERE owns.cid = %s AND account.city = customer.city;",
            [session["userid"]],
        )
        sameCityQuery = cursor.fetchall()
        cursor.execute(
            "SELECT MIN(account.balance) AS minBalance, MAX(account.balance) AS maxBalance FROM owns JOIN account ON owns.aid = account.aid WHERE owns.cid = %s;",
            [session["userid"]],
        )
        minMaxQuery = cursor.fetchall()
        return render_template(
            "accountSummary.html",
            dateOrderQuery=dateOrderQuery,
            dateAfterHighBalanceQuery=dateAfterHighBalanceQuery,
            sameCityQuery=sameCityQuery,
            minMaxQuery=minMaxQuery,
        )

    return render_template("login.html")


@app.route("/logout")
def logout():
    session["loggedin"] = False
    session["userid"] = None
    session["username"] = None
    return render_template("login.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
