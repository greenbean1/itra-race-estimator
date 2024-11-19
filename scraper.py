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

                result = {}

                # Extract position (index 0)
                try:
                    result['position'] = columns[0].get_text(strip=True)
                except (IndexError, AttributeError):
                    result['position'] = 'N/A'
                logger.debug("Extracted position: %s", result['position'])

                # Extract name and profile link (index 1)
                try:
                    name_cell = columns[1]
                    profile_link = name_cell.find('a')
                    if profile_link and profile_link.get('href'):
                        result['profile_link'] = urljoin('https://itra.run', profile_link['href'])
                        result['name'] = profile_link.get_text(strip=True).strip()
                    else:
                        result['profile_link'] = 'N/A'
                        result['name'] = 'N/A'
                except (IndexError, AttributeError):
                    result['profile_link'] = 'N/A'
                    result['name'] = 'N/A'
                logger.debug("Extracted name: %s, profile_link: %s", result['name'], result['profile_link'])

                # Extract time (index 2)
                try:
                    result['time'] = columns[2].get_text(strip=True)
                except (IndexError, AttributeError):
                    result['time'] = 'N/A'
                logger.debug("Extracted time: %s", result['time'])

                # Extract age (index 3, accounting for rowspan)
                try:
                    result['age'] = columns[3].get_text(strip=True)
                except (IndexError, AttributeError):
                    result['age'] = 'N/A'
                logger.debug("Extracted age: %s", result['age'])

                # Extract gender (index 4)
                try:
                    result['gender'] = columns[4].get_text(strip=True)
                except (IndexError, AttributeError):
                    result['gender'] = 'N/A'
                logger.debug("Extracted gender: %s", result['gender'])

                # Extract nationality (index 5)
                try:
                    nationality_cell = columns[5]
                    result['nationality'] = nationality_cell.get_text(strip=True).split()[-1] if nationality_cell else 'N/A'
                except (IndexError, AttributeError):
                    result['nationality'] = 'N/A'
                logger.debug("Extracted nationality: %s", result['nationality'])

                results.append(result)
                logger.debug("Successfully added result for runner: %s", result['name'])

            except Exception as e:
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
