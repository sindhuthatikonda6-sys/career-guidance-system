// Career Guidance System - Interactive Features
document.addEventListener('DOMContentLoaded', function() {
    
    // Form validation and animations
    const careerForm = document.getElementById('careerForm');
    if (careerForm) {
        careerForm.addEventListener('submit', function(e) {
            showLoading();
        });
    }

    // Real-time score validation
    const scoreInputs = document.querySelectorAll('input[type="number"]');
    scoreInputs.forEach(input => {
        input.addEventListener('input', function() {
            validateScore(this);
        });
    });

    // Interest level color coding
    const interestSelects = document.querySelectorAll('select[name^="interest_"]');
    interestSelects.forEach(select => {
        select.addEventListener('change', function() {
            colorCodeInterest(this);
        });
        colorCodeInterest(select); // Initial color
    });

    // Smooth scrolling and animations
    window.addEventListener('scroll', function() {
        animateOnScroll();
    });

    // Confidence meter animation
    const confidenceMeters = document.querySelectorAll('.confidence-meter');
    confidenceMeters.forEach(meter => {
        animateConfidenceMeter(meter);
    });
});

// Show loading animation on form submit
function showLoading() {
    const btn = document.querySelector('.submit-btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
    btn.disabled = true;
    setTimeout(() => {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }, 2000);
}

// Validate score inputs (0-100)
function validateScore(input) {
    const value = parseInt(input.value);
    if (value < 0) input.value = 0;
    if (value > 100) input.value = 100;
    
    // Color code based on score
    if (value >= 90) input.style.borderColor = '#4CAF50';
    else if (value >= 70) input.style.borderColor = '#FF9800';
    else input.style.borderColor = '#f44336';
}

// Color code interest levels
function colorCodeInterest(select) {
    const value = select.value;
    select.style.borderColor = value === 'High' ? '#4CAF50' : 
                              value === 'Medium' ? '#FF9800' : '#f44336';
}

// Animate elements on scroll
function animateOnScroll() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    elements.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
            el.classList.add('animate');
        }
    });
}

// Animate confidence meter
function animateConfidenceMeter(meter) {
    const fill = meter.querySelector('.progress-fill');
    const targetWidth = meter.dataset.width || '80';
    let width = 0;
    const interval = setInterval(() => {
        if (width >= parseInt(targetWidth)) {
            clearInterval(interval);
        } else {
            width += 2;
            fill.style.width = width + '%';
        }
    }, 20);
}

// Download profile as PDF (Client-side)
function downloadProfile() {
    // 1. Get Name and Career
    const nameInput = document.querySelector('input[name="name"]');
    const name = nameInput ? nameInput.value : 'Student';
    const careerTitle = document.querySelector('.career-title, h2')?.innerText || 'Career Path';

    // 2. Scrape Roadmap Steps (Step 1 first, then details)
    let roadmapText = '';
    const steps = document.querySelectorAll('.roadmap-step');

    if (steps.length > 0) {
        steps.forEach((step) => {
            // Try to find the topic header and detail list items
            const topic = step.querySelector('h3, h4, .topic')?.innerText || 'Step';
            const details = Array.from(step.querySelectorAll('li')).map(li => li.innerText);
            
            roadmapText += `\n${topic}\n`;
            details.forEach(detail => {
                roadmapText += `   - ${detail}\n`;
            });
        });
    } else {
        roadmapText = '\n(Roadmap details not visible on this page)';
    }
    
    const profileText = `
CAREER GUIDANCE REPORT
----------------------
Name: ${name}
Target Career: ${careerTitle}
Date: ${new Date().toLocaleDateString()}

LEARNING ROADMAP:
${roadmapText}
    `;
    
    const blob = new Blob([profileText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'career-roadmap.txt';
    a.click();
}

// Interactive roadmap timeline
function initRoadmapTimeline() {
    const steps = document.querySelectorAll('.roadmap-step');
    steps.forEach((step, index) => {
        step.addEventListener('click', function() {
            this.classList.toggle('expanded');
        });
    });
}

// Initialize on page load
if (document.querySelector('.roadmap-timeline')) {
    initRoadmapTimeline();
}

// Form auto-fill demo data
document.addEventListener('DOMContentLoaded', function() {
    const demoBtn = document.querySelector('.demo-btn');
    if (demoBtn) {
        demoBtn.addEventListener('click', fillDemoData);
    }
});

function fillDemoData() {
    document.querySelector('input[name="name"]').value = 'Rahul Sharma';
    document.querySelector('input[name="branch"]').value = 'CSE - 3rd Year';
    document.querySelectorAll('input[type="number"]')[0].value = 92;
    document.querySelectorAll('input[type="number"]')[1].value = 95;
    document.querySelectorAll('input[type="number"]')[2].value = 94;
    
    // Trigger validations
    document.querySelectorAll('input[type="number"]').forEach(input => validateScore(input));
    console.log('✅ Demo data filled!');
}