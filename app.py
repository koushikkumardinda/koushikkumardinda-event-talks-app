# /// script
# dependencies = [
#   "flask",
#   "requests",
#   "beautifulsoup4",
# ]
# ///

import os
import urllib.request
import xml.etree.ElementTree as ET
from flask import Flask, jsonify, render_template, request
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

FEED_URL = "https://docs.cloud.google.com/feeds/bigquery-release-notes.xml"

# In-memory cache for feed data
_cache = {
    "data": None,
    "timestamp": 0
}
CACHE_TTL = 300 # 5 minutes

def parse_feed_xml(xml_content):
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    root = ET.fromstring(xml_content)
    
    feed_title_el = root.find('atom:title', ns)
    feed_title = feed_title_el.text if feed_title_el is not None else "BigQuery Release Notes"
    
    feed_updated_el = root.find('atom:updated', ns)
    feed_updated = feed_updated_el.text if feed_updated_el is not None else ""
    
    entries = []
    for entry_el in root.findall('atom:entry', ns):
        title_el = entry_el.find('atom:title', ns)
        date_str = title_el.text if title_el is not None else "Unknown Date"
        
        id_el = entry_el.find('atom:id', ns)
        entry_id = id_el.text if id_el is not None else ""
        
        updated_el = entry_el.find('atom:updated', ns)
        updated = updated_el.text if updated_el is not None else ""
        
        # Link extraction
        link_el = entry_el.find("atom:link[@rel='alternate']", ns)
        if link_el is None:
            link_el = entry_el.find("atom:link", ns)
        link = link_el.get('href') if link_el is not None else ""
        
        content_el = entry_el.find('atom:content', ns)
        content_html = content_el.text if content_el is not None else ""
        
        # Parse HTML content into separate updates
        soup = BeautifulSoup(content_html, 'html.parser')
        updates = []
        current_type = "Update"
        current_nodes = []
        
        for child in soup.children:
            if child.name == 'h3':
                if current_nodes:
                    html_str = ''.join(str(c) for c in current_nodes).strip()
                    if html_str:
                        text_str = BeautifulSoup(html_str, 'html.parser').get_text().strip()
                        updates.append({
                            'type': current_type,
                            'html': html_str,
                            'text': text_str
                        })
                    current_nodes = []
                current_type = child.get_text().strip()
            else:
                current_nodes.append(child)
                
        # Handle trailing update elements
        if current_nodes:
            html_str = ''.join(str(c) for c in current_nodes).strip()
            if html_str:
                text_str = BeautifulSoup(html_str, 'html.parser').get_text().strip()
                updates.append({
                    'type': current_type,
                    'html': html_str,
                    'text': text_str
                })
                
        # Fallback if no h3 structure was detected
        if not updates and content_html.strip():
            updates.append({
                'type': 'Update',
                'html': content_html,
                'text': soup.get_text().strip()
            })
            
        entries.append({
            'date': date_str,
            'id': entry_id,
            'updated': updated,
            'link': link,
            'updates': updates
        })
        
    return {
        'title': feed_title,
        'updated': feed_updated,
        'entries': entries
    }

def fetch_feed_data(bypass_cache=False):
    current_time = time.time()
    if not bypass_cache and _cache["data"] and (current_time - _cache["timestamp"] < CACHE_TTL):
        return _cache["data"], True

    try:
        # Fetching XML feed
        req = urllib.request.Request(
            FEED_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            xml_data = response.read()
            
        parsed_data = parse_feed_xml(xml_data)
        
        # Update Cache
        _cache["data"] = parsed_data
        _cache["timestamp"] = current_time
        return parsed_data, False
    except Exception as e:
        # Fallback to cache if error occurs, otherwise raise error
        if _cache["data"]:
            return _cache["data"], True
        raise e

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/notes')
def get_notes():
    bypass_cache = request.args.get('refresh', 'false').lower() == 'true'
    try:
        data, from_cache = fetch_feed_data(bypass_cache)
        return jsonify({
            'success': True,
            'data': data,
            'cached': from_cache
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Run server locally on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
