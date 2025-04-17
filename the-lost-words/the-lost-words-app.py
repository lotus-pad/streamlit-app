# import pandas as pd
# import zipfile
# import plotly.express as px
# import matplotlib.pyplot as plt
# import seaborn as sns
# import requests
# from io import BytesIO
# import streamlit as st

# # LOAD DATA FROM A SAVED FILE
# df = pd.read_csv('/Users/rental/Desktop/winter2025/stat386/blog/blog-codes/the-lost-words-codes/books.csv')

# st.title('App for "the lost words"')

# #Input widgets, expanders, popovers, tabs, and sidebars

# tab1, tab2, tab3 = st.tabs(['book author', 'two', 'three'])
# #popover


# with tab1:
#     # first line
#     st.write('book')
#     #popover
#     with st.popover("Open popover"):
#         st.markdown("Hello World 👋")
#         name = st.text_input("What's your name?")

#     st.write("Your name:", name)
    
#     #rating
#     st.write("how much would you rate this app?")
#     sentiment_mapping = ["one", "two", "three", "four", "five"]
#     selected = st.feedback("stars")
#     if selected is not None:
#         st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")

import streamlit as st
import pandas as pd
import altair as alt
# from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('/Users/rental/Desktop/winter2025/stat386/blog/blog-codes/the-lost-words-codes/books.csv')

df.columns = [col.strip().title().replace(" ", "_").replace("-", "_") for col in df.columns]

# Sidebar filters
st.sidebar.header("Filter Books")
selected_authors = st.sidebar.multiselect("Select Author(s)", options=df["Author"].unique())
selected_categories = st.sidebar.multiselect("Categories", options=df["Categories"].dropna().unique())

# Filter data based on sidebar
filtered_df = df.copy()
if selected_authors:
    filtered_df = filtered_df[filtered_df["Author"].isin(selected_authors)]
if selected_categories:
    filtered_df = filtered_df[filtered_df["Categories"].isin(selected_categories)]

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["Book Explorer", "Author Profiles", "LGBTQ+ Focus", "Summary Stats"])

with tab1:
    st.header("Book Explorer")
    st.dataframe(filtered_df)
    with st.expander("View Raw Data"):
        st.dataframe(df)

with tab2:
    st.header("Author Profiles")
    top_authors = df["Author"].value_counts().head(10).reset_index()
    top_authors.columns = ["Author", "Count"]
    chart = alt.Chart(top_authors).mark_bar().encode(
        x=alt.X('Count:Q'),
        y=alt.Y('Author:N', sort='-x'),
        tooltip=['Author', 'Count']
    ).properties(width=600, height=400)
    st.altair_chart(chart)

with tab3:
    st.header("LGBTQ+ Focus")
    st.markdown("""
        We use keyword matching in descriptions and categories to flag potential LGBTQ+ related content.
    """)
    lgbt_keywords = ["lgbt", "gay", "lesbian", "queer", "trans", "nonbinary", "bisexual", "sapphic"]
    df["is_lgbtq"] = df.apply(
        lambda row: any(kw in str(row["Description"]).lower() for kw in lgbt_keywords) or
                    any(kw in str(row["Categories"]).lower() for kw in lgbt_keywords),
        axis=1
    )
    lgbtq_books = df[df["is_lgbtq"] == True]
    st.metric("LGBTQ+ Books in Dataset", len(lgbtq_books))
    st.dataframe(lgbtq_books)

with tab4:
    st.header("Summary Stats")
    st.subheader("Top Categories (Bar Chart)")
    category_counts = df["Categories"].value_counts().reset_index()
    category_counts.columns = ["Category", "Count"]
    bar_chart = alt.Chart(category_counts.head(15)).mark_bar().encode(
        x=alt.X("Count:Q"),
        y=alt.Y("Category:N", sort='-x'),
        tooltip=["Category", "Count"]
    ).properties(width=700, height=400)
    st.altair_chart(bar_chart)

    st.subheader("LGBTQ+ vs Non-LGBTQ+ Books")
    lgbt_counts = df["is_lgbtq"].value_counts().rename({True: "LGBTQ+", False: "Non-LGBTQ+"})
    st.bar_chart(lgbt_counts)

# Search bar
search_term = st.text_input("Search books by keyword (title/description)")
if search_term:
    search_results = df[df.apply(lambda row: search_term.lower() in str(row["Title"]).lower() or search_term.lower() in str(row["Description"]).lower(), axis=1)]
    st.subheader(f"Search Results for '{search_term}':")
    st.dataframe(search_results)

# Add tooltips/documentation
with st.popover("ℹ️ App Instructions"):
    st.markdown("""
    - Use the sidebar to filter by author or category.
    - Tabs let you explore the data from multiple perspectives.
    - The 'LGBTQ+ Focus' tab uses keyword matching to identify possibly LGBTQ+ books.
    - Use the search bar to look for specific terms in titles or descriptions.
    """)