// DOM Elements
const navbar = document.querySelector('.navbar');
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

// Mobile menu toggle
hamburger.addEventListener('click', () => {
    navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
    hamburger.classList.toggle('active');
});

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    if (window.innerWidth <= 768) {
        const isClickInside = navbar.contains(e.target);
        
        if (!isClickInside && navLinks.style.display === 'flex') {
            navLinks.style.display = 'none';
            hamburger.classList.remove('active');
        }
    }
});

// Close mobile menu when clicking a link
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        if (window.innerWidth <= 768) {
            navLinks.style.display = 'none';
            hamburger.classList.remove('active');
        }
    });
});

// Handle window resize
window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        navLinks.style.display = 'flex';
    } else {
        navLinks.style.display = 'none';
        hamburger.classList.remove('active');
    }
});

// Add shadow to navbar on scroll
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.1)';
    }
});

// Smooth scroll to sections
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form handling
const contactForm = document.getElementById('contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(this);
        const formObject = {};
        formData.forEach((value, key) => formObject[key] = value);
        
        // Show loading state
        const submitButton = contactForm.querySelector('.submit-button');
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Sending...';
        submitButton.disabled = true;
        
        try {
            // Send data to server
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formObject)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                // Show success message
                submitButton.textContent = 'Message Sent!';
                submitButton.style.backgroundColor = '#28a745';
                
                // Reset form after delay
                setTimeout(() => {
                    contactForm.reset();
                    submitButton.textContent = originalText;
                    submitButton.style.backgroundColor = '';
                    submitButton.disabled = false;
                }, 3000);
            } else {
                throw new Error(result.message || 'Failed to send message');
            }
        } catch (error) {
            // Show error message
            submitButton.textContent = 'Error! Try Again';
            submitButton.style.backgroundColor = '#dc3545';
            submitButton.disabled = false;
            
            // Reset button after delay
            setTimeout(() => {
                submitButton.textContent = originalText;
                submitButton.style.backgroundColor = '';
            }, 3000);
            
            console.error('Error:', error);
        }
    });
}

// Booking form handling
const bookingForm = document.getElementById('booking-form');
if (bookingForm) {
    // Set minimum date to today
    const preferredDate = document.getElementById('preferred-date');
    if (preferredDate) {
        const today = new Date().toISOString().split('T')[0];
        preferredDate.setAttribute('min', today);
    }

    bookingForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(this);
        const formObject = {};
        formData.forEach((value, key) => formObject[key] = value);
        
        // Show loading state
        const submitButton = bookingForm.querySelector('.submit-button');
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Scheduling...';
        submitButton.disabled = true;
        
        try {
            // Send data to server
            const response = await fetch('/api/book-appointment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formObject)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                // Show success message
                submitButton.textContent = 'Appointment Scheduled!';
                submitButton.style.backgroundColor = '#28a745';
                
                // Reset form after delay
                setTimeout(() => {
                    bookingForm.reset();
                    submitButton.textContent = originalText;
                    submitButton.style.backgroundColor = '';
                    submitButton.disabled = false;
                }, 3000);
            } else {
                throw new Error(result.message || 'Failed to schedule appointment');
            }
        } catch (error) {
            // Show error message
            submitButton.textContent = 'Error! Try Again';
            submitButton.style.backgroundColor = '#dc3545';
            submitButton.disabled = false;
            
            // Reset button after delay
            setTimeout(() => {
                submitButton.textContent = originalText;
                submitButton.style.backgroundColor = '';
            }, 3000);
            
            console.error('Error:', error);
        }
    });
}

// Service card hover effects
document.querySelectorAll('.service-item').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-5px)';
        card.style.boxShadow = '0 8px 20px rgba(0, 0, 0, 0.15)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
        card.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.1)';
    });
});

// Team member hover effects
document.querySelectorAll('.team-member').forEach(member => {
    member.addEventListener('mouseenter', () => {
        member.style.transform = 'translateY(-5px)';
        member.style.boxShadow = '0 8px 20px rgba(0, 0, 0, 0.15)';
    });
    
    member.addEventListener('mouseleave', () => {
        member.style.transform = 'translateY(0)';
        member.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.1)';
    });
});

// Stats animation
const stats = document.querySelectorAll('.stat-number');
let animated = false;

function animateStats() {
    if (animated) return;
    
    stats.forEach(stat => {
        const target = parseInt(stat.textContent);
        let current = 0;
        const increment = target / 50; // Adjust speed of counting
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                clearInterval(timer);
                stat.textContent = target + (stat.textContent.includes('k') ? 'k+' : '+');
            } else {
                stat.textContent = Math.floor(current);
            }
        }, 30);
    });
    
    animated = true;
}

// Check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

// Animate stats when scrolling into view
window.addEventListener('scroll', () => {
    if (stats.length > 0 && isInViewport(stats[0])) {
        animateStats();
    }
}); 