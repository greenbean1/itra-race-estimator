import requests
from bs4 import BeautifulSoup
from typing import Dict, List
from urllib.parse import urljoin
import logging
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_performance_index(profile_url: str, headers: Dict) -> str:
    """
    Extracts the ITRA Performance Index from a runner's profile page.
    Returns 'N/A' if the index is not available or if an error occurs.
    """
    try:
        logger.debug(f"Fetching performance index from profile URL: {profile_url}")
        
        # Ensure proper URL joining
        if not profile_url.startswith(('http://', 'https://')):
            profile_url = urljoin('https://itra.run', profile_url)
            logger.debug(f"Updated profile URL to absolute URL: {profile_url}")

        response = requests.get(profile_url, headers=headers, timeout=10)
        response.raise_for_status()
        logger.debug(f"Profile page response status code: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try multiple selectors to find the performance index
        index_span = soup.find('span', class_='level-count')
        if not index_span:
            logger.debug("Performance index not found with class 'level-count', trying alternative selectors")
            # Try alternative selectors
            index_span = soup.find('span', class_='itra-index') or \
                        soup.find('div', class_='performance-index') or \
                        soup.find('div', text=lambda t: t and 'Performance Index' in t)

        if index_span:
            index_value = index_span.text.strip()
            logger.debug(f"Found performance index value: {index_value}")
            return index_value
        else:
            # Check if the content might be loaded via JavaScript
            logger.debug("Performance index not found in static HTML, checking for JavaScript data")
            script_data = soup.find('script', type='application/json')
            if script_data:
                try:
                    json_data = json.loads(script_data.string)
                    if 'performanceIndex' in json_data:
                        return str(json_data['performanceIndex'])
                except json.JSONDecodeError:
                    logger.error("Failed to parse JavaScript data")
            
            logger.warning(f"No performance index found for profile: {profile_url}")
            return 'N/A'

    except requests.Timeout:
        logger.error(f"Timeout while fetching profile: {profile_url}")
        return 'N/A'
    except requests.ConnectionError:
        logger.error(f"Connection error while fetching profile: {profile_url}")
        return 'N/A'
    except requests.RequestException as e:
        logger.error(f"Request error while fetching profile: {profile_url}, error: {str(e)}")
        return 'N/A'
    except Exception as e:
        logger.error(f"Unexpected error while fetching performance index: {str(e)}")
        return 'N/A'

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
                        # Fetch performance index from profile page
                        result['performance_index'] = get_performance_index(result['profile_link'], headers)
                        logger.debug("Extracted performance index: %s", result['performance_index'])
                    else:
                        result['profile_link'] = 'N/A'
                        result['name'] = 'N/A'
                        result['performance_index'] = 'N/A'
                except (IndexError, AttributeError):
                    result['profile_link'] = 'N/A'
                    result['name'] = 'N/A'
                    result['performance_index'] = 'N/A'
                logger.debug("Extracted name: %s, profile_link: %s", result['name'], result['profile_link'])

                # Extract time (index 2)
                try:
                    result['time'] = columns[2].get_text(strip=True)
                except (IndexError, AttributeError):
                    result['time'] = 'N/A'
                logger.debug("Extracted time: %s", result['time'])

                # After extracting time, check for and skip race score column
                race_score_cell = next((col for col in columns if 'rowspan' in col.attrs), None)
                if race_score_cell:
                    # Adjust column indices for remaining fields when race score cell is present
                    age_index = 4  # Skip the race score cell
                    gender_index = 5
                    nationality_index = 6
                else:
                    # Normal column indices when no race score cell
                    age_index = 3
                    gender_index = 4
                    nationality_index = 5

                # Use these dynamic indices for remaining extractions
                result['age'] = columns[age_index].get_text(strip=True) if len(columns) > age_index else 'N/A'
                result['gender'] = columns[gender_index].get_text(strip=True) if len(columns) > gender_index else 'N/A'
                result['nationality'] = columns[nationality_index].get_text(strip=True).split()[-1] if len(columns) > nationality_index else 'N/A'

                logger.debug("Extracted age: %s", result['age'])
                logger.debug("Extracted gender: %s", result['gender'])
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