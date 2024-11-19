# ITRA Race Results Analyzer 🏃‍♂️

A web application for extracting and analyzing race results from the International Trail Running Association (ITRA) website. The application provides both a Flask-based web interface and a Streamlit dashboard for comprehensive race data analysis.

## Features

### Web Interface (Flask)
- Extract race results from ITRA race URLs
- Display runner information including:
  - Position
  - Name
  - Finish Time
  - Age
  - Gender
  - Nationality
  - ITRA Profile Link
- Clean and responsive UI with topographic background
- Loading states and error handling

### Analytics Dashboard (Streamlit)
- Interactive data visualization
- Performance analysis charts:
  - Race Time vs ITRA Performance Index
  - Finish Time vs Position scatter plot
  - Age Distribution histogram
- Multiple filtering options:
  - Gender
  - Nationality
  - Age Groups
- Downloadable results table

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/greenbean1/itra-race-estimator.git
cd itra-race-estimator
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the Flask application:
```bash
python main.py
```
The Flask app will be available at `http://localhost:5000`

4. Run the Streamlit dashboard:
```bash
streamlit run streamlit_app.py
```
The Streamlit dashboard will be available at `http://localhost:8501`

## Example Usage

1. Visit either the Flask web interface or Streamlit dashboard
2. Enter an ITRA race results URL, for example:
   `https://itra.run/Races/RaceResults/70K/2024/94006`
3. Click "Get Results" or "Analyze Results" to fetch and display the data
4. For the Streamlit dashboard:
   - Use the filters to analyze specific runner groups
   - Interact with the charts to explore patterns
   - Download the results table for further analysis

## Technologies Used
- Flask (Web Framework)
- Streamlit (Analytics Dashboard)
- Beautiful Soup 4 (Web Scraping)
- Pandas (Data Processing)
- Plotly (Data Visualization)
- Bootstrap (UI Components)
