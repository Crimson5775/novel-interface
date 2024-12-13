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

// Novel Management
async function getMyNovels() {
    try {
        const response = await fetch(`${API_BASE_URL}/novels?author=me`, {
            headers: getHeaders()
        });
        const data = await response.json();
        displayNovels(data.novels);
    } catch (error) {
        showError('Failed to fetch novels');
    }
}

function displayNovels(novels) {
    const container = document.querySelector('.novels-grid');
    container.innerHTML = '';

    novels.forEach(novel => {
        const div = document.createElement('div');
        div.className = 'novel-card';
        div.innerHTML = `
            <div class="novel-cover">
                <img src="${novel.cover_image || 'https://via.placeholder.com/150x200'}" alt="${novel.title}">
            </div>
            <div class="novel-info">
                <h3>${novel.title}</h3>
                <p>Chapters: ${novel.chapters_count || 0}</p>
                <p>Views: ${novel.views.toLocaleString()}</p>
                <div class="novel-actions">
                    <button class="edit-btn" onclick="editNovel(${novel.id})"><i class="fas fa-edit"></i> Edit</button>
                    <button class="add-chapter-btn" onclick="showAddChapter(${novel.id})"><i class="fas fa-plus"></i> Add Chapter</button>
                </div>
            </div>
        `;
        container.appendChild(div);
    });
}

async function addNovel(event) {
    event.preventDefault();
    const form = document.getElementById('add-novel-form');
    const formData = new FormData(form);

    try {
        const response = await fetch(`${API_BASE_URL}/novels`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`
            },
            body: formData
        });

        if (response.ok) {
            closeModal('add-novel-modal');
            getMyNovels();
            showSuccess('Novel added successfully');
        } else {
            const data = await response.json();
            showError(data.error);
        }
    } catch (error) {
        showError('Failed to add novel');
    }
}

async function addChapter(novelId, event) {
    event.preventDefault();
    const form = document.getElementById('add-chapter-form');
    const formData = new FormData(form);

    try {
        const response = await fetch(`${API_BASE_URL}/novels/${novelId}/chapters`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(Object.fromEntries(formData))
        });

        if (response.ok) {
            closeModal('add-chapter-modal');
            getMyNovels();
            showSuccess('Chapter added successfully');
        } else {
            const data = await response.json();
            showError(data.error);
        }
    } catch (error) {
        showError('Failed to add chapter');
    }
}

// Statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/novels/stats`, {
            headers: getHeaders()
        });
        const data = await response.json();
        updateStatistics(data);
    } catch (error) {
        showError('Failed to load statistics');
    }
}

function updateStatistics(stats) {
    document.querySelector('.stat-card:nth-child(1) p').textContent = stats.active_novels;
    document.querySelector('.stat-card:nth-child(2) p').textContent = stats.total_chapters;
    document.querySelector('.stat-card:nth-child(3) p').textContent = stats.total_views.toLocaleString();
}

// UI Helpers
function showModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function showAddChapter(novelId) {
    document.getElementById('add-chapter-form').dataset.novelId = novelId;
    showModal('add-chapter-modal');
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
    getMyNovels();
    loadStatistics();

    // Add event listeners for modals
    document.querySelector('.add-novel-btn').addEventListener('click', () => showModal('add-novel-modal'));
    document.querySelectorAll('.cancel-btn').forEach(btn => {
        btn.addEventListener('click', () => closeModal(btn.closest('.modal').id));
    });

    // Add form submissions
    document.getElementById('add-novel-form').addEventListener('submit', addNovel);
    document.getElementById('add-chapter-form').addEventListener('submit', (e) => {
        const novelId = e.target.dataset.novelId;
        addChapter(novelId, e);
    });
});
