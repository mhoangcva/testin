class WorldClock {
    constructor() {
        this.activeTimezones = new Set();
        this.updateInterval = null;
        this.availableTimezones = [
            { name: 'New York', timezone: 'America/New_York' },
            { name: 'Los Angeles', timezone: 'America/Los_Angeles' },
            { name: 'Chicago', timezone: 'America/Chicago' },
            { name: 'Denver', timezone: 'America/Denver' },
            { name: 'London', timezone: 'Europe/London' },
            { name: 'Paris', timezone: 'Europe/Paris' },
            { name: 'Berlin', timezone: 'Europe/Berlin' },
            { name: 'Rome', timezone: 'Europe/Rome' },
            { name: 'Moscow', timezone: 'Europe/Moscow' },
            { name: 'Dubai', timezone: 'Asia/Dubai' },
            { name: 'Mumbai', timezone: 'Asia/Kolkata' },
            { name: 'Shanghai', timezone: 'Asia/Shanghai' },
            { name: 'Tokyo', timezone: 'Asia/Tokyo' },
            { name: 'Seoul', timezone: 'Asia/Seoul' },
            { name: 'Sydney', timezone: 'Australia/Sydney' },
            { name: 'Melbourne', timezone: 'Australia/Melbourne' },
            { name: 'Auckland', timezone: 'Pacific/Auckland' },
            { name: 'Hawaii', timezone: 'Pacific/Honolulu' },
            { name: 'São Paulo', timezone: 'America/Sao_Paulo' },
            { name: 'Buenos Aires', timezone: 'America/Argentina/Buenos_Aires' },
            { name: 'Cairo', timezone: 'Africa/Cairo' },
            { name: 'Lagos', timezone: 'Africa/Lagos' },
            { name: 'Johannesburg', timezone: 'Africa/Johannesburg' },
            { name: 'Bangkok', timezone: 'Asia/Bangkok' },
            { name: 'Singapore', timezone: 'Asia/Singapore' }
        ];
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.addDefaultTimezones();
        this.startUpdating();
    }
    
    setupEventListeners() {
        // Map region clicks
        document.querySelectorAll('.region').forEach(region => {
            region.addEventListener('click', (e) => {
                const timezone = e.target.dataset.timezone;
                const regionName = e.target.dataset.region;
                if (timezone && regionName) {
                    this.addTimezone(regionName, timezone);
                    this.highlightRegion(e.target);
                }
            });
        });
        
        // Control buttons
        document.getElementById('addTimezone').addEventListener('click', () => {
            this.showTimezoneSelector();
        });
        
        document.getElementById('clearAll').addEventListener('click', () => {
            this.clearAllTimezones();
        });
    }
    
    addDefaultTimezones() {
        // Add some default timezones
        this.addTimezone('New York', 'America/New_York');
        this.addTimezone('London', 'Europe/London');
        this.addTimezone('Tokyo', 'Asia/Tokyo');
    }
    
    addTimezone(name, timezone) {
        const timezoneKey = `${name}-${timezone}`;
        if (this.activeTimezones.has(timezoneKey)) {
            return; // Already exists
        }
        
        this.activeTimezones.add(timezoneKey);
        this.createClockCard(name, timezone);
        this.createMapClock(name, timezone);
    }
    
    createClockCard(name, timezone) {
        const clockGrid = document.getElementById('clockGrid');
        const clockCard = document.createElement('div');
        clockCard.className = 'clock-card';
        clockCard.style.position = 'relative';
        clockCard.dataset.timezone = timezone;
        clockCard.dataset.name = name;
        
        clockCard.innerHTML = `
            <button class="close-btn" onclick="worldClock.removeTimezone('${name}', '${timezone}')">&times;</button>
            <h3>${name}</h3>
            <div class="time" data-time></div>
            <div class="date" data-date></div>
            <div class="timezone">${timezone}</div>
        `;
        
        clockGrid.appendChild(clockCard);
        this.updateClockCard(clockCard, timezone);
    }
    
    createMapClock(name, timezone) {
        // Find the corresponding region on the map
        const region = document.querySelector(`[data-region="${name}"]`);
        if (!region) return;
        
        const timezoneClocks = document.getElementById('timezoneClocks');
        const mapClock = document.createElement('div');
        mapClock.className = 'map-clock';
        mapClock.dataset.timezone = timezone;
        mapClock.dataset.name = name;
        
        // Position the clock near the region
        const bbox = region.getBBox();
        const centerX = bbox.x + bbox.width / 2;
        const centerY = bbox.y + bbox.height / 2;
        
        mapClock.style.left = `${(centerX / 1000) * 100}%`;
        mapClock.style.top = `${(centerY / 500) * 100}%`;
        
        timezoneClocks.appendChild(mapClock);
        this.updateMapClock(mapClock, timezone, name);
    }
    
    updateClockCard(clockCard, timezone) {
        const now = new Date();
        const timeElement = clockCard.querySelector('[data-time]');
        const dateElement = clockCard.querySelector('[data-date]');
        
        if (timeElement && dateElement) {
            const timeFormatter = new Intl.DateTimeFormat('en-US', {
                timeZone: timezone,
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: true
            });
            
            const dateFormatter = new Intl.DateTimeFormat('en-US', {
                timeZone: timezone,
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
            
            timeElement.textContent = timeFormatter.format(now);
            dateElement.textContent = dateFormatter.format(now);
        }
    }
    
    updateMapClock(mapClock, timezone, name) {
        const now = new Date();
        const timeFormatter = new Intl.DateTimeFormat('en-US', {
            timeZone: timezone,
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        });
        
        mapClock.innerHTML = `
            <strong>${name}</strong><br>
            ${timeFormatter.format(now)}
        `;
    }
    
    removeTimezone(name, timezone) {
        const timezoneKey = `${name}-${timezone}`;
        this.activeTimezones.delete(timezoneKey);
        
        // Remove clock card
        const clockCard = document.querySelector(`[data-timezone="${timezone}"][data-name="${name}"]`);
        if (clockCard) {
            clockCard.remove();
        }
        
        // Remove map clock
        const mapClock = document.querySelector(`.map-clock[data-timezone="${timezone}"][data-name="${name}"]`);
        if (mapClock) {
            mapClock.remove();
        }
        
        // Remove region highlight
        const region = document.querySelector(`[data-region="${name}"]`);
        if (region) {
            region.classList.remove('active');
        }
    }
    
    clearAllTimezones() {
        this.activeTimezones.clear();
        document.getElementById('clockGrid').innerHTML = '';
        document.getElementById('timezoneClocks').innerHTML = '';
        document.querySelectorAll('.region').forEach(region => {
            region.classList.remove('active');
        });
    }
    
    highlightRegion(region) {
        region.classList.add('active');
    }
    
    showTimezoneSelector() {
        const overlay = document.createElement('div');
        overlay.className = 'overlay';
        
        const selector = document.createElement('div');
        selector.className = 'timezone-selector';
        
        selector.innerHTML = `
            <h3>Add Time Zone</h3>
            <select id="timezoneSelect">
                <option value="">Select a timezone...</option>
                ${this.availableTimezones.map(tz => 
                    `<option value="${tz.timezone}">${tz.name} (${tz.timezone})</option>`
                ).join('')}
            </select>
            <div class="btn-group">
                <button class="btn" onclick="worldClock.addSelectedTimezone()">Add</button>
                <button class="btn btn-secondary" onclick="worldClock.closeTimezoneSelector()">Cancel</button>
            </div>
        `;
        
        document.body.appendChild(overlay);
        document.body.appendChild(selector);
        
        // Close on overlay click
        overlay.addEventListener('click', () => {
            this.closeTimezoneSelector();
        });
    }
    
    addSelectedTimezone() {
        const select = document.getElementById('timezoneSelect');
        const selectedValue = select.value;
        
        if (selectedValue) {
            const selectedOption = this.availableTimezones.find(tz => tz.timezone === selectedValue);
            if (selectedOption) {
                this.addTimezone(selectedOption.name, selectedOption.timezone);
            }
        }
        
        this.closeTimezoneSelector();
    }
    
    closeTimezoneSelector() {
        const overlay = document.querySelector('.overlay');
        const selector = document.querySelector('.timezone-selector');
        
        if (overlay) overlay.remove();
        if (selector) selector.remove();
    }
    
    updateAllClocks() {
        // Update clock cards
        document.querySelectorAll('.clock-card').forEach(clockCard => {
            const timezone = clockCard.dataset.timezone;
            if (timezone) {
                this.updateClockCard(clockCard, timezone);
            }
        });
        
        // Update map clocks
        document.querySelectorAll('.map-clock').forEach(mapClock => {
            const timezone = mapClock.dataset.timezone;
            const name = mapClock.dataset.name;
            if (timezone && name) {
                this.updateMapClock(mapClock, timezone, name);
            }
        });
    }
    
    startUpdating() {
        this.updateAllClocks();
        this.updateInterval = setInterval(() => {
            this.updateAllClocks();
        }, 1000);
    }
    
    stopUpdating() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }
}

// Initialize the world clock when the page loads
let worldClock;

document.addEventListener('DOMContentLoaded', () => {
    worldClock = new WorldClock();
});

// Clean up when the page is unloaded
window.addEventListener('beforeunload', () => {
    if (worldClock) {
        worldClock.stopUpdating();
    }
});

// Add some utility functions for better user experience
function getCurrentTime(timezone) {
    return new Intl.DateTimeFormat('en-US', {
        timeZone: timezone,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
    }).format(new Date());
}

function getCurrentDate(timezone) {
    return new Intl.DateTimeFormat('en-US', {
        timeZone: timezone,
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date());
}

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        worldClock.closeTimezoneSelector();
    } else if (e.key === 'a' && e.ctrlKey) {
        e.preventDefault();
        worldClock.showTimezoneSelector();
    } else if (e.key === 'c' && e.ctrlKey && e.shiftKey) {
        e.preventDefault();
        worldClock.clearAllTimezones();
    }
});