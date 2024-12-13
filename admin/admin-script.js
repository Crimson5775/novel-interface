// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';
let authToken = localStorage.getItem('authToken');

// Authentication Functions
function setAuthToken(token) {
    authToken = token;
    localStorage.setItem('authToken', token);
}

function getHeaders() {
    return {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
    };
}

// Translator Management
async function getTranslators() {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/translators`, {
            headers: getHeaders()
        });
        const data = await response.json();
        displayTranslators(data.translators);
    } catch (error) {
        showError('Failed to fetch translators');
    }
}

function displayTranslators(translators) {
    const tbody = document.querySelector('.translators-list tbody');
    tbody.innerHTML = '';

    translators.forEach(translator => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${translator.username}</td>
            <td>${translator.email}</td>
            <td><span class="status ${translator.is_active ? 'active' : 'blocked'}">${translator.is_active ? 'Active' : 'Blocked'}</span></td>
            <td>${translator.novels_count || 0}</td>
            <td class="actions">
                <button class="edit-btn" onclick="editTranslator(${translator.id})"><i class="fas fa-edit"></i></button>
                <button class="block-btn" onclick="toggleTranslatorStatus(${translator.id}, ${translator.is_active})">
                    <i class="fas ${translator.is_active ? 'fa-ban' : 'fa-check'}"></i>
                </button>
                <button class="delete-btn" onclick="deleteTranslator(${translator.id})"><i class="fas fa-trash"></i></button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function addTranslator(event) {
    event.preventDefault();
    const form = document.getElementById('add-translator-form');
    const formData = new FormData(form);

    try {
        const response = await fetch(`${API_BASE_URL}/admin/translators`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(Object.fromEntries(formData))
        });

        if (response.ok) {
            closeModal('add-translator-modal');
            getTranslators();
            showSuccess('Translator added successfully');
        } else {
            const data = await response.json();
            showError(data.error);
        }
    } catch (error) {
        showError('Failed to add translator');
    }
}

async function toggleTranslatorStatus(translatorId, currentStatus) {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/translators/${translatorId}`, {
            method: 'PUT',
            headers: getHeaders(),
            body: JSON.stringify({ is_active: !currentStatus })
        });

        if (response.ok) {
            getTranslators();
            showSuccess(`Translator ${currentStatus ? 'blocked' : 'activated'} successfully`);
        } else {
            const data = await response.json();
            showError(data.error);
        }
    } catch (error) {
        showError('Failed to update translator status');
    }
}

async function deleteTranslator(translatorId) {
    if (!confirm('Are you sure you want to delete this translator?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/admin/translators/${translatorId}`, {
            method: 'DELETE',
            headers: getHeaders()
        });

        if (response.ok) {
            getTranslators();
            showSuccess('Translator deleted successfully');
        } else {
            const data = await response.json();
            showError(data.error);
        }
    } catch (error) {
        showError('Failed to delete translator');
    }
}

// User Management
async function getUsers(page = 1) {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/users?page=${page}`, {
            headers: getHeaders()
        });
        const data = await response.json();
        displayUsers(data.users);
        updatePagination(data.current_page, data.pages);
    } catch (error) {
        showError('Failed to fetch users');
    }
}

function displayUsers(users) {
    const tbody = document.querySelector('.users-list tbody');
    tbody.innerHTML = '';

    users.forEach(user => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${user.username}</td>
            <td>${user.email}</td>
            <td><span class="status ${user.is_active ? 'active' : 'blocked'}">${user.is_active ? 'Active' : 'Blocked'}</span></td>
            <td>${new Date(user.created_at).toLocaleDateString()}</td>
            <td class="actions">
                <button class="view-btn" onclick="viewUser(${user.id})"><i class="fas fa-eye"></i></button>
                <button class="block-btn" onclick="toggleUserStatus(${user.id}, ${user.is_active})">
                    <i class="fas ${user.is_active ? 'fa-ban' : 'fa-check'}"></i>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function toggleUserStatus(userId, currentStatus) {
    try {
        const response = await fetch(`${API_BASE_URL}/admin/users/${userId}`, {
            method: 'PUT',
            headers: getHeaders(),
            body: JSON.stringify({ is_active: !currentStatus })
        });

        if (response.ok) {
            getUsers();
            showSuccess(`User ${currentStatus ? 'blocked' : 'activated'} successfully`);
        } else {
            const data = await response.json();
            showError(data.error);
        }
    } catch (error) {
        showError('Failed to update user status');
    }
}

// UI Helpers
function showModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function showSuccess(message) {
    // Implement your success notification
    console.log('Success:', message);
}

function showError(message) {
    // Implement your error notification
    console.error('Error:', message);
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize data
    getTranslators();
    getUsers();

    // Add event listeners for modals
    document.querySelector('.add-translator-btn').addEventListener('click', () => showModal('add-translator-modal'));
    document.querySelectorAll('.cancel-btn').forEach(btn => {
        btn.addEventListener('click', () => closeModal(btn.closest('.modal').id));
    });

    // Add form submissions
    document.getElementById('add-translator-form').addEventListener('submit', addTranslator);
});
