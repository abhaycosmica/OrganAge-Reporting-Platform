// OrganAge™ Platform - File Upload Functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all dropzones
    initializeDropzone('dropzone-results', 'results_file');
    initializeDropzone('dropzone-contributions', 'contributions_file');
    initializeDropzone('dropzone-food', 'food_file');
    initializeDropzone('dropzone-suppl', 'suppl_file');
    initializeDropzone('dropzone-exer', 'exer_file');
});

function initializeDropzone(dropzoneId, inputId) {
    const dropzone = document.getElementById(dropzoneId);
    const input = document.getElementById(inputId);
    const dropzoneContent = dropzone.querySelector('.dropzone-content');
    const filePreview = dropzone.querySelector('.file-preview');
    const fileName = filePreview.querySelector('.file-name');
    const removeBtn = filePreview.querySelector('.remove-file');
    
    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    // Highlight dropzone when dragging over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        dropzone.classList.add('dragover');
    }
    
    function unhighlight() {
        dropzone.classList.remove('dragover');
    }
    
    // Handle dropped files
    dropzone.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            input.files = files;
            handleFiles(files);
        }
    }
    
    // Handle file input change
    input.addEventListener('change', function() {
        handleFiles(this.files);
    });
    
    // Handle file selection
    function handleFiles(files) {
        if (files.length === 0) return;
        
        const file = files[0];
        
        // Validate file type
        if (!file.name.toLowerCase().endsWith('.csv')) {
            alert('Please upload a CSV file');
            input.value = '';
            return;
        }
        
        // Show file preview
        fileName.textContent = file.name;
        dropzoneContent.style.display = 'none';
        filePreview.style.display = 'flex';
    }
    
    // Remove file
    removeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        input.value = '';
        dropzoneContent.style.display = 'block';
        filePreview.style.display = 'none';
    });
    
    // Click on dropzone to open file dialog
    dropzone.addEventListener('click', function(e) {
        if (e.target !== removeBtn && !removeBtn.contains(e.target)) {
            input.click();
        }
    });
}

// Form validation
const form = document.querySelector('.intake-form');
if (form) {
    form.addEventListener('submit', function(e) {
        const resultsFile = document.getElementById('results_file');
        const contributionsFile = document.getElementById('contributions_file');
        
        if (!resultsFile.files.length || !contributionsFile.files.length) {
            e.preventDefault();
            alert('Please upload both CSV files before submitting');
            return false;
        }
        
        // Show loading state
        const submitBtn = form.querySelector('.submit-btn');
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
            <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
            </svg>
            Processing...
        `;
    });
}
