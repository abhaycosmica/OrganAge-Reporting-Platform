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
        
        # Read results CSV (format: System,RawIndex,Age,DiseaseAge,DeltaAge)
        results_file = os.path.join(patient_folder, 'results.csv')
        results_data = read_csv_file(results_file)
        
        if not results_data:
            flash('No data found in results file', 'error')
            return redirect(url_for('index'))
        
        # Patient info - use defaults since CSV doesn't have this
        patient_name = 'Patient'
        patient_dob = ''
        report_date = datetime.now().strftime('%B %d, %Y')
        
        # Calculate ages from the data
        # First, find if there's a Systemic row
        systemic_row = None
        for row in results_data:
            if row.get('System', '') == 'Systemic':
                systemic_row = row
                break
        
        chronological_age = safe_int(results_data[0].get('Age', 68))
        
        # Build organs_data from the CSV rows (excluding Systemic)
        organs_data = []
        
        for row in results_data:
            system = row.get('System', '')
            if system and system != 'Systemic':
                age = safe_int(row.get('DiseaseAge', chronological_age))
                delta = safe_float(row.get('DeltaAge', 0))
                
                organs_data.append({
                    'system': system,
                    'age': age,
                    'delta': delta,
                    'delta_color': 'red' if delta > 0 else ('green' if delta < 0 else 'neutral')
                })
        
        # Calculate systemic age - use Systemic row if available, otherwise average
        if systemic_row:
            systemic_age = safe_int(systemic_row.get('DiseaseAge', chronological_age))
        elif organs_data:
            systemic_age = int(sum(org['age'] for org in organs_data) / len(organs_data))
        else:
            systemic_age = chronological_age
        
        systemic_delta = systemic_age - chronological_age
        
        # Find primary driver and contributors
        sorted_organs = sorted(organs_data, key=lambda x: abs(x['delta']), reverse=True)
        primary_driver = sorted_organs[0]['system'] if sorted_organs else 'N/A'
        secondary_contributors = [org['system'] for org in sorted_organs[1:4]] if len(sorted_organs) > 1 else []
        
        # Most resilient is the one with most negative delta (aging slowest)
        most_resilient_org = min(organs_data, key=lambda x: x['delta']) if organs_data else None
        most_resilient = [most_resilient_org['system']] if most_resilient_org else []
        
        # Read contributions CSV (format: System,Biomarker,Contribution)
        contributions_file = os.path.join(patient_folder, 'contributions.csv')
        contributions_data = read_csv_file(contributions_file)
        
        # Process recommendations
        food_recs = {'recommend': [], 'avoid': []}
        suppl_recs = {'recommend': [], 'avoid': []}
        exer_recs = []
        
        # Food recommendations
        food_file = os.path.join(patient_folder, 'food.csv')
        if os.path.exists(food_file):
            food_data = read_csv_file(food_file)
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
        
        # Biomarkers for force graphs from contributions CSV
        biomarkers_data = []
        protective_data = []
        
        if contributions_data:
            for item in contributions_data:
                system = item.get('System', '')
                biomarker = item.get('Biomarker', '')
                contrib = safe_float(item.get('Contribution', 0))
                
                # Skip systemic entries, only use system-specific biomarkers
                if system != 'Systemic' and biomarker:
                    if contrib > 0:
                        biomarkers_data.append({
                            'biomarker': biomarker,
                            'contribution': contrib
                        })
                    elif contrib < 0:
                        protective_data.append({
                            'biomarker': biomarker,
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
