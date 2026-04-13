// Category Configuration
const categories = {
    'SECURITY': { label: 'IT-SECURITY', color: 'security', icon: '🔒' },
    'ZERODAY': { label: 'ZERODAY', color: 'zeroday', icon: '💣' },
    'CLOUD': { label: 'CLOUD', color: 'cloud', icon: '☁️' },
    'AI': { label: 'AI/MACHINE LEARNING', color: 'ai', icon: '🤖' },
    'HARDWARE': { label: 'HARDWARE', color: 'hardware', icon: '⚙️' }
};

// Format timestamp to relative time
function formatTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000);

    if (diff < 60) return `${diff}s ago`;
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    if (diff < 604800) return `${Math.floor(diff / 86400)}d ago`;
    
    return date.toLocaleDateString();
}

// Update metadata (date, count, last update)
function updateMetadata() {
    const now = new Date();
    document.getElementById('current-date').textContent = `DATE: ${now.toLocaleDateString('en-US', { 
        year: 'numeric', month: '2-digit', day: '2-digit' 
    })} / TIME: ${now.toLocaleTimeString('en-US', { 
        hour: '2-digit', minute: '2-digit', second: '2-digit'
    })}`;
    
    document.getElementById('feed-count').textContent = `ITEMS: ${newsData.length}`;
    document.getElementById('last-update').textContent = `LAST UPDATE: ${now.toLocaleTimeString()}`;
}

// Update category counts
function updateCategoryCounts() {
    const counts = {
        SECURITY: 0,
        ZERODAY: 0,
        CLOUD: 0,
        AI: 0,
        HARDWARE: 0
    };

    newsData.forEach(item => {
        if (item.category in counts) {
            counts[item.category]++;
        }
    });

    Object.entries(counts).forEach(([cat, count]) => {
        const elem = document.getElementById(`count-${cat.toLowerCase()}`);
        if (elem) {
            elem.textContent = `${count} Item${count !== 1 ? 's' : ''}`;
        }
    });
}

// Close modal on overlay click
function setupModalEvents() {
    document.getElementById('modalOverlay').addEventListener('click', (e) => {
        if (e.target === document.getElementById('modalOverlay')) {
            closeDashboard();
        }
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeDashboard();
        }
    });
}

// Filter news by category
function filterNewsByCategory(category) {
    return newsData.filter(item => item.category === category);
}

// Get category stats
function getCategoryStats(category) {
    const items = filterNewsByCategory(category);
    return {
        total: items.length,
        critical: items.filter(i => i.priority === 'CRITICAL').length,
        warning: items.filter(i => i.priority === 'WARNING').length,
        info: items.filter(i => i.priority === 'INFO').length
    };
}
