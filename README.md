# OrganAge™ Platform - Patient Intake System

## Overview
This is the patient intake portal for OrganAge™, an organ-specific biological age assessment platform by Cosmica Biosciences.

## Features Implemented (Page 1)
✅ Professional branded intake page with OrganAge™ and Cosmica logos
✅ Patient information form (Name, Date of Birth)
✅ Drag-and-drop CSV file upload for both required files:
   - OrganAge Results (df_results.csv)
   - Biomarker Contributions (df_contributions.csv)
✅ File validation (CSV format checking)
✅ Beautiful gradient design matching your brand aesthetic
✅ Responsive design for all devices
✅ Flash messages for user feedback
✅ Success page with patient confirmation

## Technology Stack
- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Processing**: Pandas
- **Storage**: File-based (SQLite coming in next phase)

## Project Structure
```
organage_platform/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── templates/
│   ├── intake.html        # Patient intake page
│   └── success.html       # Upload success page
├── static/
│   ├── css/
│   │   └── style.css      # OrganAge™ branded styles
│   ├── js/
│   │   └── upload.js      # Drag-and-drop functionality
│   └── images/
│       ├── organage_logo.png
│       └── cosmica_logo.png
├── uploads/               # Patient data storage
└── reports/              # Generated reports (future)
```

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt --break-system-packages
```

### 2. Run the Application
```bash
cd organage_platform
python app.py
```

The application will start on `http://localhost:5000`

## Usage

1. **Access the intake page**: Navigate to `http://localhost:5000`
2. **Enter patient information**:
   - Full Name
   - Date of Birth
3. **Upload CSV files**:
   - Drag and drop or click to upload `df_results.csv`
   - Drag and drop or click to upload `df_contributions.csv`
4. **Submit**: Click "Generate Report" button
5. **Confirmation**: View success page with patient ID

## CSV File Format Requirements

### df_results.csv
Required columns:
- System (organ system name)
- Age (chronological age)
- DiseaseAge (biological age)
- DeltaAge (difference)

### df_contributions.csv
Required columns:
- System (organ system name)
- Biomarker (biomarker name)
- Contribution (positive/negative value)

## Next Steps (Future Development)

**Phase 2 - Report Generation:**
- [ ] Parse CSV data and generate visual reports
- [ ] Create organ system breakdown pages
- [ ] Add biomarker contribution visualizations
- [ ] Implement PDF export functionality

**Phase 3 - Patient Portal:**
- [ ] Unique link generation for patients
- [ ] Email delivery system
- [ ] Patient authentication
- [ ] Report viewing interface

**Phase 4 - Data Management:**
- [ ] SQLite/PostgreSQL database integration
- [ ] Patient history tracking
- [ ] Admin dashboard
- [ ] Analytics and reporting

## Color Palette
- Background: `#0A0A0A` (dark)
- Cards: `#1A1A1A`
- Gradient: `#4A2A1A` → `#FF6B35` (brown to orange)
- Text Primary: `#FFFFFF`
- Text Secondary: `#B0B0B0`
- Accent Orange: `#FF6B35`

## Support
For questions or issues, contact Cosmica Biosciences.

---
© 2026 Cosmica Biosciences. All rights reserved.
