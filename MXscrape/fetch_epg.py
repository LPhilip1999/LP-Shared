import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import os

def run_scraper():
    url = "https://web.metaxplay.tv/api/epg" 
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Ensure script stays in its directory
    base_path = os.path.dirname(__file__)
    xml_path = os.path.join(base_path, "guide.xml")
    txt_path = os.path.join(base_path, "tvg-ids.txt")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        
        root = ET.Element("tv", {"generator-info-name": "MetaXPlay-Scraper"})
        
        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(f"# MetaXPlay TVG-ID List (.metax) - Updated {datetime.now()}\n\n")
            
            for item in data.get('channels', []):
                raw_id = item.get('id', 'unknown')
                channel_id = f"{raw_id}.metax" # Adding your requested suffix
                channel_name = item.get('name', 'Unknown Channel')
                
                txt_file.write(f"ID: {channel_id} | Name: {channel_name}\n")
                
                channel_node = ET.SubElement(root, "channel", id=channel_id)
                ET.SubElement(channel_node, "display-name").text = channel_name
                
                for prog in item.get('programs', []):
                    p = ET.SubElement(root, "programme", 
                                    channel=channel_id, 
                                    start=prog['start'], 
                                    stop=prog['end'])
                    ET.SubElement(p, "title").text = prog.get('title', 'No Title')

        tree = ET.ElementTree(root)
        tree.write(xml_path, encoding="utf-8", xml_declaration=True)
        print("Successfully updated Scraper/guide.xml and Scraper/tvg-ids.txt")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_scraper()
