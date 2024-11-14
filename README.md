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

## Manual Deployment to Streamlit Cloud

### Prerequisites
- A GitHub account
- A Streamlit Cloud account (sign up at https://share.streamlit.io)

### Step 1: Prepare Your Repository
1. Fork this repository to your GitHub account:
   - Visit the repository page
   - Click the "Fork" button in the top-right corner
   - Select your account as the destination

### Step 2: Connect to Streamlit Cloud
1. Visit [Streamlit Cloud](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app" in the top-right corner

### Step 3: Configure Deployment
1. Select your forked repository from the list
2. Configure the deployment settings:
   - Main file path: `main.py`
   - Python version: 3.11
   - Branch: `main` (or your default branch)

### Step 4: Deploy
1. Click "Deploy!"
2. Wait for the deployment process to complete
3. Your app will be available at: `https://[your-app-name].streamlit.app`

### Troubleshooting
- If the deployment fails, check the build logs in Streamlit Cloud
- Verify that all dependencies are correctly listed in `requirements.txt`
- Ensure the Python version matches (3.11)
- Check if all environment variables are properly set

## Project Structure

- `main.py`: Streamlit web interface
- `scraper.py`: Core scraping functionality
- `.streamlit/config.toml`: Streamlit configuration
- `requirements.txt`: Project dependencies

## License

MIT License
