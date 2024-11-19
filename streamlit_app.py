import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import trafilatura
from scraper import scrape_itra_results
import os

# Ensure the PORT environment variable is set
os.environ['PORT'] = '8501'

# Page configuration
st.set_page_config(
    page_title="Trail Race Results",
    page_icon="🏃",
    layout="wide"
)

# Simple styling
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

def normalize_time(time_str):
    try:
        # Convert HH:MM:SS to seconds since race start
        if time_str == 'N/A':
            return None
        time_parts = time_str.split(':')
        total_seconds = int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + int(time_parts[2])
        return total_seconds
    except (ValueError, IndexError):
        return None

def get_age_bucket(age):
    try:
        if age == 'N/A':
            return 'Unknown'
        age = int(age)
        return f"{(age // 10) * 10}-{(age // 10) * 10 + 9}"
    except (ValueError, TypeError):
        return 'Unknown'

def format_time(seconds):
    if seconds is None:
        return 'N/A'
    return str(timedelta(seconds=seconds))

# Title and Description
st.title("🏃 Trail Race Results Analyzer")
st.markdown("""
Extract and analyze race results from ITRA (International Trail Running Association).
Enter a race results URL below to get started.
""")

# URL input with example
url = st.text_input(
    "Enter ITRA race results URL",
    placeholder="https://itra.run/Races/RaceResults/70K/2024/94006",
    help="Example: https://itra.run/Races/RaceResults/70K/2024/94006"
)

# Submit button
if st.button("📊 Analyze Results"):
    if url:
        try:
            with st.spinner("🔄 Fetching race results..."):
                results = scrape_itra_results(url)
                
                if results:
                    # Convert results to DataFrame
                    df = pd.DataFrame(results)
                    
                    # Convert time strings to normalized seconds
                    df['time_seconds'] = df['time'].apply(normalize_time)
                    
                    # Create age buckets
                    df['age_group'] = df['age'].apply(get_age_bucket)
                    
                    # Display results table
                    st.subheader("📊 Race Results")
                    
                    # Format the display DataFrame
                    display_df = df.copy()
                    display_df['time'] = display_df['time_seconds'].apply(format_time)
                    
                    st.dataframe(
                        display_df[[
                            'position', 'name', 'time', 'performance_index',
                            'age', 'gender', 'nationality'
                        ]],
                        column_config={
                            "performance_index": "ITRA Index",
                            "time": "Finish Time",
                        },
                        hide_index=True,
                    )

                    # Add filters in columns
                    st.subheader("🔍 Filter Results")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        selected_genders = st.multiselect(
                            'Gender Filter',
                            options=sorted(df['gender'].unique()),
                            default=sorted(df['gender'].unique())
                        )
                    
                    with col2:
                        selected_nations = st.multiselect(
                            'Nationality Filter',
                            options=sorted(df['nationality'].unique()),
                            default=sorted(df['nationality'].unique())
                        )
                    
                    with col3:
                        selected_age_groups = st.multiselect(
                            'Age Group Filter',
                            options=sorted(df['age_group'].unique()),
                            default=sorted(df['age_group'].unique())
                        )

                    # Filter data based on selections
                    filtered_df = df[
                        df['gender'].isin(selected_genders) &
                        df['nationality'].isin(selected_nations) &
                        df['age_group'].isin(selected_age_groups)
                    ]

                    # Create visualizations
                    if not filtered_df.empty:
                        st.subheader("📈 Performance Analysis")
                        
                        # Time vs Position plot
                        fig1 = px.scatter(
                            filtered_df,
                            x='time_seconds',
                            y='position',
                            color='gender',
                            hover_data=['name', 'age', 'nationality'],
                            title='Finish Time vs Position',
                            labels={'time_seconds': 'Finish Time (HH:MM:SS)',
                                   'position': 'Position'}
                        )
                        fig1.update_traces(marker=dict(size=10))
                        st.plotly_chart(fig1, use_container_width=True)
                        
                        # Age distribution
                        fig2 = px.histogram(
                            filtered_df,
                            x='age_group',
                            color='gender',
                            title='Age Distribution',
                            labels={'age_group': 'Age Group',
                                   'count': 'Number of Runners'}
                        )
                        st.plotly_chart(fig2, use_container_width=True)
                    else:
                        st.warning("No data available for the selected filters.")
                else:
                    st.warning("No results found. Please check the URL and try again.")
                    
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.error("Please enter a valid ITRA race results URL")

# Footer
st.markdown("""
---
💡 **Tip**: The analysis includes finish times, age groups, and nationality distributions.
You can use the filters above to focus on specific groups of runners.
""")
