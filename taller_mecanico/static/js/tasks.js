// Theme management
const ThemeManager = {
    init() {
        this.theme = localStorage.getItem('theme') || 'light';
        this.applyTheme();
        this.setupThemeToggle();
    },
    
    toggleTheme() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
        localStorage.setItem('theme', this.theme);
        this.applyTheme();
    },
    
    applyTheme() {
        document.documentElement.setAttribute('data-bs-theme', this.theme);
        const themeIcon = document.getElementById('theme-toggle-icon');
        if (themeIcon) {
            themeIcon.className = this.theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
        }
    },
    
    setupThemeToggle() {
        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggleTheme());
        }
    }
};

// Notification system
const NotificationManager = {
    show(type, message, duration = 5000) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
        alertDiv.role = 'alert';
        alertDiv.style.zIndex = '1050';
        alertDiv.style.transition = 'opacity 0.3s ease-in-out';
        alertDiv.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="${this.getIcon(type)} me-2"></i>
                <span>${message}</span>
            </div>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Auto-remove after duration
        setTimeout(() => {
            alertDiv.style.opacity = '0';
            setTimeout(() => alertDiv.remove(), 300);
        }, duration);
        
        return alertDiv;
    },
    
    getIcon(type) {
        const icons = {
            'success': 'fas fa-check-circle',
            'danger': 'fas fa-exclamation-circle',
            'warning': 'fas fa-exclamation-triangle',
            'info': 'fas fa-info-circle'
        };
        return icons[type] || 'fas fa-bell';
    }
};

// Utility functions
const Utils = {
    getCookie(name) {
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
    },
    
    async fetchWithCSRF(url, options = {}) {
        const csrftoken = this.getCookie('csrftoken');
        const defaultOptions = {
            credentials: 'same-origin',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json'
            },
            ...options
        };
        
        try {
            const response = await fetch(url, defaultOptions);
            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.message || 'Error en la solicitud');
            }
            return await response.json();
        } catch (error) {
            console.error('Fetch error:', error);
            throw error;
        }
    },
    
    debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }
};

// Repair management
const RepairManager = {
    // Initialize repair selection functionality
    init() {
        this.setupRepairSelection();
        this.setupActiveRepair();
    },

    // Setup event listeners for repair selection
    setupRepairSelection() {
        document.addEventListener('click', (e) => {
            const selectBtn = e.target.closest('.select-repair');
            if (selectBtn) {
                e.preventDefault();
                const repairId = selectBtn.dataset.repairId;
                const vehicle = selectBtn.dataset.vehicle;
                const client = selectBtn.dataset.client;
                this.selectRepair(repairId, vehicle, client);
            }
        });
    },

    // Handle repair selection
    async selectRepair(repairId, vehicle, client) {
        try {
            const response = await fetch(`/reparaciones/${repairId}/tomar/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': Utils.getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            });

            if (!response.ok) {
                throw new Error('Error al seleccionar la reparación');
            }

            const data = await response.json();
            
            if (data.success) {
                // Show success message
                NotificationManager.show('success', 'Reparación seleccionada correctamente');
                
                // Update UI to show active repair
                this.setActiveRepair(repairId, vehicle, client);
                
                // Reload the page after a short delay to update the list
                setTimeout(() => window.location.reload(), 1500);
            } else {
                throw new Error(data.message || 'Error al seleccionar la reparación');
            }
        } catch (error) {
            console.error('Error:', error);
            NotificationManager.show('danger', error.message || 'Error al seleccionar la reparación');
        }
    },

    // Set the active repair in the UI
    setActiveRepair(repairId, vehicle, client) {
        const activeRepairContainer = document.getElementById('active-repair-container');
        const noActiveRepair = document.getElementById('no-active-repair');
        const activeRepairDetails = document.getElementById('active-repair-details');
        const repairIdElement = document.getElementById('repair-id');
        const repairVehicleElement = document.getElementById('active-repair-vehicle');
        const repairClientElement = document.getElementById('active-repair-client');
        const activeRepairActions = document.getElementById('active-repair-actions');

        if (repairIdElement) repairIdElement.textContent = repairId;
        if (repairVehicleElement) repairVehicleElement.textContent = vehicle;
        if (repairClientElement) repairClientElement.textContent = client;

        if (noActiveRepair) noActiveRepair.classList.add('d-none');
        if (activeRepairDetails) activeRepairDetails.classList.remove('d-none');
        if (activeRepairActions) activeRepairActions.classList.remove('d-none');

        // Start the timer for the repair
        this.startRepairTimer();
    },

    // Start the repair timer
    startRepairTimer() {
        // Implementation for the repair timer
        // This can be expanded to track time spent on the repair
        console.log('Repair timer started');
    },

    // Setup active repair on page load
    setupActiveRepair() {
        // Check if there's an active repair in localStorage
        const activeRepair = localStorage.getItem('activeRepair');
        if (activeRepair) {
            try {
                const { id, vehicle, client, startTime } = JSON.parse(activeRepair);
                this.setActiveRepair(id, vehicle, client);
            } catch (e) {
                console.error('Error parsing active repair:', e);
                localStorage.removeItem('activeRepair');
            }
        }
    }
};

// Task management
const TaskManager = {
    async updateTaskStatus(taskId, newStatus, event) {
        const button = event?.currentTarget;
        const originalHTML = button?.innerHTML;
        
        try {
            // Show loading state
            if (button) {
                button.disabled = true;
                button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
            }
            
            // Make API call
            const data = await Utils.fetchWithCSRF(`/tareas/cambiar-estado/${taskId}/${newStatus}/`, {
                method: 'POST'
            });
            
            if (data.success) {
                const taskCard = document.querySelector(`.task-item[data-task-id="${taskId}"]`);
                if (taskCard) {
                    // Add animation class before removing
                    taskCard.style.transition = 'all 0.3s ease';
                    taskCard.style.opacity = '0';
                    taskCard.style.transform = 'translateX(100%)';
                    
                    // Remove after animation
                    setTimeout(() => {
                        taskCard.remove();
                        this.updateTaskCounts(-1);
                    }, 300);
                }
                
                NotificationManager.show('success', 'Tarea actualizada correctamente');
                
                // Update progress bars if they exist
                this.updateProgressBars();
            }
        } catch (error) {
            console.error('Error updating task:', error);
            NotificationManager.show('danger', error.message || 'Error al actualizar la tarea');
        } finally {
            if (button) {
                button.disabled = false;
                button.innerHTML = originalHTML;
            }
        }
    },
    
    updateTaskCounts(change = 0) {
        const countElements = document.querySelectorAll('.task-count');
        countElements.forEach(el => {
            const currentCount = parseInt(el.textContent) || 0;
            const newCount = Math.max(0, currentCount + change);
            el.textContent = newCount;
            
            // Add animation
            el.classList.add('animate__animated', 'animate__pulse');
            setTimeout(() => {
                el.classList.remove('animate__animated', 'animate__pulse');
            }, 1000);
        });
    },
    
    updateProgressBars() {
        document.querySelectorAll('.progress-bar').forEach(bar => {
            const progress = bar.getAttribute('aria-valuenow');
            bar.style.width = `${progress}%`;
            
            // Update color based on progress
            if (progress < 30) {
                bar.classList.remove('bg-warning', 'bg-success');
                bar.classList.add('bg-danger');
            } else if (progress < 70) {
                bar.classList.remove('bg-danger', 'bg-success');
                bar.classList.add('bg-warning');
            } else {
                bar.classList.remove('bg-danger', 'bg-warning');
                bar.classList.add('bg-success');
            }
        });
    },
    
    initTaskInteractions() {
        // Initialize tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
        
        // Initialize task cards
        document.querySelectorAll('.task-item').forEach(card => {
            card.addEventListener('click', (e) => {
                if (!e.target.matches('button, a, input, .btn, .form-check-input')) {
                    card.classList.toggle('active-task');
                }
            });
        });
    }
};

// Initialize everything when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme manager
    ThemeManager.init();
    
    // Initialize task manager
    TaskManager.initTaskInteractions();
    TaskManager.updateProgressBars();
    
    // Initialize repair manager
    if (typeof RepairManager !== 'undefined') {
        RepairManager.init();
    }
    
    // Hide loading overlay if it's still visible
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
    }
    
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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
    
    // Initialize any tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Add animation on scroll
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.animate-on-scroll');
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementTop < windowHeight - 100) {
                element.classList.add('animate__animated', 'animate__fadeInUp');
            }
        });
    };
    
    // Initial check
    animateOnScroll();
    
    // Check on scroll
    window.addEventListener('scroll', Utils.debounce(animateOnScroll, 100));
    
    // Initialize any charts if needed
    if (typeof initCharts === 'function') {
        initCharts();
    }
});

// Expose functions to global scope for HTML onclick attributes
window.cambiarEstadoTarea = (tareaId, nuevoEstado, event) => {
    TaskManager.updateTaskStatus(tareaId, nuevoEstado, event);
};
