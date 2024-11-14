# ITRA Performance Index Scraper

A Python-based web scraper designed to extract ITRA (International Trail Running Association) performance index data from runner profiles.

## Features

- Direct ITRA profile URL support (itra.run/RunnerSpace/[runner]/[id])
- CSS selector-based data extraction
- Performance index retrieval
- Runner name extraction
- Streamlit web interface

## Installation

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

## Project Structure

- `main.py`: Streamlit web interface
- `scraper.py`: Core scraping functionality
- `.streamlit/config.toml`: Streamlit configuration

## License

MIT License
