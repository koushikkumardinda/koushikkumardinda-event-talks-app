# BigQuery Release Notes Explorer 🚀

A full-stack web application designed to fetch, categorize, and visualize Google Cloud BigQuery release notes. It provides data professionals with an intuitive timeline UI to track features, changes, and deprecations, complete with built-in X (Twitter) integration for seamless community sharing.

The backend is powered by Python and Flask, utilizing `BeautifulSoup4` to parse Google's official XML feed and an in-memory caching system to ensure lightning-fast load times.

## ✨ Key Features

* **📡 Live XML Parsing:** The backend automatically fetches and parses the official BigQuery release notes feed.
* **⚡ Smart API Caching:** Built-in 5-minute backend caching prevents rate-limiting and ensures instant frontend loading, with a manual refresh override.
* **🔍 Advanced Filtering & Search:** Instantly filter release notes by category (Feature, Change, Deprecation, Notice) or use keyword search.
* **📅 Interactive Timeline:** View updates in a beautifully structured, chronological timeline format with color-coded badges.
* **🐦 X (Twitter) Integration:** Select single or multiple updates using the "Bulk Share" feature and seamlessly draft posts using the custom built-in Tweet Composer modal.
* **🎨 Modern UI/UX:** Features a dark-mode glassmorphism design, smooth CSS animations, and custom toast notifications.

## 🛠️ Tech Stack

* **Backend:** Python, Flask, BeautifulSoup4
* **Frontend:** HTML5, CSS3 (Custom Variables, Grid/Flexbox), Vanilla JavaScript
* **Data Source:** Google Cloud BigQuery RSS/XML Feed

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3.8+ installed. 

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/koushikkumardinda/koushikkumardinda-event-talks-app.git](https://github.com/koushikkumardinda/koushikkumardinda-event-talks-app.git)
   cd koushikkumardinda-event-talks-app
