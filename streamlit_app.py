import streamlit as st
import pandas as pd
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
                    
                    # Display results
                    st.subheader("Top 3 Runners")
                    st.dataframe(
                        df,
                        column_config={
                            "profile_link": st.column_config.LinkColumn("Profile"),
                            "performance_index": st.column_config.Column("ITRA Index", help="Runner's ITRA Performance Index"),
                        },
                        hide_index=True,
                    )
                else:
                    st.warning("No results found. Please check the URL and try again.")
                    
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.error("Please enter a valid URL")