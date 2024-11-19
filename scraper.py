import requests
from bs4 import BeautifulSoup
from typing import Dict, List
from urllib.parse import urljoin

def scrape_itra_results(url: str) -> List[Dict]:
    """
    Scrapes ITRA race results for top 3 runners.
    Returns a list of dictionaries containing runner information.
    """
    try:
        # Validate URL
        if not url or not url.startswith(('http://', 'https://')):
            raise ValueError("Invalid URL format")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }

        # Make request with timeout and error handling
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.Timeout:
            raise Exception("Request timed out. Please try again.")
        except requests.ConnectionError:
            raise Exception("Failed to connect to the server. Please check your internet connection.")
        except requests.RequestException as e:
            raise Exception(f"Network error occurred: {str(e)}")

        soup = BeautifulSoup(response.text, 'html.parser')
        results = []

        # Find the results container (adjust based on ITRA's structure)
        # Note: These selectors need to be updated with actual ITRA HTML structure
        runners_table = soup.select_one('.race-results-table, .results-container table')
        if not runners_table:
            raise Exception("Could not find results table on the page")

        runners = runners_table.select('tbody tr')[:3]  # Get top 3 runners
        
        for index, runner in enumerate(runners, 1):
            try:
                # Extract profile link if available
                name_cell = runner.select_one('td.runner-name, td.athlete-name')
                profile_link = name_cell.find('a') if name_cell else None
                profile_url = urljoin(url, profile_link['href']) if profile_link and profile_link.get('href') else 'N/A'
                
                # Extract all required fields with fallback to N/A
                result = {
                    'position': str(index),
                    'name': (name_cell.get_text(strip=True) if name_cell else 'N/A'),
                    'profile_link': profile_url,
                    'time': (runner.select_one('td.finish-time, td.time').get_text(strip=True) 
                            if runner.select_one('td.finish-time, td.time') else 'N/A'),
                    'age': (runner.select_one('td.age').get_text(strip=True) 
                           if runner.select_one('td.age') else 'N/A'),
                    'gender': (runner.select_one('td.gender').get_text(strip=True) 
                             if runner.select_one('td.gender') else 'N/A'),
                    'nationality': (runner.select_one('td.nationality').get_text(strip=True) 
                                  if runner.select_one('td.nationality') else 'N/A')
                }
                results.append(result)
            except AttributeError:
                # Handle missing data for individual runner
                continue

        if not results:
            raise Exception("No valid results found on the page")

        return results

    except Exception as e:
        raise Exception(f"Failed to scrape results: {str(e)}")
