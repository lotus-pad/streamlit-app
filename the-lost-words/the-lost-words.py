import pandas as pd
import zipfile
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import BytesIO
import streamlit as st

# LOAD DATA FROM A SAVED FILE
df = pd.read_csv('/Users/rental/Desktop/winter2025/stat386/blog/blog-codes/the-lost-words-codes/books.csv')

st.title('App for the lost words')
