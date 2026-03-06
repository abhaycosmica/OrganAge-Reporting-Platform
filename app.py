from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pandas as pd
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configuration
UPLOAD_FOLDER = 'uploads'
REPORTS_FOLDER = 'reports'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORTS_FOLDER'] = REPORTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Patient intake page"""
    return render_template('intake.html')

@app.route('/report/<patient_id>')
def view_report(patient_id):
    """Display the OrganAge report for a patient"""
    try:
        # Load patient data
        patient_folder = os.path.join(app.config['UPLOAD_FOLDER'], patient_id)
        
        if not os.path.exists(patient_folder):
            flash('Patient not found', 'error')
            return redirect(url_for('index'))
        
        # Read metadata
        metadata_path = os.path.join(patient_folder, 'metadata.txt')
        metadata = {}
        with open(metadata_path, 'r') as f:
            for line in f:
                if ':' in line:
                    key, value = line.strip().split(':', 1)
                    metadata[key.strip()] = value.strip()
        
        # Read CSV data
        results_path = os.path.join(patient_folder, 'results.csv')
        contributions_path = os.path.join(patient_folder, 'contributions.csv')
        food_path = os.path.join(patient_folder, 'food.csv')
        suppl_path = os.path.join(patient_folder, 'suppl.csv')
        exer_path = os.path.join(patient_folder, 'exer.csv')
        
        df_results = pd.read_csv(results_path)
        df_contributions = pd.read_csv(contributions_path)
        
        # Load recommendations (optional)
        food_recs = {'avoid': [], 'recommend': []}
        suppl_recs = {'avoid': [], 'recommend': []}
        exer_recs = []
        
        if os.path.exists(food_path):
            df_food = pd.read_csv(food_path, encoding='ISO-8859-1')
            # Get top recommendations by relevance
            avoid_food = df_food[df_food['food_rec_group'] == 'avoid'].nlargest(5, 'food_score')
            recommend_food = df_food[df_food['food_rec_group'] == 'recommend'].nlargest(5, 'food_score')
            
            food_recs['avoid'] = avoid_food.to_dict('records')
            food_recs['recommend'] = recommend_food.to_dict('records')
        
        if os.path.exists(suppl_path):
            df_suppl = pd.read_csv(suppl_path)
            avoid_suppl = df_suppl[df_suppl['suppl_rec_group'] == 'avoid'].nlargest(4, 'suppl_score')
            recommend_suppl = df_suppl[df_suppl['suppl_rec_group'] == 'recommend'].nlargest(4, 'suppl_score')
            
            suppl_recs['avoid'] = avoid_suppl.to_dict('records')
            suppl_recs['recommend'] = recommend_suppl.to_dict('records')
        
        if os.path.exists(exer_path):
            df_exer = pd.read_csv(exer_path)
            exer_recs = df_exer.nlargest(6, 'exercise_score').to_dict('records')
        
        # Get chronological age from results
        chronological_age = int(df_results['Age'].iloc[0])
        
        # Get systemic age (overall biological age)
        systemic_row = df_results[df_results['System'] == 'Systemic'].iloc[0]
        systemic_age = int(systemic_row['DiseaseAge'])
        systemic_delta = round(systemic_row['DeltaAge'], 0)
        
        # Get organ systems (exclude Systemic)
        organ_systems = df_results[df_results['System'] != 'Systemic'].copy()
        
        # Sort by delta to find drivers and resilient systems
        sorted_by_delta = organ_systems.sort_values('DeltaAge', ascending=False)
        
        # Primary aging driver (highest positive delta)
        primary_driver = sorted_by_delta.iloc[0]['System'] if sorted_by_delta.iloc[0]['DeltaAge'] > 0 else None
        
        # Secondary contributors (next highest positive deltas)
        secondary_contributors = []
        for i in range(1, min(3, len(sorted_by_delta))):
            if sorted_by_delta.iloc[i]['DeltaAge'] > 0:
                secondary_contributors.append(sorted_by_delta.iloc[i]['System'])
        
        # Most resilient (lowest/most negative deltas) - get top 4
        most_resilient = sorted_by_delta.sort_values('DeltaAge').head(4)['System'].tolist()
        
        # Convert organ systems to dict for template
        organs_data = []
        for _, row in organ_systems.iterrows():
            organs_data.append({
                'system': row['System'],
                'age': int(row['DiseaseAge']),
                'delta': round(row['DeltaAge'], 0),
                'delta_color': 'green' if row['DeltaAge'] < 0 else ('red' if row['DeltaAge'] > 0 else 'neutral')
            })
        
        return render_template('report.html',
                             patient_name=metadata.get('name', 'Unknown'),
                             patient_dob=metadata.get('dob', ''),
                             report_date=metadata.get('upload_date', ''),
                             chronological_age=chronological_age,
                             systemic_age=systemic_age,
                             systemic_delta=int(systemic_delta),
                             organs_data=organs_data,
                             primary_driver=primary_driver,
                             secondary_contributors=secondary_contributors,
                             most_resilient=most_resilient,
                             df_results=df_results,
                             df_contributions=df_contributions,
                             food_recs=food_recs,
                             suppl_recs=suppl_recs,
                             exer_recs=exer_recs)
        
    except Exception as e:
        flash(f'Error loading report: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file upload and patient data"""
    try:
        # Get form data
        patient_name = request.form.get('patient_name')
        date_of_birth = request.form.get('date_of_birth')
        
        # Validate files
        if 'results_file' not in request.files or 'contributions_file' not in request.files:
            flash('Both CSV files are required', 'error')
            return redirect(url_for('index'))
        
        results_file = request.files['results_file']
        contributions_file = request.files['contributions_file']
        
        if results_file.filename == '' or contributions_file.filename == '':
            flash('Please select both CSV files', 'error')
            return redirect(url_for('index'))
        
        if not allowed_file(results_file.filename) or not allowed_file(contributions_file.filename):
            flash('Only CSV files are allowed', 'error')
            return redirect(url_for('index'))
        
        # Generate unique patient ID
        patient_id = secrets.token_urlsafe(16)
        patient_folder = os.path.join(app.config['UPLOAD_FOLDER'], patient_id)
        os.makedirs(patient_folder, exist_ok=True)
        
        # Save files
        results_path = os.path.join(patient_folder, 'results.csv')
        contributions_path = os.path.join(patient_folder, 'contributions.csv')
        
        results_file.save(results_path)
        contributions_file.save(contributions_path)
        
        # Save optional recommendation files
        if 'food_file' in request.files and request.files['food_file'].filename != '':
            food_file = request.files['food_file']
            if allowed_file(food_file.filename):
                food_file.save(os.path.join(patient_folder, 'food.csv'))
        
        if 'suppl_file' in request.files and request.files['suppl_file'].filename != '':
            suppl_file = request.files['suppl_file']
            if allowed_file(suppl_file.filename):
                suppl_file.save(os.path.join(patient_folder, 'suppl.csv'))
        
        if 'exer_file' in request.files and request.files['exer_file'].filename != '':
            exer_file = request.files['exer_file']
            if allowed_file(exer_file.filename):
                exer_file.save(os.path.join(patient_folder, 'exer.csv'))
        
        # Validate CSV structure (basic check)
        try:
            df_results = pd.read_csv(results_path)
            df_contributions = pd.read_csv(contributions_path)
            
            # Check required columns
            required_results_cols = ['System', 'Age', 'DiseaseAge', 'DeltaAge']
            required_contributions_cols = ['System', 'Biomarker', 'Contribution']
            
            if not all(col in df_results.columns for col in required_results_cols):
                flash('Results CSV is missing required columns', 'error')
                return redirect(url_for('index'))
            
            if not all(col in df_contributions.columns for col in required_contributions_cols):
                flash('Contributions CSV is missing required columns', 'error')
                return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Error reading CSV files: {str(e)}', 'error')
            return redirect(url_for('index'))
        
        # Save patient metadata
        metadata = {
            'name': patient_name,
            'dob': date_of_birth,
            'upload_date': datetime.now().isoformat(),
            'patient_id': patient_id
        }
        
        metadata_path = os.path.join(patient_folder, 'metadata.txt')
        with open(metadata_path, 'w') as f:
            for key, value in metadata.items():
                f.write(f'{key}: {value}\n')
        
        flash('Files uploaded successfully!', 'success')
        
        # Redirect to report page
        return redirect(url_for('view_report', patient_id=patient_id))
        
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
