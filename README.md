# 🌍 World Clock

A beautiful, interactive world clock that displays real-time clocks for different time zones across the globe on an interactive world map.

![World Clock Demo](https://img.shields.io/badge/Demo-Live-green)

## Features

### 🗺️ Interactive World Map
- Click on different regions to add time zones
- Visual indicators show active time zones
- Hover effects for better user experience
- Time overlays directly on the map

### ⏰ Real-Time Clocks
- Live updating every second
- 12-hour format with AM/PM
- Full date display including day of week
- Clean, modern card design

### 🌐 Comprehensive Time Zone Support
- 25+ popular time zones included
- Major cities from all continents
- Accurate IANA time zone identifiers
- Automatic daylight saving time handling

### 🎨 Modern UI/UX
- Beautiful gradient background
- Glass-morphism design elements
- Smooth animations and transitions
- Fully responsive design
- Dark theme optimized

### 🚀 Interactive Features
- Add time zones via dropdown selector
- Click map regions to add zones
- Remove individual clocks
- Clear all clocks at once
- Keyboard shortcuts support

## How to Use

### Getting Started
1. Open `index.html` in your web browser
2. The application loads with three default time zones: New York, London, and Tokyo

### Adding Time Zones
**Method 1: Click the Map**
- Click on any colored region on the world map
- The corresponding time zone will be automatically added

**Method 2: Use the Dropdown**
- Click the "+ Add Time Zone" button
- Select from 25+ available time zones
- Click "Add" to confirm

### Managing Clocks
- **Remove individual clocks**: Click the "×" button on any clock card
- **Clear all clocks**: Click the "Clear All" button
- **View on map**: Each active time zone shows a small clock overlay on the map

### Keyboard Shortcuts
- `Ctrl + A`: Open time zone selector
- `Ctrl + Shift + C`: Clear all time zones
- `Escape`: Close time zone selector

## Technical Details

### Technologies Used
- **HTML5**: Semantic structure and SVG map
- **CSS3**: Modern styling with backdrop-filter and animations
- **Vanilla JavaScript**: ES6+ classes and modern APIs
- **Intl.DateTimeFormat API**: Accurate time zone handling

### Browser Compatibility
- Chrome 88+
- Firefox 85+
- Safari 14+
- Edge 88+

### Performance Features
- Efficient 1-second update interval
- Minimal DOM manipulation
- CSS-based animations
- Responsive grid layout

## File Structure

```
world-clock/
├── index.html          # Main HTML structure
├── styles.css          # All styling and animations
├── script.js           # JavaScript functionality
└── README.md          # Documentation
```

## Supported Time Zones

The application includes these major time zones:

**Americas**
- New York (EST/EDT)
- Los Angeles (PST/PDT)  
- Chicago (CST/CDT)
- Denver (MST/MDT)
- São Paulo (BRT/BRST)
- Buenos Aires (ART)
- Hawaii (HST)

**Europe**
- London (GMT/BST)
- Paris (CET/CEST)
- Berlin (CET/CEST)
- Rome (CET/CEST)
- Moscow (MSK)

**Asia Pacific**
- Tokyo (JST)
- Shanghai (CST)
- Mumbai (IST)
- Seoul (KST)
- Bangkok (ICT)
- Singapore (SGT)
- Dubai (GST)
- Sydney (AEDT/AEST)
- Melbourne (AEDT/AEST)
- Auckland (NZDT/NZST)

**Africa**
- Cairo (EET/EEST)
- Lagos (WAT)
- Johannesburg (SAST)

## Features in Detail

### Real-Time Updates
The application updates all displayed times every second using JavaScript's `setInterval`. The `Intl.DateTimeFormat` API ensures accurate time zone conversions and automatically handles daylight saving time transitions.

### Interactive Map
The world map is created using SVG paths representing major geographical regions. Each region is clickable and associated with specific time zone data.

### Responsive Design
The layout adapts to different screen sizes:
- Desktop: Multi-column grid layout
- Tablet: Flexible grid with fewer columns  
- Mobile: Single column stack

### Modern Styling
- Glass-morphism effects with `backdrop-filter`
- CSS Grid for responsive layouts
- Smooth CSS transitions and animations
- Professional color scheme and typography

## Browser Support Notes

This application uses modern web APIs and CSS features:
- `Intl.DateTimeFormat` for time zone handling
- `backdrop-filter` for glass effects
- CSS Grid for layouts
- ES6+ JavaScript features

For the best experience, use a modern, up-to-date web browser.

## License

This project is open source and available under the MIT License.

---

Enjoy tracking time around the world! 🌍⏰