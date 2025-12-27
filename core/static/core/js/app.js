/**
 * Cebu Best Value Trading - Kitchen Management System
 * Main Application JavaScript
 */

// Toggle dropdown menus
function toggleDropdown(id) {
  const menu = document.getElementById(id);
  if (menu) {
    menu.classList.toggle('show');
  }
}

// Close dropdowns when clicking outside
document.addEventListener('click', function(event) {
  // Don't close if clicking on nav items or their children
  if (event.target.closest('.nav-item') || event.target.closest('.dropdown-trigger')) {
    return;
  }

  // Close all open menus
  document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
    menu.classList.remove('show');
  });
});

// Toggle mobile menu
function toggleMobileMenu() {
  const menu = document.getElementById('mobile-menu');
  if (menu) {
    menu.classList.toggle('show');
  }
}

// Close mobile menu when clicking a link
document.querySelectorAll('.mobile-menu-item').forEach(item => {
  item.addEventListener('click', function() {
    const menu = document.getElementById('mobile-menu');
    if (menu) {
      menu.classList.remove('show');
    }
  });
});

// Update active mobile nav item
document.addEventListener('DOMContentLoaded', function() {
  const currentPath = window.location.pathname;
  document.querySelectorAll('.mobile-nav-item').forEach(item => {
    if (item.getAttribute('href') === currentPath) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  });
});

// Form validation and error handling
function validateForm(formElement) {
  let isValid = true;
  const inputs = formElement.querySelectorAll('[required]');

  inputs.forEach(input => {
    if (!input.value.trim()) {
      showFieldError(input, 'This field is required');
      isValid = false;
    } else {
      clearFieldError(input);
    }
  });

  return isValid;
}

function showFieldError(element, message) {
  const group = element.closest('.form-group') || element.parentElement;
  group.classList.add('error');

  let errorElement = group.querySelector('.form-error');
  if (!errorElement) {
    errorElement = document.createElement('span');
    errorElement.className = 'form-error';
    element.after(errorElement);
  }
  errorElement.textContent = message;
}

function clearFieldError(element) {
  const group = element.closest('.form-group') || element.parentElement;
  group.classList.remove('error');

  const errorElement = group.querySelector('.form-error');
  if (errorElement) {
    errorElement.remove();
  }
}

// Add smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Loading state for buttons
document.querySelectorAll('.btn').forEach(button => {
  button.addEventListener('click', function() {
    if (this.closest('form')) {
      this.disabled = true;
    }
  });
});

// Prevent multiple form submissions
document.querySelectorAll('form').forEach(form => {
  form.addEventListener('submit', function(e) {
    const submitBtn = this.querySelector('[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = true;
      setTimeout(() => {
        submitBtn.disabled = false;
      }, 5000); // Re-enable after 5 seconds in case of error
    }
  });
});

// Format currency fields
function formatCurrency(input) {
  let value = input.value.replace(/[^\d]/g, '');
  if (value) {
    value = (parseInt(value) / 100).toFixed(2);
    input.value = '₱ ' + value;
  }
}

// Format phone number fields
function formatPhoneNumber(input) {
  let value = input.value.replace(/[^\d]/g, '');
  if (value.length > 0) {
    if (value.length <= 3) {
      input.value = value;
    } else if (value.length <= 6) {
      input.value = value.slice(0, 3) + '-' + value.slice(3);
    } else {
      input.value = value.slice(0, 3) + '-' + value.slice(3, 6) + '-' + value.slice(6, 10);
    }
  }
}

// Debounce function for search inputs
function debounce(func, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func.apply(this, args), delay);
  };
}

// Auto-save form data to localStorage (optional)
function autoSaveForm(formElement) {
  const formKey = 'form_' + (formElement.id || formElement.name || Math.random());

  // Load saved data on page load
  const savedData = localStorage.getItem(formKey);
  if (savedData) {
    const data = JSON.parse(savedData);
    Object.keys(data).forEach(key => {
      const input = formElement.querySelector(`[name="${key}"]`);
      if (input) {
        input.value = data[key];
      }
    });
  }

  // Save data on input change
  formElement.addEventListener('change', function() {
    const formData = new FormData(this);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });
    localStorage.setItem(formKey, JSON.stringify(data));
  });

  // Clear saved data on successful submit
  formElement.addEventListener('submit', function() {
    localStorage.removeItem(formKey);
  });
}

// Disable auto-save by default (opt-in with data-autosave attribute)
document.querySelectorAll('form[data-autosave]').forEach(form => {
  autoSaveForm(form);
});

// Toast notification helper
function showToast(message, type = 'info', duration = 3000) {
  const toast = document.createElement('div');
  toast.className = `message message-${type}`;
  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    max-width: 400px;
    z-index: 1000;
    animation: slideDown 0.3s ease;
  `;
  toast.innerHTML = `<span>${message}</span>`;

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'slideUp 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// Confirm delete helper
function confirmDelete(event, message = 'Are you sure?') {
  if (!confirm(message)) {
    event.preventDefault();
  }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
  // Add smooth fade-in to page content
  document.body.style.animation = 'fadeIn 0.3s ease';

  // Add keyboard shortcuts (Ctrl+K for search, etc.)
  document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for command palette or search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      // Implement as needed
    }
  });
});
