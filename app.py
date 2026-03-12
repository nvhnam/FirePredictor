import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime, time

DEFAULT_MAP_CENTER = [21.5, 103.5]
DEFAULT_ZOOM = 8

st.set_page_config(layout="wide", page_title="Vietnam Forest Fire Warning")

def predict_fires(target_date, target_time):
    if target_time >= time(12, 0):
        return [
            {"lat": 21.3, "lon": 103.2, "confidence": "High"},
            {"lat": 21.8, "lon": 103.8, "confidence": "Nominal"},
            {"lat": 22.1, "lon": 104.1, "confidence": "High"}
        ]
    return [] 

st.title("🔥 Vietnam Forest Fire Early Warning System")
st.markdown("Select a date and time to run the prediction model for the Northwest region.")

col1, col2 = st.columns(2)
with col1:
    selected_date = st.date_input("Target Date", datetime.today())
with col2:
    selected_time = st.time_input("Target Time", datetime.now().time())

if st.button("Run Prediction", type="primary"):    
    with st.spinner("Running model inference..."):
        fire_points = predict_fires(selected_date, selected_time)
        m = folium.Map(location=DEFAULT_MAP_CENTER, zoom_start=DEFAULT_ZOOM, tiles="CartoDB positron")
        if fire_points:
            st.warning(f"⚠️ Warning: {len(fire_points)} fire hotspots predicted for this timeframe.")
            for point in fire_points:
                folium.Marker(
                    location=[point["lat"], point["lon"]],
                    popup=f"Confidence: {point['confidence']}",
                    icon=folium.DivIcon(html="<div style='font-size: 24px; line-height: 24px;'>🔥</div>")
                ).add_to(m)
        else:
            st.success("✅ No forest fires predicted for this timeframe.")

        st_folium(m, width="100%", height=600, returned_objects=[])