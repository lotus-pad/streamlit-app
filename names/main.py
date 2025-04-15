import pandas as pd
import zipfile
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import BytesIO
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# from my_plots import *
import streamlit as st

## LOAD DATA DIRECTLY FROM SS WEBSITE
@st.cache_data
def load_name_data():
    names_file = 'https://www.ssa.gov/oact/babynames/names.zip'
    response = requests.get(names_file)
    with zipfile.ZipFile(BytesIO(response.content)) as z:
        dfs = []
        files = [file for file in z.namelist() if file.endswith('.txt')]
        for file in files:
            with z.open(file) as f:
                df = pd.read_csv(f, header=None)
                df.columns = ['name','sex','count']
                df['year'] = int(file[3:7])
                dfs.append(df)
        data = pd.concat(dfs, ignore_index=True)
    data['pct'] = data['count'] / data.groupby(['year', 'sex'])['count'].transform('sum')
    return data
df = load_name_data()
df['total_births'] = df.groupby(['year', 'sex'])['count'].transform('sum')
df['prop'] = df['count'] / df['total_births']
df['rank'] = df.groupby(['year', 'sex'])['count'].rank(method='first', ascending=False)


## LOAD DATA FROM A SAVED FILE
# df = pd.read_csv('/Users/rental/Desktop/winter2025/stat386/class-practice/all-names.csv')
# df['total_births'] = df.groupby(['year', 'sex'])['count'].transform('sum')
# df['prop'] = df['count'] / df['total_births']

## LOAD DATA FROM A SMALLER NAME DATASET ON GITHUB
# url = 'https://raw.githubusercontent.com/esnt/Data/refs/heads/main/Names/popular_names.csv'
# df = pd.read_csv(url)

st.title('My Name App')

####04/03 talking about containers
tab1, tab2, tab3 = st.tabs(['overall', 'by name', 'by year'])
with tab1:
    st.write('here is stuff about all the data')

with tab2:
    st.write('name')
    # pick a name
    noi = st.text_input('enter a name')
    plot_female = st.checkbox('plot female line')
    plot_male = st.checkbox('plot male line')
    name_df = df[df['name']==noi]

    fig1 = plt.figure(figsize=(15, 8))

    if plot_female:
        sns.lineplot(data=name_df[name_df['sex'] == 'F'], x='year', y='prop', label='Female')

    if plot_male:
        sns.lineplot(data=name_df[name_df['sex'] == 'M'], x='year', y='prop', label='Male')

    plt.title(f'popularity of {noi} over time')
    plt.xlim(1880, 2025)
    plt.xlabel('year')
    plt.ylabel('proportion')
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()

    st.pyplot(fig1)

with tab3:
    st.write('year')
    # pick a year
    yoi = st.text_input('enter a year')
    top_names = df[df['year'] == yoi]
    top_female = top_names[top_names['sex'] == 'F'].nlargest(10, 'count')

    fig2 = plt.figure(figsize=(10, 5))

    sns.barplot(data=top_female, x='count', y='name')
    plt.title(f"top 10 female names in {yoi}")
    plt.xlabel('count')
    plt.ylabel('name')
    plt.tight_layout()

    st.pyplot(fig2)