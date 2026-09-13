import json
import os
import streamlit as st

st.set_page_config(page_title="Competitor News Tracker", layout="wide")
st.title("Competitor News Tracker")

DATA_LOCATION = "data/run_results/makita_accessories.json"

# TODO: Have it parse the entire data directory and return the results in the pandas df
@st.cache_data
def load_feed():
    if not os.path.exists(DATA_LOCATION):
        st.error(f"Data file not found at: `{DATA_LOCATION}`")
        return []

    with open(DATA_LOCATION, "r", encoding="utf-8") as file:
        feed = json.load(file)

    return feed.get("results", [])


@st.dialog("Article Details", width="large")
def show_article_modal(item: dict):
    st.subheader(item.get("title", "No Title"))

    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"**Score / Relevance:** {item.get('score', 'N/A')}")
    with col2:
        published_date = item.get("published_date")
        if published_date:
            st.caption(f"**Published:** {published_date}")

    st.divider()

    full_text = item.get("raw_content") or item.get("content", "No content.")
    st.markdown(full_text)

    url = item.get("url")
    if url:
        st.link_button("Open Original Source ↗", url)


with st.spinner("Loading competitor intelligence feed..."):
    articles = load_feed()

if not articles:
    st.info("No competitor news available in this feed.")
    st.stop()

st.caption(f"Showing {len(articles)} tracked developments:")

NUM_COLS = 2
columns = st.columns(NUM_COLS)

for idx, item in enumerate(articles):
    target_col = columns[idx % NUM_COLS]

    with target_col:
        with st.container(border=True):
            title = item.get("title", "Untitled Development")
            snippet = item.get("content", "")

            st.markdown(f"#### {title}")
            preview = (
                (snippet[:160] + "...") if len(snippet) > 160 else snippet
            )
            st.write(preview)

            if st.button("Read Full Story", key=f"btn_{idx}"):
                show_article_modal(item)
