# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)


app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:9596@localhost/mydatabase'
app.config['UPLOAD_FOLDER'] = 'UPLOAD_FOLDER2/'
app.config['STATIC_FOLDER'] = 'static/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SECRET_KEY'] = 'your_secret_key'  # Required for session management
db = SQLAlchemy(app)

class Submissions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    blog = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255))
    video = db.Column(db.String(255))
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# Create connection to MySQL database
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="9596",
    database="myDatabase",
    cursorclass=pymysql.cursors.DictCursor
)
with connection.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INT AUTO_INCREMENT PRIMARY KEY,
            feedback TEXT
        )
    """)
    connection.commit()

# Serve HTML files
# Serve HTML files
@app.route("/")
def home():
    # Fetch submissions from the database
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM submissions")
        submissions = cursor.fetchall()

    return render_template("front.html", submissions=submissions)


@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/register.html")
def register():
    return render_template("register.html")

@app.route("/certified.html")
def certified():
    return render_template("certified.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/service.html")
def service():
    return render_template("service.html")

@app.route("/pickup.html")
def pickup():
    return render_template("pickup.html")

@app.route("/feedback.html")
def feedback():
    return render_template("feedback.html")

@app.route("/front.html")
def front():
    return render_template("front.html")
@app.route("/admin")
def admin():
    # Fetch data from the takepickup table
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM takepickup")
        takepickups = cursor.fetchall()

    # Fetch data from the product table
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()

    # Render the admin.html template with the fetched data
    return render_template("admin.html", takepickups=takepickups, products=products)

@app.route("/educate.html")
def educate():
    return render_template("educate.html")

@app.route("/waste.html")
def waste():
    return render_template("waste.html")

# Handle form submissions
@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        blog = request.form["blog"]
        image = request.form["image"]
        video = request.form["video"]

        with connection.cursor() as cursor:
            sql = "INSERT INTO submissions (blog, image, video) VALUES (%s, %s, %s)"
            cursor.execute(sql, (blog, image, video))
            connection.commit()

        return "Thank you for your contribution!"
@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    if request.method == "POST":
        feedback = request.form.get("feedback", "")

        # Here you can process the feedback, store it in the database, etc.
        # For now, let's just print it
        print("Feedback received:", feedback)

        # Redirect the user to a thank you page or any other appropriate action
        return redirect(url_for("thank_you"))
@app.route("/thank_you")
def thank_you():
    return render_template("service.html")

@app.route("/submit-certificate", methods=["POST"])
def submit_certificate():
    if request.method == "POST":
        FullName = request.form["FullName"]
        mobileNumber = request.form["mobileNumber"]
        address = request.form["address"]

        with connection.cursor() as cursor:
            sql = "INSERT INTO certificates (FullName, mobileNumber, address) VALUES (%s, %s, %s)"
            cursor.execute(sql, (FullName, mobileNumber, address))
            connection.commit()

        return "Thank you for submitting your certificate request!"

@app.route("/takepickup", methods=["POST"])
def takepickup():
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")
        waste_type = request.form.get("waste_type", "")
        date_pickup = request.form.get("date_pickup", "")
        time_pickup = request.form.get("time_pickup", "")
        address_pickup = request.form.get("address_pickup", "")

        with connection.cursor() as cursor:
            sql = "INSERT INTO takepickup (name, email, phone, waste_type, date_pickup, time_pickup, address_pickup) VALUES (%s, %s, %s, %s,  %s, %s, %s)"
            cursor.execute(sql, (name, email, phone, waste_type, date_pickup, time_pickup, address_pickup))
            connection.commit()

        feedback_message = "Thank you for scheduling a pickup! We'll be in touch soon."
        return render_template("feedback.html", message=feedback_message)

# Handle login form submission
# Route to handle user login
@app.route("/login", methods=["POST"])
def login_user():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Users WHERE username=%s AND email=%s AND password=%s"
            cursor.execute(sql, (username, email, password))
            user = cursor.fetchone()
            if user:
                session["user_role"] = user["role"]  # Storing user role in session
                if user["role"] == "user":
                    return redirect(url_for("front"))
                elif user["role"] == "admin":
                    return redirect(url_for("admin"))
            else:
                return redirect("/login.html?error=No+user+exists")

# Route to handle form submission from educate.html
# Handle form submissions
@app.route("/submit", methods=["POST"])
def submit_form():
    if request.method == "POST":
        blog = request.form["blog"]
        image = request.files["image"]
        video = request.form["video"]

        if image:
            filename = secure_filename(image.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(save_path)
            image_path = os.path.join(request.base_url, app.config['UPLOAD_FOLDER'][1:], filename)
        else:
            image_path = ""

        with connection.cursor() as cursor:
            sql = "INSERT INTO submissions (blog, image, video) VALUES (%s, %s, %s)"
            cursor.execute(sql, (blog, image_path, video))
            connection.commit()

        return "Thank you for your contribution!"@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER2'], filename)



# Handle register form submission
@app.route("/register", methods=["POST"])
def register_user():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]
        username = request.form.get("username")  # Use .get() to handle if username is not submitted
        join_as = request.form.get("adminType")
        

        with connection.cursor() as cursor:
            check_sql = "SELECT * FROM Users WHERE username = %s OR email = %s"
            cursor.execute(check_sql, (username, email))
            existing_user = cursor.fetchone()

            if existing_user:
                if existing_user["username"] == username:
                    return redirect("/register.html?error=Username+is+already+taken")
                else:
                    return redirect("/register.html?error=Email+is+already+registered")
            else:
                sql = "INSERT INTO Users (name, email, username, password, role, join_as) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, email, username, password, role, join_as))
                connection.commit()
                return redirect("/login.html")



# Start the server
if __name__ == "__main__":
    app.run(port=5500, debug=True)
