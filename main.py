import streamlit as st
import json
from scraper import dynamic_scraper  # Import the scraper function

# Streamlit UI setup
st.title("Dynamic Web Scraper")
st.write("Enter the URL to scrape and an optional search term.")

# URL input
url = st.text_input("URL", "https://example.com/your_target_page")

# Search term input
search_term = st.text_input("Search Term (optional)", "")

# Button to trigger scraping
if st.button("Scrape"):
    if url:
        st.write("Scraping...")
        try:
            # Call the scraper function
            scraped_data = dynamic_scraper(url, search_term)

            # Convert the scraped data from JSON string to a Python object
            results = json.loads(scraped_data)

            # Display results
            if results:
                st.write("### Scraped Results:")
                for item in results:
                    st.write(f"**Title:** {item['title']}")
                    st.image(item['thumbnail'], width=200)
                    st.write(f"[Watch Video]({item['video_link']})")
            else:
                st.write("No results found.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid URL.")
