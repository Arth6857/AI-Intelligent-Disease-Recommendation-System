from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import pandas as pd
import os

app = Flask(__name__)

# =========================
# CONFIG
# =========================
app.config["SECRET_KEY"] = "change-this-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "change-this-jwt-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# =========================
# DATABASE MODEL
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

# =========================
# LOAD DATASETS
# =========================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

precautions_df = pd.read_csv(os.path.join(BASE_DIR, "dataset/precautions_df.csv"))
workout_df = pd.read_csv(os.path.join(BASE_DIR, "dataset/workout_df.csv"))
description_df = pd.read_csv(os.path.join(BASE_DIR, "dataset/description.csv"))
medications_df = pd.read_csv(os.path.join(BASE_DIR, "dataset/medications.csv"))
diets_df = pd.read_csv(os.path.join(BASE_DIR, "dataset/diets.csv"))

# =========================
# HELPER FUNCTION
# =========================
def get_demo_data(disease):
    desc = description_df[description_df["Disease"] == disease]["Description"].values
    desc = desc[0] if len(desc) > 0 else "No description available."

    precautions = precautions_df[
        precautions_df["Disease"] == disease
    ].iloc[:, 1:].values.flatten().tolist()

    medications = medications_df[
        medications_df["Disease"] == disease
    ]["Medication"].tolist()

    diet = diets_df[diets_df["Disease"] == disease]["Diet"].tolist()

    workout = workout_df[
        workout_df["disease"] == disease
    ]["workout"].tolist()

    return desc, precautions, medications, diet, workout

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return redirect(url_for("login"))

# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").strip()
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()

        if not username or not email or not password:
            flash("Please fill all fields.")
            return redirect(url_for("register"))

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash("Username or Email already exists.")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_or_email = request.form.get("username").strip()
        password = request.form.get("password").strip()

        user = User.query.filter(
            (User.username == username_or_email) |
            (User.email == username_or_email)
        ).first()

        if user and check_password_hash(user.password, password):
            session["user"] = user.username
            flash("Login successful.")
            return redirect(url_for("dashboard"))

        flash("Invalid username/email or password.")
        return redirect(url_for("login"))

    return render_template("login.html")

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("login"))

# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("index.html", name=session["user"])

# ---------- WEBSITE PREDICT ----------
@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return redirect(url_for("login"))

    current_user = session["user"]

    age = request.form.get("age")
    location = request.form.get("location")
    symptoms = request.form.get("symptoms")

    if not symptoms:
        flash("Please enter symptoms.")
        return redirect(url_for("dashboard"))

    predicted_disease = "Heart attack"   # Replace with ML model

    desc, precautions, medications, diet, workout = get_demo_data(predicted_disease)

    return render_template(
        "index.html",
        name=current_user,
        age=age,
        location=location,
        symptoms=symptoms,
        predicted_disease=predicted_disease,
        dis_des=desc,
        my_precautions=precautions[:4],
        medications=medications,
        my_diet=diet,
        workout=workout
    )

# =========================
# JWT API ROUTES
# =========================

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()

    username_or_email = data.get("username")
    password = data.get("password")

    user = User.query.filter(
        (User.username == username_or_email) |
        (User.email == username_or_email)
    ).first()

    if user and check_password_hash(user.password, password):
        token = create_access_token(identity=user.username)
        return jsonify({"access_token": token}), 200

    return jsonify({"message": "Invalid credentials"}), 401


@app.route("/api/predict", methods=["POST"])
@jwt_required()
def api_predict():
    current_user = get_jwt_identity()
    data = request.get_json()
    symptoms = data.get("symptoms", "")

    if not symptoms:
        return jsonify({"message": "Please enter symptoms"}), 400

    predicted_disease = "Heart attack"

    desc, precautions, medications, diet, workout = get_demo_data(predicted_disease)

    return jsonify({
        "user": current_user,
        "symptoms": symptoms,
        "predicted_disease": predicted_disease,
        "description": desc,
        "precautions": precautions[:4],
        "medications": medications,
        "diet": diet,
        "workout": workout
    })

# ---------- OTHER PAGES ----------
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/developer")
def developer():
    return render_template("developer.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app.run(debug=True)