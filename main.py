import streamlit as st
from scraper import ItraScraper

def main():
    # Page configuration
    st.set_page_config(
        page_title="ITRA Performance Index Scraper",
        page_icon="🏃",
        layout="centered"
    )

    # Header
    st.title("🏃 ITRA Performance Index Scraper")
    st.markdown("""
    This tool extracts the ITRA (International Trail Running Association) performance index 
    from runner profiles. Enter a valid ITRA profile URL below.
    
    Example URL formats:
    - `https://itra.run/RunnerSpace/Hoover.Beau/5249134`
    - `https://itra.run/api/RunnerSpace/GetRunnerSpace?memberString=p3z7u3wRI8fpW0uxAv2OTA%3D%3D`
    """)

    # URL input
    url = st.text_input("Enter ITRA Profile URL", "")

    if st.button("Get Performance Index"):
        if url:
            with st.spinner("Fetching data..."):
                # Create scraper instance
                scraper = ItraScraper()
                
                # Get the performance index
                result = scraper.extract_performance_index(url)

                # Display results
                if result['success']:
                    st.success("Data retrieved successfully!")
                    
                    # Create two columns for organized display
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric(
                            label="Runner Name",
                            value=result['runner_name']
                        )
                    
                    with col2:
                        st.metric(
                            label="Performance Index",
                            value=result['performance_index']
                        )
                else:
                    st.error(f"Error: {result['error']}")
        else:
            st.warning("Please enter a URL")

    # Footer with information
    st.markdown("---")
    st.markdown("""
    ### About
    - This tool scrapes ITRA performance index data from runner profiles
    - Supports both direct profile URLs and API endpoints
    - Data is fetched in real-time
    
    ### Tips
    - Make sure to use the correct URL format
    - The profile must be public
    - Performance index might not be available for all runners
    """)

if __name__ == "__main__":
    main()
