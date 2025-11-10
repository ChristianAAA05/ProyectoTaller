// Function to get CSRF token from cookies
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

// Function to show alert message
function showAlert(type, message) {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    alertDiv.role = 'alert';
    alertDiv.style.zIndex = '1050';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Add to body
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Function to update task status
function cambiarEstadoTarea(tareaId, nuevoEstado) {
    const csrftoken = getCookie('csrftoken');
    
    // Show loading state
    const button = event.currentTarget;
    const originalHTML = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
    
    // Make the API call
    fetch(`/tareas/cambiar-estado/${tareaId}/${nuevoEstado}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin'
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw err; });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Find the task card
            const taskCard = document.querySelector(`.task-item[data-task-id="${tareaId}"]`);
            if (taskCard) {
                // Remove the task card from its current position
                taskCard.remove();
                
                // Show success message
                showAlert('success', 'Tarea actualizada correctamente');
                
                // Reload the page after a short delay to show the updated task list
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            }
        } else {
            throw new Error(data.error || 'Error al actualizar el estado');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('danger', error.message || 'Error al actualizar el estado');
    })
    .finally(() => {
        // Reset button state
        if (button) {
            button.disabled = false;
            button.innerHTML = originalHTML;
        }
    });
}

// Add event listeners when the document is ready
document.addEventListener('DOMContentLoaded', function() {
    // Add any initialization code here if needed
});
