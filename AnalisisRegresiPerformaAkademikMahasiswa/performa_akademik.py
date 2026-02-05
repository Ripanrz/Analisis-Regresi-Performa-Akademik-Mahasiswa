from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)

# Load Model Terbaik yang sudah disimpan
try:
    with open('regression_final_best_model.pkl', 'rb') as f:
        model = pickle.load(f)
except:
    model = None
    print("⚠️ Warning: File 'regression_final_best_model.pkl' belum ada. Pastikan sudah di-upload/generate.")

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    input_data = {}
    
    if request.method == 'POST' and model:
        # Ambil data dari Form HTML
        try:
            features = [
                float(request.form['study_hours']),
                float(request.form['social_media_hours']),
                float(request.form['mental_health']), # Rating 1-10
                float(request.form['sleep_hours']),
                float(request.form['exercise_frequency']),
                float(request.form['netflix_hours'])
            ]
            
            # Buat DataFrame agar nama kolom sesuai dengan model (Mencegah warning)
            feature_names = [
                'study_hours_per_day', 'social_media_hours', 'mental_health_rating',
                'sleep_hours', 'exercise_frequency', 'netflix_hours'
            ]
            
            df_input = pd.DataFrame([features], columns=feature_names)
            
            # Prediksi
            pred_score = model.predict(df_input)[0]
            
            # Batasi nilai agar logis (0 - 100)
            pred_score = max(0, min(100, pred_score))
            
            prediction = round(pred_score, 2)
            input_data = request.form # Simpan input biar gak ilang setelah reload
            
        except Exception as e:
            print(f"Error: {e}")

    return render_template('index.html', prediction=prediction, input_data=input_data)

if __name__ == '__main__':
    app.run(debug=True)