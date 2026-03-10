import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime, time

# ==========================================
# CONFIGURATION (Robust for future changes)
# ==========================================
# Default to Northwest Vietnam (approx. Dien Bien / Son La area)
DEFAULT_MAP_CENTER = [21.5, 103.5]
DEFAULT_ZOOM = 8

# Set page layout to wide for a better map viewing experience
st.set_page_config(layout="wide", page_title="Vietnam Forest Fire Warning")

# ==========================================
# MOCK INFERENCE FUNCTION
# ==========================================
def predict_fires(target_date, target_time):
    """
    Replace this with your actual model inference.
    It accepts a date and time, and should return a list of dictionaries 
    containing the latitude and longitude of predicted fires.
    """
    # Mocking some data: If the user picks a time after 12:00 PM, show fires.
    if target_time >= time(12, 0):
        return [
            {"lat": 21.3, "lon": 103.2, "confidence": "High"},
            {"lat": 21.8, "lon": 103.8, "confidence": "Nominal"},
            {"lat": 22.1, "lon": 104.1, "confidence": "High"}
        ]
    return [] # No fires predicted

# ==========================================
# UI LAYOUT
# ==========================================
st.title("🔥 Vietnam Forest Fire Early Warning System")
st.markdown("Select a date and time to run the prediction model for the Northwest region.")

# Inputs: Placed in columns for a cleaner UI
col1, col2 = st.columns(2)
with col1:
    # Allows past, present, or future dates
    selected_date = st.date_input("Target Date", datetime.today())
with col2:
    selected_time = st.time_input("Target Time", datetime.now().time())

# Button to trigger the model (prevents the app from constantly rerunning on every input change)
if st.button("Run Prediction", type="primary"):
    
    with st.spinner("Running model inference..."):
        # Fetch predictions
        fire_points = predict_fires(selected_date, selected_time)
        
        # ==========================================
        # MAP RENDERING
        # ==========================================
        # Initialize the map
        m = folium.Map(location=DEFAULT_MAP_CENTER, zoom_start=DEFAULT_ZOOM, tiles="CartoDB positron")
        
        # Add a bounding box or marker to show the exact query location (Optional)
        # folium.Marker(DEFAULT_MAP_CENTER, popup="Northwest Focus Area").add_to(m)

        # Plot the predicted fires
        if fire_points:
            st.warning(f"⚠️ Warning: {len(fire_points)} fire hotspots predicted for this timeframe.")
            for point in fire_points:
                # Using a custom HTML DivIcon to display the fire emoji flawlessly
                folium.Marker(
                    location=[point["lat"], point["lon"]],
                    popup=f"Confidence: {point['confidence']}",
                    icon=folium.DivIcon(html="<div style='font-size: 24px; line-height: 24px;'>🔥</div>")
                ).add_to(m)
        else:
            st.success("✅ No forest fires predicted for this timeframe.")

        # Display the map in Streamlit
        # Using returned_objects=[] prevents Streamlit from rerunning when you click the map
        st_folium(m, width="100%", height=600, returned_objects=[])