import requests
from bs4 import BeautifulSoup
from typing import Dict, List
from urllib.parse import urljoin
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
            logger.debug("HTML content: %s", soup.prettify())
            raise Exception("Could not find results table on the page")

        # Get top 3 runners (skip header, get next 3 rows)
        runners = runners_table.select('tr')[1:4]
        
        for runner in runners:
            try:
                # Get all td elements
                columns = runner.find_all('td')
                logger.debug("Processing runner row with %d columns", len(columns))
                logger.debug("Row HTML structure: %s", runner.prettify())

                # Extract values with debug logging
                position = columns[0].get_text(strip=True)
                logger.debug("Extracted position: %s", position)

                # Extract profile link and name from second column
                name_cell = columns[1]
                profile_link = name_cell.find('a')
                
                # Process profile link and name
                if profile_link and profile_link.get('href'):
                    profile_url = urljoin('https://itra.run', profile_link['href'])
                    name = profile_link.get_text(strip=True).strip()
                else:
                    profile_url = 'N/A'
                    name = 'N/A'
                logger.debug("Extracted name: %s, profile_url: %s", name, profile_url)

                # Extract time
                time = columns[2].get_text(strip=True)
                logger.debug("Extracted time: %s", time)

                # Extract age (index 4 after race score column)
                age = columns[4].get_text(strip=True)
                logger.debug("Extracted age: %s", age)

                # Extract gender
                gender = columns[5].get_text(strip=True)
                logger.debug("Extracted gender: %s", gender)

                # Extract nationality
                nationality_cell = columns[6]
                nationality = nationality_cell.get_text(strip=True).split()[-1] if nationality_cell else 'N/A'
                logger.debug("Extracted nationality: %s", nationality)
                
                # Build result dictionary with all required fields
                result = {
                    'position': position,
                    'name': name,
                    'profile_link': profile_url,
                    'time': time,
                    'age': age,
                    'gender': gender,
                    'nationality': nationality
                }
                results.append(result)
                logger.debug("Successfully added result for runner: %s", name)
            except (AttributeError, IndexError) as e:
                logger.error("Error processing runner row: %s", str(e))
                logger.debug("Row HTML structure: %s", runner.prettify())
                continue

        if not results:
            logger.debug("Table HTML structure: %s", runners_table.prettify())
            raise Exception("No valid results found on the page")

        logger.debug("Successfully extracted %d results", len(results))
        return results

    except Exception as e:
        logger.error("Scraping error: %s", str(e))
        raise Exception(f"Failed to scrape results: {str(e)}")
