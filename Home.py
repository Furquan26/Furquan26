# Home.py
import streamlit as st
import requests
import xmltodict
from auth import show_auth_page

# Check authentication
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    show_auth_page()
    st.stop()

# Rest of your existing Home.py code follows here...
st.set_page_config(page_title="📰 Personalized News", layout="wide")
st.title(f"📰 Personalized News Aggregator - Welcome {st.session_state.user_name}!")
st.markdown("Select your preferred **sources**, choose a **category**, or chat with the assistant below!")

# ... rest of your existing Home.py code ...

# Source and category mappings
sources = {
    "Times of India": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
    "Dainik Bhaskar": "https://www.bhaskar.com/rss-v1--category-1061.xml",
    "ABP Majha": "https://marathi.abplive.com/rss/featured-articles.xml",
    "Dainik Jagran": "https://www.jagran.com/rss/news/national.xml",
    "Aaj Tak": "https://www.aajtak.in/rssfeed/ns"
}

categories = {
    "General": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "Sports": "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms",
    "Politics": "https://www.thehindu.com/news/national/feeder/default.rss",
    "Technology": "https://www.indiatoday.in/technology/rss",
    "Market": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms"
}

# Sidebar selection
with st.sidebar:
    st.header("Choose your news preferences")
    selected_sources = st.multiselect("Select News Sources", list(sources.keys()))
    selected_category = st.selectbox("Select News Category", list(categories.keys()))

# Fetch news function
def fetch_rss(url):
    try:
        response = requests.get(url)
        data = xmltodict.parse(response.content)
        return data["rss"]["channel"]["item"]
    except:
        return []

# Get News button
if st.button("Get News"):
    news_items = []

    # From selected sources
    for src in selected_sources:
        items = fetch_rss(sources[src])
        for item in items:
            news_items.append({"title": item["title"], "link": item["link"], "source": src})

    # From category
    items = fetch_rss(categories[selected_category])
    for item in items:
        news_items.append({"title": item["title"], "link": item["link"], "source": selected_category})

    if news_items:
        st.subheader("🗞️ News Results")
        for news in news_items:
            st.markdown(f"🔗 [{news['title']}]({news['link']})  — *{news['source']}*")
    else:
        st.warning("No news items found.")

# --- Chatbot Section ---
st.divider()
st.subheader("🤖 Chat with NewsBot")

# Save conversation
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.chat_input("Ask me something like 'Show sports news' or 'What’s new in technology'?")

# Bot response logic
def handle_bot_query(query):
    query = query.lower()
    matched_category = None
    for cat in categories:
        if cat.lower() in query:
            matched_category = cat
            break
    if matched_category:
        items = fetch_rss(categories[matched_category])
        if items:
            response = f"Here are the latest {matched_category} news articles:\n\n"
            for item in items[:5]:
                response += f"🔗 [{item['title']}]({item['link']})\n\n"
            return response
        else:
            return "Sorry, couldn't find anything right now."
    return "Try asking about a news category like sports, politics, or technology."

# Display chat history
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# Handle input
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    reply = handle_bot_query(user_input)
    st.session_state.chat_history.append(("assistant", reply))
    with st.chat_message("assistant"):
        st.markdown(reply)
