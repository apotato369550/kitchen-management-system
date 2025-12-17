// Tutorial configuration and functionality using Driver.js
let tutorialDriver = null;
let tutorialProgress = {};

/**
 * Initialize and start the tutorial
 */
function startTutorial() {
    // Check if Driver.js is loaded
    if (typeof window.driver === 'undefined') {
        console.error('Driver.js not loaded');
        alert('Tutorial library failed to load. Please refresh the page.');
        return;
    }

    const currentPath = window.location.pathname;

    // Initialize Driver.js with dark mode support
    tutorialDriver = window.driver({
        showProgress: true,
        showButtons: ['next', 'previous', 'close'],
        steps: getStepsForPage(currentPath),
        onDestroyStarted: () => {
            if (tutorialDriver && tutorialDriver.hasNextStep && tutorialDriver.hasNextStep()) {
                const confirmed = confirm('Are you sure you want to exit the tutorial? Your progress will be saved.');
                if (confirmed) {
                    tutorialDriver.destroy();
                } else {
                    return false;
                }
            } else {
                tutorialDriver.destroy();
            }
        },
        onDestroyed: () => {
            // Tutorial was closed without completing
            if (tutorialDriver && tutorialDriver.getActiveIndex && tutorialDriver.getActiveIndex() < getTotalTutorialSteps() - 1) {
                saveTutorialProgress(tutorialDriver.getActiveIndex());
            }
        },
        popoverClass: 'tutorial-popover',
        progressText: 'Step {{current}} of {{total}}',
        nextBtnText: 'Next →',
        prevBtnText: '← Back',
        doneBtnText: 'Finish ✓'
    });

    tutorialDriver.drive();
}

/**
 * Start tutorial from a specific step
 */
function startTutorialFromStep(stepIndex) {
    const currentPath = window.location.pathname;

    tutorialDriver = window.driver({
        showProgress: true,
        showButtons: ['next', 'previous', 'close'],
        steps: getStepsForPage(currentPath),
        popoverClass: 'tutorial-popover',
        startIndex: stepIndex
    });

    tutorialDriver.drive();
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
 * Get all 14 tutorial steps
 */
function getAllTutorialSteps() {
    return [
        // Step 1: Welcome
        {
            element: '.bg-gradient-to-r.from-blue-50',
            popover: {
                title: '🎉 Welcome to KitchenHub!',
                description: 'This interactive tutorial will guide you through setting up and using your kitchen management system. You\'ll create real sample data that you can delete later. Let\'s begin! (About 7 minutes)',
                position: 'bottom'
            }
        },

        // Step 2: Navigation Bar
        {
            element: '.hidden.md\\:flex.items-center.gap-1',
            popover: {
                title: '🧭 Navigation System',
                description: 'Navigate using these organized dropdown menus. Each section groups related features for your workflow: Raw Materials, Production, Sales, and Admin (if you\'re an admin).',
                position: 'bottom'
            }
        },

        // Step 3: Raw Materials Dropdown
        {
            element: 'button[onclick="toggleDropdown(\'materials-menu\')"]',
            popover: {
                title: '📦 Raw Materials Section',
                description: 'Let\'s start by creating your raw materials library. Click this dropdown to see the options.',
                position: 'bottom',
                onNextClick: () => {
                    const btn = document.querySelector('button[onclick="toggleDropdown(\'materials-menu\')"]');
                    if (btn) btn.click();
                }
            }
        },

        // Step 4: Navigate to Raw Materials List
        {
            element: '#materials-menu a[href*="raw_material"]',
            popover: {
                title: '📚 Raw Materials Library',
                description: 'This is where you manage all your raw materials. Click "Library" to start.',
                position: 'right',
                onNextClick: () => {
                    const link = document.querySelector('#materials-menu a[href*="raw_material_list"]');
                    if (link) {
                        saveTutorialProgress(3);
                        window.location.href = link.getAttribute('href') + '?tutorial=active';
                    }
                }
            }
        },

        // Step 5: Add Raw Material Button
        {
            element: 'a[href*="raw_material_create"]',
            popover: {
                title: '➕ Create Raw Material',
                description: 'Click "Add Material" to create your first raw material. Example: Name="Chicken Breast", Category="Meat", Unit="grams"',
                position: 'bottom',
                onNextClick: () => {
                    const link = document.querySelector('a[href*="raw_material_create"]');
                    if (link) {
                        saveTutorialProgress(4);
                        window.location.href = link.getAttribute('href') + '?tutorial=active';
                    }
                }
            }
        },

        // Step 6: Raw Material Form - User creates sample data
        {
            element: 'form',
            popover: {
                title: '📝 Add Sample Material',
                description: 'Fill in this form to create a sample raw material. You\'ll need:\n• Name: e.g., "Chicken Breast"\n• Category: e.g., "Meat"\n• Unit: e.g., "grams"\n\nAfter submitting, click Next to continue.',
                position: 'bottom'
            }
        },

        // Step 7: Record Consumption
        {
            element: 'button[onclick="toggleDropdown(\'materials-menu\')"]',
            popover: {
                title: '📊 Record Consumption',
                description: 'Now let\'s record daily consumption. Click the Raw Materials dropdown again to access the consumption section.',
                position: 'bottom',
                onNextClick: () => {
                    const btn = document.querySelector('button[onclick="toggleDropdown(\'materials-menu\')"]');
                    if (btn) btn.click();
                }
            }
        },

        // Step 8: Navigate to Consumption Create
        {
            element: '#materials-menu a[href*="consumption_create"]',
            popover: {
                title: '➕ Record Consumption',
                description: 'Click here to record today\'s consumption of the material you just created.',
                position: 'right',
                onNextClick: () => {
                    const link = document.querySelector('#materials-menu a[href*="consumption_create"]');
                    if (link) {
                        saveTutorialProgress(7);
                        window.location.href = link.getAttribute('href') + '?tutorial=active';
                    }
                }
            }
        },

        // Step 9: Consumption Form - User enters data
        {
            element: 'form',
            popover: {
                title: '📝 Track Material Usage',
                description: 'Fill in this form to record consumption:\n• Material: Select the material you created\n• Quantity: Enter today\'s usage (e.g., "500")\n\nThis helps you track what\'s being used daily.',
                position: 'bottom'
            }
        },

        // Step 10: Product Types Setup
        {
            element: 'button[onclick="toggleDropdown(\'production-menu\')"]',
            popover: {
                title: '🏭 Production Section',
                description: 'Now let\'s set up your product types. These are the items you produce. Click on the Production dropdown.',
                position: 'bottom',
                onNextClick: () => {
                    const btn = document.querySelector('button[onclick="toggleDropdown(\'production-menu\')"]');
                    if (btn) btn.click();
                }
            }
        },

        // Step 11: Add Product Type
        {
            element: '#production-menu a[href*="product_type"]',
            popover: {
                title: '📋 Product Types',
                description: 'Click "Product Types" to see your product catalog. Let\'s add a new product type.',
                position: 'right',
                onNextClick: () => {
                    const link = document.querySelector('#production-menu a[href*="product_type_list"]');
                    if (link) {
                        saveTutorialProgress(10);
                        window.location.href = link.getAttribute('href') + '?tutorial=active';
                    }
                }
            }
        },

        // Step 12: Create Product Type Form
        {
            element: 'a[href*="product_type_create"]',
            popover: {
                title: '➕ Add Product Type',
                description: 'Click "Add Product Type" and create a sample product:\n• Name: e.g., "Food Pack"\n• Description: e.g., "Standard meal pack"\n\nClick Next after creating it.',
                position: 'bottom',
                onNextClick: () => {
                    const link = document.querySelector('a[href*="product_type_create"]');
                    if (link) {
                        saveTutorialProgress(11);
                        window.location.href = link.getAttribute('href') + '?tutorial=active';
                    }
                }
            }
        },

        // Step 13: Production Recording
        {
            element: 'button[onclick="toggleDropdown(\'production-menu\')"]',
            popover: {
                title: '📈 Record Production',
                description: 'Let\'s record daily production output. Click the Production dropdown to access production recording.',
                position: 'bottom',
                onNextClick: () => {
                    const btn = document.querySelector('button[onclick="toggleDropdown(\'production-menu\')"]');
                    if (btn) btn.click();
                }
            }
        },

        // Step 14: Production Form
        {
            element: '#production-menu a[href*="production_create"]',
            popover: {
                title: '➕ Record Production',
                description: 'Click here to record production for today.',
                position: 'right',
                onNextClick: () => {
                    const link = document.querySelector('#production-menu a[href*="production_create"]');
                    if (link) {
                        saveTutorialProgress(13);
                        window.location.href = link.getAttribute('href') + '?tutorial=active';
                    }
                }
            }
        },

        // Step 15: Customers
        {
            element: 'button[onclick="toggleDropdown(\'sales-menu\')"]',
            popover: {
                title: '👥 Sales & Orders',
                description: 'Now let\'s set up customers and orders. Click the Sales dropdown.',
                position: 'bottom',
                onNextClick: () => {
                    const btn = document.querySelector('button[onclick="toggleDropdown(\'sales-menu\')"]');
                    if (btn) btn.click();
                }
            }
        },

        // Step 16: Customer List
        {
            element: '#sales-menu a[href*="customer_list"]',
            popover: {
                title: '👥 Customers',
                description: 'Click here to manage your customer database. All purchase orders are linked to customers.',
                position: 'right',
                onNextClick: () => {
                    const link = document.querySelector('#sales-menu a[href*="customer_list"]');
                    if (link) {
                        saveTutorialProgress(15);
                        window.location.href = link.getAttribute('href') + '?tutorial=active';
                    }
                }
            }
        },

        // Step 17: Add Customer
        {
            element: 'a[href*="customer_create"]',
            popover: {
                title: '➕ Create Customer',
                description: 'Click "Add Customer" to create a sample customer:\n• Name: e.g., "ABC Restaurant"\n• Contact: e.g., "555-1234"',
                position: 'bottom',
                onNextClick: () => {
                    const link = document.querySelector('a[href*="customer_create"]');
                    if (link) {
                        saveTutorialProgress(16);
                        window.location.href = link.getAttribute('href') + '?tutorial=active';
                    }
                }
            }
        },

        // Step 18: Orders
        {
            element: 'button[onclick="toggleDropdown(\'sales-menu\')"]',
            popover: {
                title: '📋 Purchase Orders',
                description: 'Let\'s create a purchase order. Click the Sales dropdown again.',
                position: 'bottom',
                onNextClick: () => {
                    const btn = document.querySelector('button[onclick="toggleDropdown(\'sales-menu\')"]');
                    if (btn) btn.click();
                }
            }
        },

        // Step 19: Create Order
        {
            element: '#sales-menu a[href*="purchase_order_create"]',
            popover: {
                title: '📋 New Order',
                description: 'Click "New Order" to create a sample purchase order with the customer and product you created.',
                position: 'right',
                onNextClick: () => {
                    const link = document.querySelector('#sales-menu a[href*="purchase_order_create"]');
                    if (link) {
                        saveTutorialProgress(18);
                        window.location.href = link.getAttribute('href') + '?tutorial=active';
                    }
                }
            }
        },

        // Step 20: Order Detail & Fulfillment
        {
            element: '.flex.justify-between',
            popover: {
                title: '✅ Track Order Progress',
                description: 'After creating an order, you\'ll see the fulfillment progress here. You can:\n• View all items and their status\n• Add delivery updates\n• Track fulfillment percentage\n• Auto-update status when fully fulfilled',
                position: 'bottom'
            }
        },

        // Step 21: Profile & Settings
        {
            element: '.relative.group:last-child',
            popover: {
                title: '👤 Profile & Settings',
                description: 'Click your profile avatar in the top-right to access:\n• Your profile information\n• Change password\n• Logout',
                position: 'bottom'
            }
        },

        // Step 22: Tutorial Complete
        {
            element: '.bg-gradient-to-r.from-blue-50',
            popover: {
                title: '🎉 Tutorial Complete!',
                description: 'Congratulations! You\'ve completed the tutorial.\n\nSample data created:\n✓ 1 Raw Material\n✓ 1 Consumption Entry\n✓ 1 Product Type\n✓ 1 Production Entry\n✓ 1 Customer\n✓ 1 Purchase Order\n\nYou can delete this data from each section, or keep it as examples.\n\nYou can restart this tutorial anytime from the Tutorial button in the navigation bar.',
                position: 'bottom'
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

// Add completion event listener when Driver.js is done
document.addEventListener('driver.finished', () => {
    completeTutorial();
});
