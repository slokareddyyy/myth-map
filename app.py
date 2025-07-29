import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from PIL import Image
import os

# Setup
st.set_page_config(page_title="Myth Map", layout="centered")
st.title("🗺️ Myth Map: Document Your Local Legends")

# Ensure image directory exists
if not os.path.exists("images"):
    os.makedirs("images")

# Load or create dataset
DATA_FILE = "data.csv"
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["name", "description", "language", "latitude", "longitude", "image_path"]).to_csv(DATA_FILE, index=False)

# User form
with st.form("myth_form"):
    name = st.text_input("Your Name (Optional)")
    description = st.text_area("Describe a local myth, festival, or deity in your language")
    language = st.text_input("Language Used")
    latitude = st.number_input("Latitude", format="%.6f")
    longitude = st.number_input("Longitude", format="%.6f")
    image = st.file_uploader("Optional Image (e.g., temple, artwork)", type=["jpg", "jpeg", "png"])
    submit = st.form_submit_button("Submit")

    if submit and description and language:
        img_path = ""
        if image:
            img_path = f"images/{name or 'anon'}_{image.name}"
            with open(img_path, "wb") as f:
                f.write(image.getbuffer())

        new_row = pd.DataFrame([{
            "name": name,
            "description": description,
            "language": language,
            "latitude": latitude,
            "longitude": longitude,
            "image_path": img_path
        }])

        new_row.to_csv(DATA_FILE, mode='a', header=False, index=False)
        st.success("✨ Your entry has been added!")

# Display data on map
df = pd.read_csv(DATA_FILE)
st.header("🧭 Myth Map Viewer")

m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)  # Default: India center

for _, row in df.iterrows():
    popup_text = f"<b>Language:</b> {row['language']}<br><b>Description:</b> {row['description']}"
    if row['image_path'] and os.path.exists(row['image_path']):
        popup_text += f"<br><img src='{row['image_path']}' width='100'>"
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=folium.Popup(popup_text, max_width=250),
        tooltip=row['language']
    ).add_to(m)

st_data = st_folium(m, width=700, height=500)
