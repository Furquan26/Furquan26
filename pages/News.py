import streamlit as st
import requests
import xmltodict

# # 🔐 Restrict access to logged-in users only
# if "authenticated" not in st.session_state or not st.session_state.authenticated:
#     st.error("🔒 Please login to access this page.")
#     st.stop()

st.set_page_config(page_title="🗞️ News Results")

st.title("🗞️ News Results")

# RSS feed mappings
sources = {
    "Times of India": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
    "Dainik Bhaskar": "https://www.bhaskar.com/rss-v1--category-1061.xml",
    "ABP Majha": "https://marathi.abplive.com/rss/featured-articles.xml",
    "Dainik Jagran": "https://www.jagran.com/rss/news/national.xml",
    "Aaj Tak": "https://www.aajtak.in/rss",
    "India Today": "https://www.indiatoday.in/rss/home"
}

categories = {
    "General": [{"name": "Times of India", "url": sources["Times of India"]}],
    "Sports": [{"name": "TOI Sports", "url": "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms"}],
    "Politics": [{"name": "The Hindu Politics", "url": sources["The Hindu"]}],
    "Technology": [{"name": "India Today Tech", "url": "https://www.indiatoday.in/technology/rss"}],
    "Market": [{"name": "Economic Times Market", "url": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms"}]
}

def fetch_news(feed_list):
    news_items = []
    for feed in feed_list:
        try:
            resp = requests.get(feed["url"])
            data = xmltodict.parse(resp.content)
            items = data["rss"]["channel"]["item"]
            for i in items[:10]:
                news_items.append({
                    "title": i.get("title", "No Title"),
                    "link": i.get("link", "#"),
                    "source": feed["name"]
                })
        except Exception as e:
            st.warning(f"Failed to load from {feed['name']}: {e}")
    return news_items

# Fetch from session
if "selected_sources" not in st.session_state:
    st.error("Please go to the Home page and select sources.")
    st.stop()

selected_sources = st.session_state.selected_sources
selected_category = st.session_state.selected_category

# Create list of feeds
feeds_to_fetch = []
for src in selected_sources:
    feeds_to_fetch.append({"name": src, "url": sources[src]})

if selected_category != "-- None --":
    feeds_to_fetch.extend(categories[selected_category])

news = fetch_news(feeds_to_fetch)

# Show results
if news:
    for item in news:
        st.markdown(f"- [{item['title']}]({item['link']}) _(Source: {item['source']})_")
else:
    st.info("No news found.")
