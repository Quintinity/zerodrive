from flask import Flask, session, redirect, url_for

app = Flask("zerodrive")

@app.route("/")
def root():
    if "logged_in" in session:
        return "You are logged in"
    return "You are not logged in."

@app.route("/login")
def login():
    if "logged_in" in session:
        return redirect(url_for("index"))
    session["logged_in"] = True
    return "You are now logged in"

if __name__ == "__main__":
    app.run()
