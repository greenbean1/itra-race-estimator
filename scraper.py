import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
import re
import json

class ItraScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def extract_performance_index(self, url: str) -> Dict[str, Optional[str]]:
        """
        Extract ITRA performance index from a runner's profile URL
        Returns a dictionary with performance index and runner name
        """
        try:
            # Validate URL format
            if not self._is_valid_itra_url(url):
                return {
                    'success': False,
                    'error': 'Invalid ITRA URL format',
                    'performance_index': None,
                    'runner_name': None
                }

            # Check if it's an API URL
            if 'api/RunnerSpace' in url:
                return self._extract_from_api(url)
            else:
                return self._extract_from_html(url)

        except requests.RequestException as e:
            return {
                'success': False,
                'error': f'Network error: {str(e)}',
                'performance_index': None,
                'runner_name': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'performance_index': None,
                'runner_name': None
            }

    def _extract_from_api(self, url: str) -> Dict[str, Optional[str]]:
        """
        Extract performance index from API endpoint
        """
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        
        try:
            data = response.json()
            
            # Extract performance index from JSON response
            if 'runnerSpace' in data and 'performanceIndex' in data['runnerSpace']:
                performance_index = str(data['runnerSpace']['performanceIndex'])
                runner_name = data['runnerSpace'].get('fullName', 'Unknown Runner')
                
                return {
                    'success': True,
                    'error': None,
                    'performance_index': performance_index,
                    'runner_name': runner_name
                }
            else:
                return {
                    'success': False,
                    'error': 'Performance index not found in API response',
                    'performance_index': None,
                    'runner_name': None
                }
        except json.JSONDecodeError:
            return {
                'success': False,
                'error': 'Invalid JSON response from API',
                'performance_index': None,
                'runner_name': None
            }

    def _extract_from_html(self, url: str) -> Dict[str, Optional[str]]:
        """
        Extract performance index from HTML page
        """
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract performance index using the new selector
        performance_element = soup.find('span', class_='level-count')
        if not performance_element:
            return {
                'success': False,
                'error': 'Performance index not found',
                'performance_index': None,
                'runner_name': None
            }

        # Extract runner name
        name_element = soup.find('h1', class_='runner-name') or soup.find('div', class_='runner-title')
        runner_name = name_element.text.strip() if name_element else 'Unknown Runner'

        # Extract the numeric value
        performance_text = performance_element.text.strip()
        performance_index = re.search(r'\d+', performance_text)
        
        if not performance_index:
            return {
                'success': False,
                'error': 'Could not parse performance index',
                'performance_index': None,
                'runner_name': runner_name
            }

        return {
            'success': True,
            'error': None,
            'performance_index': performance_index.group(),
            'runner_name': runner_name
        }

    def _is_valid_itra_url(self, url: str) -> bool:
        """
        Validate if the URL is a valid ITRA profile URL
        """
        itra_patterns = [
            r'https?://itra\.run/RunnerSpace/[^/]+/\d+',
            r'https?://itra\.run/api/RunnerSpace/GetRunnerSpace\?memberString=[^/]+',
            r'https?://www\.itra\.run/RunnerSpace/[^/]+/\d+'
        ]
        return any(re.match(pattern, url) for pattern in itra_patterns)
