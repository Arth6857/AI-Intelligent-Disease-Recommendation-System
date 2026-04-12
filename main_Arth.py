from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'change-this-secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

# Load datasets
precautions_df = pd.read_csv('dataset/precautions_df.csv')
workout_df = pd.read_csv('dataset/workout_df.csv')
description_df = pd.read_csv('dataset/description.csv')
medications_df = pd.read_csv('dataset/medications.csv')
diets_df = pd.read_csv('dataset/diets.csv')

def get_demo_data(disease):
    desc = description_df[description_df['Disease']==disease]['Description']
    desc = desc.iloc[0] if not desc.empty else 'No description available.'
    precautions = precautions_df[precautions_df['Disease']==disease].iloc[:,1:].values.flatten().tolist()
    medications = medications_df[medications_df['Disease']==disease]['Medication'].tolist()
    diet = diets_df[diets_df['Disease']==disease]['Diet'].tolist()
    workout = workout_df[workout_df['disease']==disease]['workout'].tolist()
    return desc, precautions, medications, diet, workout

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'msg':'User already exists'}), 400
    user = User(username=data['username'], password=generate_password_hash(data['password']))
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg':'Registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'msg':'Invalid credentials'}), 401
    token = create_access_token(identity=user.username)
    return jsonify(access_token=token)

@app.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    current_user = get_jwt_identity()
    symptoms = request.json.get('symptoms','')
    disease = 'Heart attack'
    desc, precautions, medications, diet, workout = get_demo_data(disease)
    return jsonify({
        'user': current_user,
        'symptoms': symptoms,
        'predicted_disease': disease,
        'description': desc,
        'precautions': precautions[:4],
        'medications': medications,
        'diet': diet,
        'workout': workout
    })

if __name__ == '__main__':
    app.run(debug=True)