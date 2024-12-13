// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Add active class to current nav item
const navLinks = document.querySelectorAll('.nav-links a');
navLinks.forEach(link => {
    link.addEventListener('click', function() {
        navLinks.forEach(l => l.classList.remove('active'));
        this.classList.add('active');
    });
});

// Search functionality
const searchInput = document.querySelector('.search-bar input');
const searchButton = document.querySelector('.search-bar button');

searchButton.addEventListener('click', () => {
    const searchTerm = searchInput.value.trim();
    if (searchTerm) {
        // Implement search functionality here
        console.log('Searching for:', searchTerm);
    }
});

// Novel cards hover effect
const novelCards = document.querySelectorAll('.novel-card');
novelCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});

// Implement smooth scroll to top when hero button is clicked
const ctaButton = document.querySelector('.cta-button');
ctaButton.addEventListener('click', () => {
    window.scrollTo({
        top: document.querySelector('.featured-novels').offsetTop,
        behavior: 'smooth'
    });
});

// Authentication Functions
function updateUIForLoggedInUser(userData) {
    // Hide login section
    document.getElementById('login-section').style.display = 'none';
    
    // Hide About and Contact links
    document.querySelector('.about-link').style.display = 'none';
    document.querySelector('.contact-link').style.display = 'none';

    // Show admin button for admin users
    if (userData.role === 'admin') {
        const adminButton = document.querySelector('.admin-button');
        adminButton.style.display = 'inline-block';
        adminButton.addEventListener('click', () => {
            window.location.href = '/admin/dashboard.html';
        });
    }

    // Show translator button for users with translator permission
    if (userData.permissions && userData.permissions.can_translate) {
        const translatorButton = document.querySelector('.translator-button');
        translatorButton.style.display = 'inline-block';
        translatorButton.addEventListener('click', () => {
            window.location.href = '/translator/dashboard.html';
        });
    }
}

async function checkLoginState() {
    const token = localStorage.getItem('token');
    if (token) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/verify`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.ok) {
                const userData = await response.json();
                updateUIForLoggedInUser(userData);
            } else {
                updateUIForLoggedOutUser();
            }
        } catch (error) {
            console.error('Auth check failed:', error);
            updateUIForLoggedOutUser();
        }
    } else {
        updateUIForLoggedOutUser();
    }
}

async function login(event) {
    event.preventDefault();
    const form = document.getElementById('login-form');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: data.username,
                password: data.password
            })
        });

        if (response.ok) {
            const result = await response.json();
            localStorage.setItem('token', result.access_token);
            localStorage.setItem('user', JSON.stringify(result.user));
            
            // Update UI based on user role
            updateUIForLoggedInUser(result.user);
            
            // Close the login dropdown
            const loginDropdown = document.querySelector('.login-dropdown-content');
            if (loginDropdown) {
                loginDropdown.style.display = 'none';
            }
        } else {
            const error = await response.json();
            alert(error.error || 'Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Failed to login. Please try again.');
    }
}

function logout() {
    updateUIForLoggedOutUser();
    window.location.href = '/';
}

function updateUIForLoggedOutUser() {
    // Show login section and hide user menu
    document.getElementById('login-section').style.display = 'block';
    document.querySelector('.user-menu').style.display = 'none';
    
    // Show about and contact links
    document.querySelector('.about-link').style.display = 'block';
    document.querySelector('.contact-link').style.display = 'block';
    
    // Hide admin button
    document.querySelector('.admin-button').style.display = 'none';
    
    // Clear stored token
    localStorage.removeItem('token');
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Check login state on page load
    checkLoginState();

    // Login form submission
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', login);
    }

    // Logout button
    const logoutBtn = document.querySelector('.logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            logout();
        });
    }

    // Login dropdown
    const loginBtn = document.querySelector('.login-btn');
    const loginDropdown = document.querySelector('.login-dropdown-content');
    
    if (loginBtn && loginDropdown) {
        loginBtn.addEventListener('click', (e) => {
            e.preventDefault();
            loginDropdown.style.display = loginDropdown.style.display === 'block' ? 'none' : 'block';
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!loginBtn.contains(e.target) && !loginDropdown.contains(e.target)) {
                loginDropdown.style.display = 'none';
            }
        });
    }
});

// Navbar visibility control
const navbar = document.querySelector('.navbar');
let lastScrollY = window.scrollY;
let isMouseNearNav = false;
let hideTimeout;
let scrollTimeout;

// Function to show navbar
function showNavbar() {
    navbar.classList.remove('hidden');
    navbar.classList.add('show');
}

// Function to hide navbar
function hideNavbar() {
    if (!isMouseNearNav) {
        navbar.classList.add('hidden');
        navbar.classList.remove('show');
    }
}

// Handle scroll events with debouncing
window.addEventListener('scroll', () => {
    clearTimeout(scrollTimeout);
    
    const currentScrollY = window.scrollY;
    const scrollingUp = currentScrollY < lastScrollY;
    const atTop = currentScrollY < 50;
    
    if (scrollingUp || atTop) {
        showNavbar();
    } else if (!isMouseNearNav && currentScrollY > 50) {
        // Add delay before hiding when scrolling down
        scrollTimeout = setTimeout(() => {
            hideNavbar();
        }, 150);
    }
    
    lastScrollY = currentScrollY;
});

// Handle mouse movement
document.addEventListener('mousemove', (e) => {
    clearTimeout(hideTimeout);
    
    // Check if mouse is near the top of the page
    if (e.clientY <= 80) { // Increased detection area
        isMouseNearNav = true;
        showNavbar();
    } else {
        isMouseNearNav = false;
        // Only hide if we're not at the top and scrolling down
        if (window.scrollY > 50 && window.scrollY >= lastScrollY) {
            hideTimeout = setTimeout(() => {
                hideNavbar();
            }, 300);
        }
    }
});

// UI Helpers
function showModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function showSuccess(message) {
    // Implement your success notification
    alert(message); // Replace with better notification system
}

function showError(message) {
    // Implement your error notification
    alert(message); // Replace with better notification system
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Modal close buttons
    document.querySelectorAll('.cancel-btn').forEach(btn => {
        btn.addEventListener('click', () => closeModal(btn.closest('.modal').id));
    });
});
