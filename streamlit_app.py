import streamlit as st
from scraper import scrape_itra_results
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Trail Race Results",
    page_icon="🏃",
    layout="wide"
)

# Custom CSS with earth tones theme
st.markdown('''
<style>
    /* Earth tones variables */
    :root {
        --color-earth: #8B4513;
        --color-forest: #2F4F4F;
        --color-stone: #696969;
        --color-moss: #556B2F;
        --color-sand: #DEB887;
    }

    /* Main container styling */
    .stApp {
        background-color: var(--color-sand);
    }

    /* Headers styling */
    h1 {
        color: var(--color-earth) !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        text-align: center;
        padding: 1rem 0;
    }

    /* Topographic background pattern */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0.1;
        z-index: -1;
        background-image: repeating-linear-gradient(
            45deg,
            transparent,
            transparent 20px,
            var(--color-forest) 20px,
            var(--color-forest) 21px
        );
    }

    /* Custom styling for Streamlit elements */
    .stButton > button {
        background-color: var(--color-moss) !important;
        color: white !important;
        border: none !important;
        width: 100%;
    }

    .stButton > button:hover {
        background-color: var(--color-forest) !important;
    }
</style>
''', unsafe_allow_html=True)

# Title
st.title("Trail Race Results")

# URL input
url = st.text_input("Enter ITRA race results URL", placeholder="https://itra.run/Races/RaceResults/...")

# Submit button
if st.button("Get Results"):
    if url:
        try:
            with st.spinner("Fetching race results..."):
                results = scrape_itra_results(url)
                
                # Convert results to DataFrame for better display
                df = pd.DataFrame(results)
                
                # Reorder columns for better presentation
                columns = ['position', 'name', 'time', 'age', 'gender', 'nationality', 'profile_link']
                df = df[columns]
                
                # Display results
                st.subheader("Top 3 Runners")
                st.dataframe(
                    df,
                    column_config={
                        "profile_link": st.column_config.LinkColumn("Profile"),
                    },
                    hide_index=True,
                )
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.error("Please enter a valid URL")
