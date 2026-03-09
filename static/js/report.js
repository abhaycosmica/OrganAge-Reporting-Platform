// OrganAge™ Report Interactive Features

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll handling
    const reportPages = document.querySelectorAll('.report-page');
    
    // Add scroll progress indicator (optional)
    let currentPage = 0;
    
    window.addEventListener('scroll', function() {
        const scrollPosition = window.scrollY;
        const windowHeight = window.innerHeight;
        
        reportPages.forEach((page, index) => {
            const pageTop = page.offsetTop;
            const pageBottom = pageTop + page.offsetHeight;
            
            if (scrollPosition >= pageTop - windowHeight / 2 && 
                scrollPosition < pageBottom - windowHeight / 2) {
                currentPage = index;
            }
        });
    });
    
    // Keyboard navigation (optional)
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowDown' || e.key === 'PageDown') {
            e.preventDefault();
            if (currentPage < reportPages.length - 1) {
                reportPages[currentPage + 1].scrollIntoView({ behavior: 'smooth' });
            }
        } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
            e.preventDefault();
            if (currentPage > 0) {
                reportPages[currentPage - 1].scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
    
    console.log('OrganAge™ Report loaded successfully');
});

// Recommendations Tab Switching
document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.recs-tab');
    const tabContents = document.querySelectorAll('.recs-tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            
            // Remove active class from all tabs and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked tab and corresponding content
            this.classList.add('active');
            document.getElementById(`tab-${tabName}`).classList.add('active');
        });
    });
});
