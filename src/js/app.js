// Initialize on page load
function init() {
    renderMainFeed();
    updateMetadata();
    updateCategoryCounts();
    setupModalEvents();
}

// Render Main Feed - shows empty state, news only in modals
function renderMainFeed() {
    const container = document.getElementById('feed-container');
    container.innerHTML = `
        <div class="empty-state" style="grid-column: 1 / -1;">
            <div class="empty-state-icon">🦀</div>
            <div class="empty-state-text">ClawFeed</div>
            <div class="empty-state-subtext">Click a category above to view news</div>
        </div>
    `;
}

// Create News Item Element
function createNewsElement(item) {
    const article = document.createElement('div');
    article.className = 'news-item';
    
    const catInfo = categories[item.category];
    const bgClass = catInfo ? catInfo.color : 'security';

    article.innerHTML = `
        <div class="news-header">
            <div class="news-category ${bgClass}">
                ${item.category}
            </div>
            <div class="news-priority">${item.priority}</div>
        </div>
        <div class="news-title">${escapeHtml(item.title)}</div>
        <div class="news-description">${escapeHtml(item.description)}</div>
        <div class="news-tags">
            ${item.tags.map(tag => `<span class="tag">#${tag}</span>`).join('')}
        </div>
        <div class="news-footer">
            <span class="news-source">${escapeHtml(item.source)}</span>
            <span class="news-time">${formatTime(item.timestamp)}</span>
        </div>
    `;

    article.addEventListener('click', () => {
        openDashboard(item.category);
    });

    return article;
}

// Open Dashboard Modal
function openDashboard(category) {
    const overlay = document.getElementById('modalOverlay');
    const modal = document.getElementById('modalContent');
    
    const catInfo = categories[category];
    const items = filterNewsByCategory(category);

    const colorClass = catInfo.color;

    let modalContent = `
        <div class="modal-header">
            <div>
                <span style="font-size: 2rem; margin-right: 15px;">${catInfo.icon}</span>
                <div class="modal-title">${catInfo.label}</div>
            </div>
            <button class="modal-close" onclick="closeDashboard()">✕</button>
        </div>
    `;

    if (items.length === 0) {
        modalContent += `
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <div class="empty-state-text">No items in this category</div>
                <div class="empty-state-subtext">Items will appear here once added</div>
            </div>
        `;
    } else {
        modalContent += `
            <div class="modal-filters">
                <button class="filter-btn active" onclick="filterModal('all', '${category}')">All</button>
                <button class="filter-btn" onclick="filterModal('critical', '${category}')">Critical</button>
                <button class="filter-btn" onclick="filterModal('warning', '${category}')">Warning</button>
                <button class="filter-btn" onclick="filterModal('info', '${category}')">Info</button>
            </div>

            <div class="modal-feed" id="modalFeed">
                ${items.map(item => `
                    <div class="modal-news-item ${colorClass}">
                        <div class="modal-news-title">${escapeHtml(item.title)}</div>
                        <div class="modal-news-desc">${escapeHtml(item.description)}</div>
                        <div class="modal-news-meta">
                            <span><strong>Priority:</strong> ${item.priority}</span>
                            <span><strong>Source:</strong> ${escapeHtml(item.source)}</span>
                            <span><strong>Time:</strong> ${formatTime(item.timestamp)}</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    modal.className = `modal ${colorClass}`;
    modal.innerHTML = modalContent;

    overlay.classList.add('active');
}

// Close Dashboard Modal
function closeDashboard() {
    document.getElementById('modalOverlay').classList.remove('active');
}

// Filter Modal Items
function filterModal(type, category) {
    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    // Filter and render items
    const items = filterNewsByCategory(category);
    const catInfo = categories[category];
    const colorClass = catInfo.color;
    
    let filteredItems = items;
    if (type !== 'all') {
        filteredItems = items.filter(i => i.priority === type.toUpperCase());
    }

    const feedContainer = document.getElementById('modalFeed');
    
    if (filteredItems.length === 0) {
        feedContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <div class="empty-state-text">No ${type} items in this category</div>
            </div>
        `;
    } else {
        feedContainer.innerHTML = filteredItems.map(item => `
            <div class="modal-news-item ${colorClass}">
                <div class="modal-news-title">${escapeHtml(item.title)}</div>
                <div class="modal-news-desc">${escapeHtml(item.description)}</div>
                <div class="modal-news-meta">
                    <span><strong>Priority:</strong> ${item.priority}</span>
                    <span><strong>Source:</strong> ${escapeHtml(item.source)}</span>
                    <span><strong>Time:</strong> ${formatTime(item.timestamp)}</span>
                </div>
            </div>
        `).join('');
    }
}

// Escape HTML for security
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Initialize on load
window.addEventListener('load', init);

// Auto-update metadata every second
setInterval(updateMetadata, 1000);
