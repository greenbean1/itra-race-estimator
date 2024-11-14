# ITRA Performance Index Scraper

A Python-based web scraper designed to extract ITRA (International Trail Running Association) performance index data from runner profiles.

## Features

- Direct ITRA profile URL support (itra.run/RunnerSpace/[runner]/[id])
- CSS selector-based data extraction
- Performance index retrieval
- Runner name extraction
- Streamlit web interface

## Local Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run main.py
```

2. Enter a valid ITRA profile URL in one of these formats:
   - `https://itra.run/RunnerSpace/[runner]/[id]`
   - `https://itra.run/api/RunnerSpace/GetRunnerSpace?memberString=[encoded_string]`

3. Click "Get Performance Index" to retrieve the data.

## Deployment to Streamlit Cloud

1. Fork this repository to your GitHub account.

2. Visit [Streamlit Cloud](https://share.streamlit.io) and sign in with your GitHub account.

3. Click on "New app" and select this repository.

4. Set the following deployment settings:
   - Main file path: `main.py`
   - Python version: 3.11

5. Click "Deploy!" and wait for the deployment to complete.

## Project Structure

- `main.py`: Streamlit web interface
- `scraper.py`: Core scraping functionality
- `.streamlit/config.toml`: Streamlit configuration
- `requirements.txt`: Project dependencies

## License

MIT License
