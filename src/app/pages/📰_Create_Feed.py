import pandas as pd
import streamlit as st
from src.db.connection import write_feed, get_connection

st.title("Create a news feed...")

row1 = st.columns(1)
row2 = st.columns(3)
row3 = st.columns(1)

feed_name = row1[0].text_input(
    "Feed Name", placeholder="Enter a name for this feed."
)
competitor_name = row2[0].text_input(
    "Competitor Name", placeholder="Enter a competitor name."
)
category = row2[1].text_input("Category", placeholder="Enter a category.")
custom_query = row2[2].text_input(
    "Custom Query", placeholder="Enter a custom query. [Optional]"
)

# Base DataFrame with initial default parameters
params_table = pd.DataFrame(
    columns=["Parameter", "Value"],
    data=[
        ["search_depth", "advanced"],
        ["time_range", "y"],
        ["max_results", "10"],
        ["include_images", "True"],
        ["include_answer", "True"],
        ["include_raw_content", "True"],
        ["include_domains", ""],
        ["exclude_domains", ""],
        ["exact_match", "True"],
    ],
)

# Drop-down expander area with editable table
with row3[0].expander("Extra Parameters", expanded=False):
    st.caption("Double-click any value in the table to modify its setting:")

    edited_params_df = st.data_editor(
        params_table,
        use_container_width=True,
        hide_index=True,
        disabled=["Parameter"], 
        num_rows="fixed",  
        key="params_editor",
    )

extra_kwargs = dict(
    zip(edited_params_df["Parameter"], edited_params_df["Value"])
)

if st.button("Create Feed", type="primary"):
    payload = {
        "feed_name": feed_name,
        "competitor": competitor_name,
        "category": category,
        "custom_query": custom_query or None,
        "query": custom_query or f'"{competitor_name}" new power tool accessories',
        "extra_params": {k: v for k, v in extra_kwargs.items() if v != ""},
    }
    with get_connection() as conn:
        write_feed(conn, feed_name, [payload])
    st.success("Feed configuration ready!")
    st.json(payload)
