// DOM Elements
const navbar = document.querySelector('.navbar');
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation menu
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const userMenuButton = document.querySelector('.user-menu-button');
    const userDropdown = document.querySelector('.user-dropdown');
    const body = document.body;

    // Function to close all menus
    function closeAllMenus() {
        if (navLinks) navLinks.classList.remove('active');
        if (userDropdown) userDropdown.classList.remove('active');
        body.style.overflow = '';
    }

    // Handle hamburger menu
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function(e) {
            e.stopPropagation();
            
            // Close user dropdown if open
            if (userDropdown) userDropdown.classList.remove('active');
            
            // Toggle navigation menu
            navLinks.classList.toggle('active');
            body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : '';
        });

        // Close menu when clicking a navigation link
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                closeAllMenus();
            });
        });
    }

    // Handle user menu
    if (userMenuButton && userDropdown) {
        userMenuButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Close navigation menu if open
            if (navLinks) navLinks.classList.remove('active');
            
            // Toggle user dropdown
            userDropdown.classList.toggle('active');
            
            // Handle body scroll on mobile
            if (window.innerWidth <= 768) {
                body.style.overflow = userDropdown.classList.contains('active') ? 'hidden' : '';
            }
        });

        // Close dropdown when clicking its links
        userDropdown.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                closeAllMenus();
            });
        });
    }

    // Close menus when clicking outside
    document.addEventListener('click', function(e) {
        if ((!hamburger || !hamburger.contains(e.target)) && 
            (!navLinks || !navLinks.contains(e.target)) &&
            (!userMenuButton || !userMenuButton.contains(e.target)) &&
            (!userDropdown || !userDropdown.contains(e.target))) {
            closeAllMenus();
        }
    });

    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            closeAllMenus();
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
        const formData = {
            service: document.getElementById('service').value,
            'preferred-date': document.getElementById('preferred-date').value,
            'preferred-time': document.getElementById('preferred-time').value,
            notes: document.getElementById('notes').value || ''
        };
        
        // Show loading state
        const submitButton = bookingForm.querySelector('.submit-button');
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Отправка...';
        submitButton.disabled = true;
        
        try {
            // Send data to server
            const response = await fetch('/api/book-appointment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (response.ok) {
                // Show success message
                submitButton.textContent = 'Запись создана!';
                submitButton.style.backgroundColor = '#28a745';
                
                // Redirect to appointments page after delay
                setTimeout(() => {
                    window.location.href = '/appointments';
                }, 2000);
            } else {
                throw new Error(result.message || 'Не удалось создать запись');
            }
        } catch (error) {
            // Show error message
            submitButton.textContent = 'Ошибка! Попробуйте снова';
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

// Login form handling
const loginForm = document.getElementById('login-form');
if (loginForm) {
    // Password visibility toggle
    const togglePassword = document.getElementById('toggle-password');
    const passwordInput = document.getElementById('password');
    
    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    }

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        clearErrors();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const remember = document.getElementById('remember').checked;

        // Basic validation
        let hasErrors = false;
        if (!email) {
            showError('email', 'Email is required');
            hasErrors = true;
        } else if (!validateEmail(email)) {
            showError('email', 'Please enter a valid email');
            hasErrors = true;
        }

        if (!password) {
            showError('password', 'Password is required');
            hasErrors = true;
        }

        if (hasErrors) return;

        // Show loading state
        const submitButton = loginForm.querySelector('.submit-button');
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Logging in...';
        submitButton.disabled = true;

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email,
                    password,
                    remember
                })
            });

            const result = await response.json();

            if (response.ok) {
                // Redirect on success
                window.location.href = result.redirect;
            } else {
                // Show error message
                showError('password', result.message);
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            }
        } catch (error) {
            console.error('Error:', error);
            showError('password', 'An error occurred. Please try again.');
            submitButton.textContent = originalText;
            submitButton.disabled = false;
        }
    });
}

// Helper functions
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function showError(fieldId, message) {
    const errorDiv = document.getElementById(`${fieldId}-error`);
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.classList.add('show');
    }
}

function clearErrors() {
    document.querySelectorAll('.error-message').forEach(error => {
        error.textContent = '';
        error.classList.remove('show');
    });
}

// Registration form handling
const registrationForm = document.getElementById('register-form');
if (registrationForm) {
    registrationForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        clearErrors();
        
        const first_name = document.getElementById('first_name').value;
        const last_name = document.getElementById('last_name').value;
        const middle_name = document.getElementById('middle_name').value;
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;
        const birthDate = document.getElementById('birth_date').value;
        
        let isValid = true;
        
        if (!first_name) {
            showError('first_name', 'Пожалуйста, введите ваше имя');
            isValid = false;
        }
        
        if (!last_name) {
            showError('last_name', 'Пожалуйста, введите вашу фамилию');
            isValid = false;
        }
        
        if (!validateEmail(email)) {
            showError('email', 'Пожалуйста, введите корректный email');
            isValid = false;
        }

        if (!phone) {
            showError('phone', 'Пожалуйста, введите номер телефона');
            isValid = false;
        }
        
        if (!password) {
            showError('password', 'Пожалуйста, введите пароль');
            isValid = false;
        }
        
        if (password !== confirmPassword) {
            showError('confirm_password', 'Пароли не совпадают');
            isValid = false;
        }
        
        if (!birthDate) {
            showError('birth_date', 'Пожалуйста, введите дату рождения');
            isValid = false;
        }
        
        if (isValid) {
            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        first_name,
                        last_name,
                        middle_name,
                        email,
                        phone,
                        password,
                        birth_date: birthDate
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    window.location.href = data.redirect || '/login';
                } else {
                    showError('email', data.message || 'Ошибка регистрации');
                }
            } catch (error) {
                showError('email', 'Произошла ошибка при регистрации');
                console.error('Error:', error);
            }
        }
    });
} 