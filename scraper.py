import requests
from bs4 import BeautifulSoup
from typing import Dict, List

def scrape_itra_results(url: str) -> List[Dict]:
    """
    Scrapes ITRA race results for top 3 runners.
    Returns a list of dictionaries containing runner information.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # Find the results table (adjust selectors based on actual ITRA website structure)
        runners = soup.select('table.results-table tr')[:4]  # First 3 runners + header
        
        for runner in runners[1:]:  # Skip header row
            cols = runner.select('td')
            if len(cols) >= 4:
                result = {
                    'position': cols[0].get_text(strip=True) or 'N/A',
                    'name': cols[1].get_text(strip=True) or 'N/A',
                    'time': cols[2].get_text(strip=True) or 'N/A',
                    'category': cols[3].get_text(strip=True) or 'N/A'
                }
                results.append(result)
                
        return results
    except Exception as e:
        raise Exception(f"Failed to scrape results: {str(e)}")
