import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

# ----------------------
# Load color dataset
# ----------------------
@st.cache_data
def load_colors():
    """
    Load colors.csv which contains columns: color_name, hex, R, G, B
    """
    df = pd.read_csv("colors.csv")
    return df

colors_df = load_colors()

# ----------------------
# Function to find closest color
# ----------------------
def get_closest_color(R, G, B):
    """
    Find the closest color from dataset using Manhattan distance.
    """
    min_distance = float('inf')
    closest_color = ""
    for i in range(len(colors_df)):
        d = abs(R - int(colors_df.loc[i, "R"])) + \
            abs(G - int(colors_df.loc[i, "G"])) + \
            abs(B - int(colors_df.loc[i, "B"]))
        if d < min_distance:
            min_distance = d
            closest_color = colors_df.loc[i, "color_name"]
    return clos
