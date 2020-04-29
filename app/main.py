from flask import Flask, render_template, url_for, request, \
    redirect, session, jsonify
from flaskext.mysql import MySQL

from crypto import Encrypt
from date import Date
from events import get_data, generate_buzz, random_data
from countries import countries
import os

# Create the Flask application and other configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or \
                           "b'\xe3\xa3\xb0\xd6Q<\x144\xa2\xd5\xd0IN \xf4\\\x16\x1b\x1e\xf0\xe8\x92:\xd3'"

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'  # COMMENT - for test locally!
app.config['MYSQL_DATABASE_HOST'] = 'db'  # COMMENT - for test locally!
# app.config['MYSQL_DATABASE_PASSWORD'] = 'P@sWorD123'  # COMMENT - for test in docker!
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'  # COMMENT - for test in docker!
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'game'

mysql = MySQL()
mysql.init_app(app)
con = mysql.connect()
cursor = con.cursor()


@app.route("/")
def index():
    """ When the website loads, it will automatically be redirected
    to the login page.
    """
    if "user" in session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    """The route and the method for logging in, which uses both GET
    and POST."""
    if "user" in session:
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            cursor = mysql.get_db().cursor()
            username_input = request.form['username']
            password_input = request.form['password']

            cursor.execute('''SELECT * FROM admins WHERE username=%s''', username_input)

            if cursor.rowcount == 0:
                print('The username entered does not match' + 'any record in our database')
                return render_template('auth/login.html', title="BestApp", fail_login=True)
            else:
                results = cursor.fetchone()
                encrypted_real_password = results[2]
                crypt = Encrypt(password_input)
                length_input = len(password_input)
                word = ''

                # For loop runs through until length_input
                for i in range(0, length_input):
                    word = crypt.get_hashed_saltspot(i)
                    if word == encrypted_real_password:
                        session["user"] = username_input
                        return redirect(url_for('home'))
                return render_template('auth/login.html', title="BestApp", fail_login=True)
        else:
            return render_template('auth/login.html', title="BestApp", fail_login=False)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    """Sign up method"""
    if "user" in session:
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            username_input = request.form['username']
            username_confirm = request.form['confirm-username']
            password_input = request.form['password']
            password_confirm = request.form['confirm-password']

            if username_input == username_confirm:
                if password_input == password_confirm:
                    con = mysql.connect()
                    cursor = con.cursor()
                    cursor.execute('''SELECT * FROM admins WHERE username=%s''', username_input)
                    # This means that no username exists
                    if cursor.rowcount == 0:
                        date = Date()
                        date_today = date.todays_date()
                        crypto = Encrypt(password_input)
                        new_password = crypto.get_hashed_salt()
                        cursor.execute(
                            '''INSERT INTO admins (username, password, date_created) VALUES (%s, %s, %s)''',
                            (username_input, new_password, date_today))
                        # We have to commit in order for it to be actually
                        # sent to the database
                        con.commit()
                        return render_template('auth/signup.html', title="BestApp", success=True)
                    else:
                        # The username exists in the database
                        return render_template('auth/signup.html', title="BestApp", user_exists=True)
                else:
                    # Passwords the user entered do not match at all
                    return render_template('auth/signup.html', title="BestApp", match_error=True)
            else:
                # Username the user entered do not match at all
                return render_template('auth/signup.html', title="BestApp", match_error=True)
        else:
            return render_template('auth/signup.html', title="BestApp", match_error=False)


@app.route("/home")
def home():
    """Generate Pleyers Data"""
    if "user" in session:
        user = session["user"]
        return render_template('home.html', username=user)
    else:
        return redirect(url_for('login'))


@app.route("/_get_data/", methods=["POST"])
def _get_data():
    get_data = [generate_buzz() for _ in range(1)]
    return jsonify({
        "data": render_template("reports/gen_players.html", get_data=get_data)
    })


@app.route("/top_10")
def get_top_10():
    """Generate random Data"""

    if "user" in session:
        user = session["user"]
        event_data = [generate_buzz() for _ in range(10)]
        return render_template('reports/get_top_10.html', title="Top 10 | BestApp",
                               event_data=event_data, username=user)
    else:
        return redirect(url_for('login'))


@app.route("/top_100")
def get_top_100():
    """Generate random Data"""
    if "user" in session:
        user = session["user"]
        event_data = [generate_buzz() for _ in range(100)]
        return render_template('reports/get_top_100.html', title="Top 100 | BestApp",
                               event_data=event_data, username=user)
    else:
        return redirect(url_for('login'))


@app.route("/profile")
def profile():
    """Access the user's profile and stats"""
    if "user" in session:
        user = session["user"]
        geo_data = get_data()
        event_data = generate_buzz()

        return render_template('profile.html', title="My Profile | BestApp", username=user,
                               geo_data=geo_data, event_data=event_data)
    else:
        return redirect(url_for('login'))


@app.route("/lifetime_report")
def lifetime_report():
    """Lifetime report, all statistics"""
    if "user" in session:
        user = session["user"]
        date = Date()
        current_date = date.todays_date()
        total = random_data([x for x in range(9, 9999)], 1)
        total_players = random_data([x for x in range(59999, 99999)], 1)
        revenue = sum(random_data([x for x in range(9, 9999)], 12))
        sale = sum(random_data([x for x in range(9, 9999)], 12))
        event_data = [generate_buzz() for _ in range(5)]
        country = random_data(countries, 12)
        labels = [x.upper() for x in country]
        values = random_data([x for x in range(499, 14999)], 12)
        colors = [
            "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
            "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
            "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"
        ]

        return render_template('reports/lifetime_report.html', title="Lifetime Report | BestApp",
                               todays_date=current_date, username=user,
                               total=total, revenue=revenue, sale=sale,
                               max=17000, chart_=zip(values, labels, colors),
                               event_data=event_data, total_players=total_players)
    else:
        return redirect(url_for('login'))


@app.route("/logout")
def logout():
    """Logout, so that no one can access this url. It would be very hard to"""
    if "user" in session:
        session.pop("user", None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    """Handles error links"""
    return render_template('error/forbidden_access.html', title="404 Error | BestApp")


@app.errorhandler(500)
def server_error(e):
    """What the user sees when the server crashes for whatever reason"""
    return render_template('error/server_error.html', title="500 Server Error | BestApp")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
