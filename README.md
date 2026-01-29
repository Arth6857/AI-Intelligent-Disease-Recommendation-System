Disease Prediction and Medical Recommendation System 🩺
A machine learning-powered web application that predicts diseases based on user-entered symptoms and provides comprehensive health recommendations including medications, dietary suggestions, and exercise routines.

🎯 Features
Intelligent Disease Prediction: Uses Random Forest machine learning model with 100% accuracy
Symptom Spell Correction: Advanced fuzzy matching to correct misspelled symptoms
Comprehensive Health Recommendations:
Disease descriptions and information
Personalized medication suggestions
Dietary recommendations
Exercise and workout plans
Preventive precautions
User-Friendly Web Interface: Clean, responsive design with Bootstrap
Real-time Predictions: Instant results through Flask web application
🚀 Technologies Used
Backend: Python, Flask
Machine Learning: scikit-learn, Random Forest Classifier
Data Processing: pandas, numpy
Frontend: HTML, CSS, Bootstrap 5
Model Persistence: pickle
📊 Dataset Information
The system uses comprehensive medical datasets containing:

41 Diseases: Including common conditions like diabetes, hypertension, allergies, etc.
132 Symptoms: Comprehensive symptom database for accurate predictions
Medical Recommendations: Curated medications, diets, and workout plans for each disease
Dataset Files (located in dataset/):
Training.csv: Main training dataset with symptoms and disease labels
symptoms_df.csv: Symptom database with disease mappings
description.csv: Detailed disease descriptions
medications.csv: Medication recommendations for each disease
diets.csv: Dietary recommendations and nutrition plans
workout_df.csv: Exercise and workout suggestions
precautions_df.csv: Preventive measures and precautions
Symptom-severity.csv: Symptom severity classifications
🔧 Installation & Setup
Prerequisites
Python 3.7+
pip package manager
Installation Steps
Clone the repository:

git clone https://github.com/sohamvsonar/Disease-Prediction-and-Medical-Recommendation-System.git
cd Disease-Prediction-and-Medical-Recommendation-System
Install required dependencies:

pip install -r requirements.txt
Run the Flask application:

python main.py
Access the application: Open your web browser and navigate to:

http://localhost:5000
📱 Usage
Enter Symptoms: Type your symptoms separated by commas (e.g., "fever, headache, nausea")
Submit: Click the predict button to get your results
View Results: Get comprehensive information including:
Predicted disease
Disease description
Recommended medications
Dietary suggestions
Exercise plans
Preventive precautions
👥 Team Members
Soham Sonar
Tanmay Pramanick
Kunal Rajput
📸 Screenshots
![Uploading Screenshot 2026-01-30 at 1.40.51 AM.png…]()


🏗️ Project Structure
Disease-Prediction-and-Medical-Recommendation-System/
├── dataset/                    # Medical datasets
│   ├── Training.csv
│   ├── symptoms_df.csv
│   ├── description.csv
│   ├── medications.csv
│   ├── diets.csv
│   ├── workout_df.csv
│   ├── precautions_df.csv
│   └── Symptom-severity.csv
├── model/                      # Trained ML models
│   └── RandomForest.pkl
├── templates/                  # HTML templates
│   └── index.html
├── static/                     # Static assets
│   ├── bgCover.jpg
│   └── img.png
├── screenshots/                # Application screenshots
│   ├── ss1.jpg
│   ├── ss2.jpg
│   └── ss3.jpg
├── main.py                     # Flask web application
├── disease_prediction_system.ipynb  # Model training notebook
├── requirements.txt            # Python dependencies
└── README.md
⚠️ Disclaimer
This system is for educational and informational purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns.

=======
