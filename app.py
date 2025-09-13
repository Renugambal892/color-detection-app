import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

# Load colors from CSV
@st.cache_data
def load_colors():
    return pd.read_csv('colors.csv', names=["color", "color_name", "hex", "R", "G", "B"], header=0)

# Find the closest color name from RGB
def get_closest_color(R, G, B, df):
    minimum = float('inf')
    cname = ""
    for i in range(len(df)):
        d = abs(R - int(df.loc[i,"R"])) + abs(G - int(df.loc[i,"G"])) + abs(B - int(df.loc[i,"B"]))
        if d <= minimum:
            minimum = d
            cname = df.loc[i,"color_name"]
    return cname

# Load the colors dataset
colors_df = load_colors()

st.title("🎨 Color Detection App")

# Upload an image
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.write("Click on the image to pick a color")

    # Create a canvas to allow clicking
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=3,
        stroke_color="#000000",
        background_image=image,
        update_streamlit=True,
        height=image.size[1],
        width=image.size[0],
        drawing_mode="point",
        point_display_radius=5,
        key="canvas"
    )

    # Check if user clicked on the image
    if canvas_result.json_data is not None and canvas_result.json_data["objects"]:
        obj = canvas_result.json_data["objects"][0]
        x = int(obj["left"])
        y = int(obj["top"])

        # Get RGB from the image at the clicked point
        R, G, B = image.getpixel((x, y))
        color_name = get_closest_color(R, G, B, colors_df)

        # Display results
        st.markdown(f"**Clicked Coordinates:** ({x}, {y})")
        st.markdown(f"**Color Name:** {color_name}")
        st.markdown(f"**RGB Values:** ({R}, {G}, {B})")
        st.markdown(
            f"<div style='background-color: rgb({R},{G},{B}); width: 150px; height: 50px;'></div>",
            unsafe_allow_html=True
        )
