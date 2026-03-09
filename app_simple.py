from flask import Flask, render_template, request, redirect, url_for, flash
import os
import csv
from datetime import datetime
import json
import uuid

app = Flask(__name__)
app.secret_key = 'organage-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def read_csv_file(filepath):
    """Read CSV file and return list of dictionaries"""
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except UnicodeDecodeError:
        # Try with ISO-8859-1 encoding if UTF-8 fails
        with open(filepath, 'r', encoding='ISO-8859-1') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    return data

def safe_float(value, default=0.0):
    """Safely convert value to float"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_int(value, default=0):
    """Safely convert value to int"""
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default

@app.route('/')
def index():
    return render_template('intake.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        # Check required files
        if 'results_file' not in request.files or 'contributions_file' not in request.files:
            flash('Results and Contributions files are required', 'error')
            return redirect(url_for('index'))
        
        # Create session folder
        session_id = str(uuid.uuid4())[:8]
        patient_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        os.makedirs(patient_folder, exist_ok=True)
        
        # Save uploaded files
        for field_name, filename in [('results_file', 'results.csv'),
                                      ('contributions_file', 'contributions.csv'),
                                      ('food_file', 'food.csv'),
                                      ('suppl_file', 'suppl.csv'),
                                      ('exer_file', 'exer.csv')]:
            if field_name in request.files:
                file = request.files[field_name]
                if file and file.filename:
                    filepath = os.path.join(patient_folder, filename)
                    file.save(filepath)
        
        # Save metadata
        metadata = {
            'upload_time': datetime.now().isoformat(),
            'session_id': session_id
        }
        with open(os.path.join(patient_folder, 'metadata.txt'), 'w') as f:
            json.dump(metadata, f)
        
        return redirect(url_for('view_report', session_id=session_id))
    
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/report/<session_id>')
def view_report(session_id):
    try:
        patient_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        
        # Read results CSV
        results_file = os.path.join(patient_folder, 'results.csv')
        results_data = read_csv_file(results_file)
        
        if not results_data:
            flash('No data found in results file', 'error')
            return redirect(url_for('index'))
        
        # Get patient info from first row
        first_row = results_data[0]
        patient_name = first_row.get('name', 'Patient')
        patient_dob = first_row.get('dob', '')
        report_date = datetime.now().strftime('%B %d, %Y')
        
        # Calculate ages
        chronological_age = safe_int(first_row.get('chronological_age', 0))
        systemic_age = safe_int(first_row.get('systemic_age', 0))
        systemic_delta = systemic_age - chronological_age
        
        # Read contributions CSV
        contributions_file = os.path.join(patient_folder, 'contributions.csv')
        contributions_data = read_csv_file(contributions_file)
        
        # Process organ systems data
        organs_data = []
        organ_systems = ['Nervous', 'Mental', 'Circulatory', 'Respiratory', 
                        'Metabolic', 'Digestive', 'Musculoskeletal', 'Infectious', 'Genitourinary']
        
        for system in organ_systems:
            system_lower = system.lower()
            age_key = f'{system_lower}_age'
            
            age = safe_int(first_row.get(age_key, chronological_age))
            delta = age - chronological_age
            
            organs_data.append({
                'system': system,
                'age': age,
                'delta': delta,
                'delta_color': 'red' if delta > 0 else ('green' if delta < 0 else 'neutral')
            })
        
        # Find primary driver and contributors
        sorted_organs = sorted(organs_data, key=lambda x: abs(x['delta']), reverse=True)
        primary_driver = sorted_organs[0]['system'] if sorted_organs else 'N/A'
        secondary_contributors = [org['system'] for org in sorted_organs[1:4]] if len(sorted_organs) > 1 else []
        most_resilient = min(organs_data, key=lambda x: x['delta'])['system'] if organs_data else 'N/A'
        
        # Process recommendations
        food_recs = {'recommend': [], 'avoid': []}
        suppl_recs = {'recommend': [], 'avoid': []}
        exer_recs = []
        
        # Food recommendations
        food_file = os.path.join(patient_folder, 'food.csv')
        if os.path.exists(food_file):
            food_data = read_csv_file(food_file)
            # Sort by food_score
            food_data_sorted = sorted(food_data, key=lambda x: safe_float(x.get('food_score', 0)), reverse=True)
            for item in food_data_sorted[:10]:
                rec_group = item.get('food_rec_group', 'recommend')
                if rec_group == 'recommend' and len(food_recs['recommend']) < 5:
                    food_recs['recommend'].append(item)
                elif rec_group == 'avoid' and len(food_recs['avoid']) < 5:
                    food_recs['avoid'].append(item)
        
        # Supplement recommendations
        suppl_file = os.path.join(patient_folder, 'suppl.csv')
        if os.path.exists(suppl_file):
            suppl_data = read_csv_file(suppl_file)
            suppl_data_sorted = sorted(suppl_data, key=lambda x: safe_float(x.get('suppl_score', 0)), reverse=True)
            for item in suppl_data_sorted[:8]:
                rec_group = item.get('suppl_rec_group', 'recommend')
                if rec_group == 'recommend' and len(suppl_recs['recommend']) < 4:
                    suppl_recs['recommend'].append(item)
                elif rec_group == 'avoid' and len(suppl_recs['avoid']) < 4:
                    suppl_recs['avoid'].append(item)
        
        # Exercise recommendations
        exer_file = os.path.join(patient_folder, 'exer.csv')
        if os.path.exists(exer_file):
            exer_data = read_csv_file(exer_file)
            exer_data_sorted = sorted(exer_data, key=lambda x: safe_float(x.get('exercise_score', 0)), reverse=True)
            exer_recs = exer_data_sorted[:6]
        
        # Biomarkers for force graphs
        biomarkers_data = []
        protective_data = []
        
        if contributions_data:
            for item in contributions_data:
                contrib = safe_float(item.get('contribution', 0))
                if contrib > 0:
                    biomarkers_data.append({
                        'biomarker': item.get('biomarker', ''),
                        'contribution': contrib
                    })
                elif contrib < 0:
                    protective_data.append({
                        'biomarker': item.get('biomarker', ''),
                        'contribution': abs(contrib)
                    })
        
        # Sort and get top 5
        biomarkers_data = sorted(biomarkers_data, key=lambda x: x['contribution'], reverse=True)[:5]
        protective_data = sorted(protective_data, key=lambda x: x['contribution'], reverse=True)[:5]
        
        return render_template('report.html',
                             patient_name=patient_name,
                             patient_dob=patient_dob,
                             report_date=report_date,
                             chronological_age=chronological_age,
                             systemic_age=systemic_age,
                             systemic_delta=systemic_delta,
                             organs_data=organs_data,
                             primary_driver=primary_driver,
                             secondary_contributors=secondary_contributors,
                             most_resilient=most_resilient,
                             df_results=results_data,
                             df_contributions=contributions_data,
                             food_recs=food_recs,
                             suppl_recs=suppl_recs,
                             exer_recs=exer_recs,
                             biomarkers_data=biomarkers_data,
                             protective_data=protective_data)
        
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
