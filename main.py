from flask import Flask, redirect, url_for, render_template, request, flash
import mysql.connector


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


def db_create():
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Daniel004989",
        database = "instagram_users"
    )
    return db
    

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("ig_login_index.html")
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = db_create()
        if db.is_connected():
            cursor = db.cursor()
            cursor.execute("SELECT * FROM `User` WHERE `email` = %s", (email, ))
            data = cursor.fetchone()
            if data:
                if password == data[3] :
                    return render_template("profile.html")
                else:
                    flash('Incorrect email or password.', category='error')
                    return render_template("ig_login_index.html")
        else:
            flash('Database connection failed.', category='error')
            return render_template("ig_login_index.html")


    

@app.route("/signup", methods=['GET', 'POST'])
def signup():    
    if request.method == 'GET':
        return render_template("ig_signup_index.html")
    
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_name = request.form['user_name']

        db = db_create()

        cursor = db.cursor()
        cursor.execute("SELECT * FROM `User` WHERE `email` = %s", (email,))
        data = cursor.fetchone()
        if data:
            flash('Email already exists.', category='error')
        elif len(user_name) < 2:
            flash('User name must be at least 2 characters long.', category='error')    
        elif len(password) < 5:
            flash('Password must be at least 5 characters long.', category='error')
        else:
            cursor.execute("INSERT INTO `User` (`email`, `user_name`, `password`) VALUES (%s, %s, %s)",(email, user_name, password))
            db.commit()
            cursor.close()
            db.close()
            flash('Account created successfully.', category='success')
            return redirect(url_for("login"))

        cursor.close()
        db.close()
        return render_template("ig_signup_index.html")


@app.route("/homepage")
def homepage():
    return render_template("profile.html")

class Users:
    def __init__(self, id, mail, user_name, password) :
        self.id = id
        self.mail = mail
        self.user_name = user_name
        self.password = password


if __name__ ==  "__main__":
    app.run(debug=True)  