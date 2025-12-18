// Tutorial configuration and functionality using Driver.js
let tutorialDriver = null;
let tutorialProgress = {};

/**
 * Initialize and start the tutorial
 */
function startTutorial() {
    // Check if Driver is loaded - try multiple ways it could be exposed
    let DriverLib = null;

    if (typeof window.driver !== 'undefined') {
        DriverLib = window.driver;
    } else if (typeof window.Driver !== 'undefined') {
        DriverLib = window.Driver;
    } else if (typeof driver !== 'undefined') {
        DriverLib = driver;
    } else {
        console.error('Driver.js not loaded. Available globals:', Object.keys(window).filter(k => k.toLowerCase().includes('driver')));
        alert('Tutorial library failed to load. Please refresh the page.');
        return;
    }

    const currentPath = window.location.pathname;

    try {
        // Initialize Driver.js with dark mode support
        // Try both ways the library could be used
        if (DriverLib.Driver) {
            tutorialDriver = new DriverLib.Driver({
                allowClose: true,
                overlayClickNext: false,
                steps: getStepsForPage(currentPath)
            });
        } else {
            tutorialDriver = new DriverLib({
                allowClose: true,
                overlayClickNext: false,
                steps: getStepsForPage(currentPath)
            });
        }

        if (tutorialDriver.drive) {
            tutorialDriver.drive();
        } else if (tutorialDriver.start) {
            tutorialDriver.start();
        }
    } catch (e) {
        console.error('Error starting tutorial:', e);
        alert('Error starting tutorial: ' + e.message);
    }
}

/**
 * Start tutorial from a specific step
 */
function startTutorialFromStep(stepIndex) {
    // Check if Driver is loaded
    let DriverLib = null;

    if (typeof window.driver !== 'undefined') {
        DriverLib = window.driver;
    } else if (typeof window.Driver !== 'undefined') {
        DriverLib = window.Driver;
    } else if (typeof driver !== 'undefined') {
        DriverLib = driver;
    } else {
        return;
    }

    const currentPath = window.location.pathname;

    try {
        if (DriverLib.Driver) {
            tutorialDriver = new DriverLib.Driver({
                allowClose: true,
                overlayClickNext: false,
                steps: getStepsForPage(currentPath)
            });
        } else {
            tutorialDriver = new DriverLib({
                allowClose: true,
                overlayClickNext: false,
                steps: getStepsForPage(currentPath)
            });
        }

        if (tutorialDriver.drive) {
            tutorialDriver.drive();
        } else if (tutorialDriver.start) {
            tutorialDriver.start();
        }
    } catch (e) {
        console.error('Error resuming tutorial:', e);
    }
}

/**
 * Get tutorial steps for the current page
 * Routes different steps based on URL
 */
function getStepsForPage(currentPath) {
    const allSteps = getAllTutorialSteps();

    // Return steps relevant to current page
    // For simplicity, return all steps and let Driver.js handle navigation
    return allSteps;
}

/**
 * Get all tutorial steps - simplified for reliability
 */
function getAllTutorialSteps() {
    return [
        {
            element: 'h1',
            popover: {
                title: '🎉 Welcome to KitchenHub!',
                description: 'This tutorial will guide you through using your kitchen management system. You\'ll create sample data to learn how everything works.'
            }
        },
        {
            element: 'nav',
            popover: {
                title: '🧭 Navigation',
                description: 'Use the navigation menu to explore different sections: Raw Materials, Production, Sales, and Admin settings.'
            }
        },
        {
            element: '#start-tutorial-btn',
            popover: {
                title: '📚 Tutorial Button',
                description: 'You can always restart the tutorial using this button in the top navigation bar.'
            }
        },
        {
            element: 'main',
            popover: {
                title: '📋 Main Content Area',
                description: 'This is where the main features and content of the system are displayed. Each section has its own set of features and workflows.'
            }
        },
        {
            element: 'h2',
            popover: {
                title: '⚡ Quick Tips',
                description: 'Explore the system by clicking on menu items. Start with setting up your raw materials, then products, customers, and orders. Happy managing!'
            }
        }
    ];
}

/**
 * Get total number of tutorial steps
 */
function getTotalTutorialSteps() {
    return getAllTutorialSteps().length;
}

/**
 * Save tutorial progress to localStorage
 */
function saveTutorialProgress(stepIndex) {
    localStorage.setItem('tutorial_step', stepIndex);
    localStorage.setItem('tutorial_active', 'true');
}

/**
 * Load tutorial progress from localStorage
 */
function loadTutorialProgress() {
    return {
        active: localStorage.getItem('tutorial_active') === 'true',
        step: parseInt(localStorage.getItem('tutorial_step') || '0')
    };
}

/**
 * Clear tutorial progress from localStorage
 */
function clearTutorialProgress() {
    localStorage.removeItem('tutorial_step');
    localStorage.removeItem('tutorial_active');
}

/**
 * Mark tutorial as completed in the backend
 */
function completeTutorial() {
    fetch('{% url "tutorial_complete" %}', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (response.ok) {
            clearTutorialProgress();
            showCompletionMessage();
        }
    }).catch(error => {
        console.error('Error completing tutorial:', error);
    });
}

/**
 * Show completion message to user
 */
function showCompletionMessage() {
    alert('🎉 Tutorial completed successfully!\n\nYou can restart it anytime from the Tutorial button in the navigation bar.\n\nThe sample data you created can be deleted from each section.');
}

/**
 * Get CSRF token from cookies
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Check if tutorial is active in URL params and resume if needed
 */
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const tutorialProgress = loadTutorialProgress();

    if (urlParams.get('tutorial') === 'active' && tutorialProgress.active) {
        // Remove tutorial param from URL to clean it up
        if (window.history.replaceState) {
            const url = window.location.href.replace(/[?&]tutorial=active/, '');
            window.history.replaceState({}, document.title, url);
        }

        // Resume tutorial from saved step
        setTimeout(() => {
            startTutorialFromStep(tutorialProgress.step);
        }, 500);
    }
});
