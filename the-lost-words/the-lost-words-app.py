import streamlit as st
import pandas as pd
import altair as alt

df = pd.read_csv("the-lost-words/books.csv")


# url = 'https://raw.githubusercontent.com/lotus-pad/the-lost-words-codes/books.csv'
# df = pd.read_csv(url)



df.columns = [col.strip().title().replace(" ", "_").replace("-", "_") for col in df.columns]

# Sidebar filters
st.sidebar.header("filter books")
selected_author = st.sidebar.selectbox("choose an author", options=["All"] + list(df["Author"].dropna().unique()))
selected_categories = st.sidebar.multiselect("choose categories", options=df["Categories"].dropna().unique())

# Filtered data
filtered_df = df.copy()
if selected_author != "All":
    filtered_df = filtered_df[filtered_df["Author"] == selected_author]
if selected_categories:
    filtered_df = filtered_df[filtered_df["Categories"].isin(selected_categories)]

# Tabs
tab1, tab2 = st.tabs(["explore books", "summary stats"])

with tab1:
    st.header("filtered books")
    st.dataframe(filtered_df)

    with st.expander("view raw data"):
        st.dataframe(df)

with tab2:
    st.header("category breakdown")
    cat_counts = df["Categories"].value_counts().reset_index()
    cat_counts.columns = ["category", "count"]
    chart = alt.Chart(cat_counts.head(10)).mark_bar().encode(
        x="count:Q", y=alt.Y("category:N", sort='-x'), tooltip=["category", "count"]
    ).properties(width=600)
    st.altair_chart(chart)

# Search
search_term = st.text_input("search title or description")
if search_term:
    results = df[df.apply(lambda row: search_term.lower() in str(row["Title"]).lower() or search_term.lower() in str(row["Description"]).lower(), axis=1)]
    st.subheader(f"search results for '{search_term}'")
    st.dataframe(results)

# Documentation
with st.popover("ℹ️ how to use this app"):
    st.markdown("""
    - use the sidebar to filter by author or category  
    - explore filtered data under 'explore books' tab  
    - view overall category stats in 'summary stats'  
    - search for keywords in titles or descriptions  
    - click 'view raw data' to see everything  
    """)
