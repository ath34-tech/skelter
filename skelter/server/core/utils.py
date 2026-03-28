import re
import json
import os
import sys
from pathlib import Path

def get_asset_path(relative_path: str) -> Path:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path(os.path.abspath("."))

    return base_path / relative_path

def clean_json_response(content: str) -> dict:
    json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
    if json_match:
        content = json_match.group(1)
    else:
        json_match = re.search(r'```\s*(.*?)\s*```', content, re.DOTALL)
        if json_match:
            content = json_match.group(1)
            
    content = content.strip()
    
    if not (content.startswith('{') and content.endswith('}')):
        start = content.find('{')
        end = content.rfind('}')
        if start != -1 and end != -1:
            content = content[start:end+1]
            
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON. Raw content: {content}")
        raise e
