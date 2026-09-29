# shared.py
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# -------------------------
# Colors & Styling
# -------------------------
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#ff7f0e"

def set_page_style():
    st.markdown(
        """
        <style>
        .css-1d391kg {background-color: #f5f5f5;}
        .stButton>button {background-color: #1f77b4; color: white;}
        </style>
        """, unsafe_allow_html=True
    )

# -------------------------
# Characters
# -------------------------
CHARACTERS = [
    {
        "name": "Marcus",
        "description": "Black first-time homebuyer, hit hard by the crash",
        "loan_type": "Conventional",
        "story_color": "#d62728"
    },
    {
        "name": "David",
        "description": "High-income White buyer, actually benefited post-crash",
        "loan_type": "Conventional",
        "story_color": "#2ca02c"
    },
    {
        "name": "Maria",
        "description": "Single mother, FHA loan, struggled post-crash",
        "loan_type": "FHA",
        "story_color": "#9467bd"
    },
    {
        "name": "James",
        "description": "Veteran, VA loan, weathered the crash better",
        "loan_type": "VA",
        "story_color": "#8c564b"
    },
    {
        "name": "Sandra",
        "description": "Middle-class, refinanced to survive",
        "loan_type": "Conventional",
        "story_color": "#e377c2"
    }
]

# -------------------------
# Chart Helpers
# -------------------------
def plot_bar(df, x, y, color=None, title=None):
    fig = px.bar(df, x=x, y=y, color=color)
    if title:
        fig.update_layout(title=title)
    return fig

def plot_line(df, x, y, color=None, title=None):
    fig = px.line(df, x=x, y=y, color=color)
    if title:
        fig.update_layout(title=title)
    return fig

# -------------------------
# Load Data Helper
# -------------------------
DATA_PATH = Path(__file__).parent / 'hmda_master.parquet'

@st.cache_data
def load_data(path=DATA_PATH):
    return pd.read_parquet(path)