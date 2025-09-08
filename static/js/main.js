// SomaPopote - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initLanguageToggle();
    initSmoothScrolling();
    initAnimations();
    initDashboardTabs();
    initFormValidation();
    initTooltips();
});

// Language Toggle Functionality
function initLanguageToggle() {
    const languageSelect = document.getElementById('languageSelect');
    if (languageSelect) {
        languageSelect.addEventListener('change', function() {
            const selectedLang = this.value;
            console.log('Language changed to:', selectedLang);
            
            // Here you would implement actual language switching
            // For demo purposes, show notification
            if (selectedLang === 'en') {
                showNotification('English version coming soon!', 'info');
            } else {
                showNotification('Swahili version active!', 'success');
            }
        });
    }
}

// Smooth Scrolling for Navigation Links
function initSmoothScrolling() {
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
}

// Initialize Animations on Scroll
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all animated elements
    const animatedElements = document.querySelectorAll('.feature-card, .step-card, .stat-card, .student-card');
    animatedElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(element);
    });
}

// Dashboard Tab Functionality
function initDashboardTabs() {
    const tabLinks = document.querySelectorAll('.sidebar .nav-link[data-tab]');
    const tabContents = document.querySelectorAll('.tab-content');

    tabLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all tabs
            tabLinks.forEach(tab => tab.classList.remove('active'));
            tabContents.forEach(content => content.style.display = 'none');
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Show corresponding content
            const tabId = this.getAttribute('data-tab');
            const targetContent = document.getElementById(tabId);
            if (targetContent) {
                targetContent.style.display = 'block';
            }
        });
    });
}

// Form Validation
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (validateForm(this)) {
                // Show loading state
                const submitBtn = this.querySelector('button[type="submit"]');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner"></span> Inatuma...';
                submitBtn.disabled = true;
                
                // Simulate form submission
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                    showNotification('Umefanikiwa!', 'success');
                    this.reset();
                }, 2000);
            }
        });
    });
}

// Validate Form Fields
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    if (!isValid) {
        showNotification('Tafadhali jaza sehemu zote zinazohitajika', 'error');
    }
    
    return isValid;
}

// Initialize Tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Show Notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Loading Spinner
function showLoading(element) {
    element.innerHTML = '<div class="spinner"></div>';
    element.disabled = true;
}

function hideLoading(element, originalContent) {
    element.innerHTML = originalContent;
    element.disabled = false;
}

// Progress Ring Animation
function animateProgressRing(element, percentage) {
    const degree = (percentage / 100) * 360;
    element.style.setProperty('--progress', `${degree}deg`);
    element.textContent = `${percentage}%`;
}

// Student Search Functionality
function initStudentSearch() {
    const searchInput = document.querySelector('input[placeholder="Tafuta mwanafunzi..."]');
    const studentCards = document.querySelectorAll('.student-card');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            studentCards.forEach(card => {
                const studentName = card.querySelector('h6').textContent.toLowerCase();
                const studentInfo = card.textContent.toLowerCase();
                
                if (studentName.includes(searchTerm) || studentInfo.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
}

// Bulk SMS Functionality
function sendBulkSMS(phoneNumbers, message) {
    return new Promise((resolve, reject) => {
        // Simulate SMS sending
        setTimeout(() => {
            const successCount = Math.floor(Math.random() * phoneNumbers.length);
            resolve({
                success: true,
                successCount: successCount,
                totalNumbers: phoneNumbers.length,
                message: 'SMS sent successfully'
            });
        }, 2000);
    });
}

// Chart Initialization (if Chart.js is available)
function initCharts() {
    if (typeof Chart !== 'undefined') {
        // Progress Chart
        const progressCtx = document.getElementById('progressChart');
        if (progressCtx) {
            new Chart(progressCtx, {
                type: 'line',
                data: {
                    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                    datasets: [{
                        label: 'Student Progress',
                        data: [65, 75, 80, 89],
                        borderColor: '#007bff',
                        backgroundColor: 'rgba(0, 123, 255, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }
        
        // Subject Distribution Chart
        const subjectCtx = document.getElementById('subjectChart');
        if (subjectCtx) {
            new Chart(subjectCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Hisabati', 'Sayansi', 'Kiswahili', 'English'],
                    datasets: [{
                        data: [30, 25, 25, 20],
                        backgroundColor: [
                            '#007bff',
                            '#28a745',
                            '#ffc107',
                            '#dc3545'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
    }
}

// Real-time Updates Simulation
function simulateRealTimeUpdates() {
    // Update student count
    setInterval(() => {
        const studentCountElement = document.querySelector('.stat-number');
        if (studentCountElement && studentCountElement.textContent === '156') {
            const currentCount = parseInt(studentCountElement.textContent);
            const newCount = currentCount + Math.floor(Math.random() * 3);
            studentCountElement.textContent = newCount;
        }
    }, 30000); // Update every 30 seconds
    
    // Update quiz count
    setInterval(() => {
        const quizCountElement = document.querySelectorAll('.stat-number')[2];
        if (quizCountElement && quizCountElement.textContent === '1,234') {
            const currentCount = parseInt(quizCountElement.textContent.replace(',', ''));
            const newCount = currentCount + Math.floor(Math.random() * 5);
            quizCountElement.textContent = newCount.toLocaleString();
        }
    }, 20000); // Update every 20 seconds
}

// Keyboard Shortcuts
function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[placeholder="Tafuta mwanafunzi..."]');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            });
        }
    });
}

// Print Functionality
function printContent(contentId) {
    const printContent = document.getElementById(contentId);
    if (printContent) {
        const printWindow = window.open('', '_blank');
        printWindow.document.write(`
            <html>
                <head>
                    <title>SomaPopote - Print</title>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                    <style>
                        body { font-family: Arial, sans-serif; }
                        .no-print { display: none; }
                        @media print {
                            .no-print { display: none !important; }
                        }
                    </style>
                </head>
                <body>
                    ${printContent.innerHTML}
                </body>
            </html>
        `);
        printWindow.document.close();
        printWindow.print();
    }
}

// Export to CSV
function exportToCSV(data, filename) {
    const csv = convertToCSV(data);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', filename);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function convertToCSV(data) {
    const header = Object.keys(data[0]);
    const csvRows = [
        header.join(','),
        ...data.map(row => header.map(header => row[header]).join(','))
    ];
    return csvRows.join('\n');
}

// Initialize everything when page loads
document.addEventListener('DOMContentLoaded', function() {
    initStudentSearch();
    simulateRealTimeUpdates();
    initKeyboardShortcuts();
    initCharts();
    
    // Add click handlers for print buttons
    const printButtons = document.querySelectorAll('[onclick*="printContent"]');
    printButtons.forEach(button => {
        button.addEventListener('click', function() {
            const contentId = this.getAttribute('onclick').match(/printContent\('(.+?)'\)/)[1];
            printContent(contentId);
        });
    });
});

// Utility function to format numbers
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Utility function to format dates
function formatDate(date) {
    return new Date(date).toLocaleDateString('sw-TZ', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
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

// Debounce function for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function for performance
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Local storage helpers
function saveToLocalStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
        return true;
    } catch (e) {
        console.error('Error saving to localStorage:', e);
        return false;
    }
}

function getFromLocalStorage(key) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    } catch (e) {
        console.error('Error getting from localStorage:', e);
        return null;
    }
}

// Session storage helpers
function saveToSessionStorage(key, value) {
    try {
        sessionStorage.setItem(key, JSON.stringify(value));
        return true;
    } catch (e) {
        console.error('Error saving to sessionStorage:', e);
        return false;
    }
}

function getFromSessionStorage(key) {
    try {
        const item = sessionStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    } catch (e) {
        console.error('Error getting from sessionStorage:', e);
        return null;
    }
}

// API call helper
async function apiCall(url, options = {}) {
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const mergedOptions = { ...defaultOptions, ...options };

    try {
        const response = await fetch(url, mergedOptions);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Form data serializer
function serializeForm(form) {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    return data;
}

// Copy to clipboard function
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Nakili kwenye clipboard!', 'success');
    } catch (err) {
        console.error('Failed to copy text: ', err);
        showNotification('Imeshindwa kunakili', 'error');
    }
}

// Generate random ID
function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// Validate phone number (Tanzania format)
function validatePhoneNumber(phoneNumber) {
    const tanzaniaRegex = /^(\+255|0)[67]\d{8}$/;
    return tanzaniaRegex.test(phoneNumber);
}

// Format phone number to international format
function formatPhoneNumber(phoneNumber) {
    if (phoneNumber.startsWith('+255')) {
        return phoneNumber;
    } else if (phoneNumber.startsWith('0')) {
        return '+255' + phoneNumber.substring(1);
    }
    return phoneNumber;
}

// Calculate percentage
function calculatePercentage(part, total) {
    if (total === 0) return 0;
    return Math.round((part / total) * 100);
}

// Get time ago string
function timeAgo(date) {
    const seconds = Math.floor((new Date() - new Date(date)) / 1000);
    
    let interval = seconds / 31536000;
    if (interval > 1) {
        return Math.floor(interval) + ' miaka iliyopita';
    }
    
    interval = seconds / 2592000;
    if (interval > 1) {
        return Math.floor(interval) + ' miezi iliyopita';
    }
    
    interval = seconds / 86400;
    if (interval > 1) {
        return Math.floor(interval) + ' siku iliyopita';
    }
    
    interval = seconds / 3600;
    if (interval > 1) {
        return Math.floor(interval) + ' masaa iliyopita';
    }
    
    interval = seconds / 60;
    if (interval > 1) {
        return Math.floor(interval) + ' dakika iliyopita';
    }
    
    return Math.floor(seconds) + ' sekunde iliyopita';
}

// Initialize tooltips when dynamically added content
function initializeDynamicTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]:not(.tooltip-initialized)'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
        tooltipTriggerEl.classList.add('tooltip-initialized');
    });
}

// Handle window resize events
const handleResize = debounce(() => {
    // Reinitialize charts if they exist
    if (typeof Chart !== 'undefined') {
        Chart.instances.forEach(chart => {
            chart.resize();
        });
    }
}, 250);

window.addEventListener('resize', handleResize);

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    // Clean up any pending operations
    // Save any unsaved data if needed
});

// Error handling
window.addEventListener('error', (e) => {
    console.error('Global error:', e);
    // You could send error reports to your server here
});

// Unhandled promise rejection handling
window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled promise rejection:', e);
    // You could send error reports to your server here
});

// Export functions for global access
window.SomaPopote = {
    showNotification,
    showLoading,
    hideLoading,
    animateProgressRing,
    sendBulkSMS,
    printContent,
    exportToCSV,
    copyToClipboard,
    validatePhoneNumber,
    formatPhoneNumber,
    calculatePercentage,
    timeAgo,
    apiCall,
    saveToLocalStorage,
    getFromLocalStorage,
    saveToSessionStorage,
    getFromSessionStorage
};
