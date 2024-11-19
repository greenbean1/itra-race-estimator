import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from scraper import scrape_itra_results

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
</style>
""", unsafe_allow_html=True)

def normalize_time(time_str):
    try:
        # Convert HH:MM:SS to seconds since race start
        if time_str == 'N/A':
            return 'N/A'
        time_parts = time_str.split(':')
        return str(timedelta(hours=int(time_parts[0]), minutes=int(time_parts[1]), seconds=int(time_parts[2])))
    except (ValueError, IndexError):
        return 'N/A'

def get_age_bucket(age):
    try:
        if age == 'N/A':
            return 'Unknown'
        age = int(age)
        return f"{(age // 10) * 10}-{(age // 10) * 10 + 9}"
    except (ValueError, TypeError):
        return 'Unknown'

# Title
st.title("Trail Race Results")

# URL input
url = st.text_input(
    "Enter ITRA race results URL",
    placeholder="https://itra.run/Races/RaceResults/..."
)

# Submit button
if st.button("Get Results"):
    if url:
        try:
            with st.spinner("Fetching race results..."):
                results = scrape_itra_results(url)
                
                if results:
                    # Convert results to DataFrame
                    df = pd.DataFrame(results)
                    
                    # Reorder columns
                    columns = ['position', 'name', 'time', 'performance_index', 'age', 'gender', 'nationality', 'profile_link']
                    df = df[columns]
                    
                    # Display results table
                    st.subheader("Top 3 Runners")
                    st.dataframe(
                        df,
                        column_config={
                            "profile_link": st.column_config.LinkColumn("Profile"),
                            "performance_index": st.column_config.Column("ITRA Index", help="Runner's ITRA Performance Index"),
                        },
                        hide_index=True,
                    )

                    if not df.empty:
                        # Create normalized time column
                        df['normalized_time'] = df['time'].apply(normalize_time)
                        
                        # Create age buckets
                        df['age_group'] = df['age'].apply(get_age_bucket)
                        
                        # Add filters
                        st.subheader("Interactive Analysis")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            selected_genders = st.multiselect('Gender', df['gender'].unique())
                        with col2:
                            selected_nations = st.multiselect('Nationality', df['nationality'].unique())
                        with col3:
                            selected_age_groups = st.multiselect('Age Group', sorted(df['age_group'].unique()))
                        
                        # Filter data based on selections
                        filtered_df = df.copy()
                        if selected_genders:
                            filtered_df = filtered_df[filtered_df['gender'].isin(selected_genders)]
                        if selected_nations:
                            filtered_df = filtered_df[filtered_df['nationality'].isin(selected_nations)]
                        if selected_age_groups:
                            filtered_df = filtered_df[filtered_df['age_group'].isin(selected_age_groups)]
                        
                        # Create scatterplot only if we have valid performance indices
                        valid_performance = filtered_df['performance_index'] != 'N/A'
                        valid_time = filtered_df['normalized_time'] != 'N/A'
                        plot_df = filtered_df[valid_performance & valid_time].copy()
                        
                        if not plot_df.empty:
                            fig = px.scatter(plot_df,
                                x='normalized_time',
                                y='performance_index',
                                color='gender',
                                hover_data=['name', 'age', 'nationality'],
                                title='Runner Performance vs Time'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning("No valid data available for visualization after filtering.")
                else:
                    st.warning("No results found. Please check the URL and try again.")
                    
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.error("Please enter a valid URL")
