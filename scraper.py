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

        # Find the results table using the specific ID
        runners_table = soup.select_one('#RunnerRaceResults')
        if not runners_table:
            raise Exception("Could not find results table on the page")

        # Get top 3 runners (skip header row)
        runners = runners_table.select('tbody tr')[:3]
        
        for index, runner in enumerate(runners, 1):
            try:
                # Get all td elements
                columns = runner.find_all('td')
                if len(columns) < 7:  # Ensure we have all required columns
                    continue

                # Extract profile link and name from second column
                name_cell = columns[1]
                profile_link = name_cell.find('a')
                
                # Process profile link
                if profile_link and profile_link.get('href'):
                    profile_url = urljoin('https://itra.run', profile_link['href'])
                else:
                    profile_url = 'N/A'
                
                # Extract name (text after the img tag)
                name = profile_link.get_text(strip=True) if profile_link else 'N/A'
                
                # Extract nationality (text after the img tag in last column)
                nationality_cell = columns[-1]
                nationality = nationality_cell.get_text(strip=True) if nationality_cell else 'N/A'
                
                # Build result dictionary with all required fields
                result = {
                    'position': str(index),
                    'name': name,
                    'profile_link': profile_url,
                    'time': columns[2].get_text(strip=True) if len(columns) > 2 else 'N/A',
                    'age': columns[4].get_text(strip=True) if len(columns) > 4 else 'N/A',
                    'gender': columns[5].get_text(strip=True) if len(columns) > 5 else 'N/A',
                    'nationality': nationality
                }
                results.append(result)
            except AttributeError as e:
                # Handle missing data for individual runner
                continue

        if not results:
            raise Exception("No valid results found on the page")

        return results

    except Exception as e:
        raise Exception(f"Failed to scrape results: {str(e)}")
