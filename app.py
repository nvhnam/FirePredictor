import os
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import requests
import pytz
from datetime import datetime, date

# Constants
DEFAULT_MAP_CENTER = [21.5, 103.5]
DEFAULT_ZOOM = 7
API_URL = os.getenv("API_URL", "http://144.91.85.194:3000/api/fires")
START_DATE = date(2026, 3, 25)

# Get current date in Vietnam Timezone (GMT+7)
VN_TZ = pytz.timezone('Asia/Ho_Chi_Minh')
vn_today = datetime.now(VN_TZ).date()

# Approximate coordinates for Northwest Vietnam highlight (Tây Bắc)
NORTHWEST_POLYGON = [
    [22.85, 102.17], [22.85, 104.63], [22.20, 105.05], [21.13, 105.80], 
    [20.20, 106.00], [20.45, 104.80], [20.90, 102.17], [22.85, 102.17]
]

st.set_page_config(layout="wide", page_title="Vietnam Wildfire Warning", page_icon="🔥")

# Initialize session state for persistent results
if 'fire_data' not in st.session_state:
    st.session_state.fire_data = None
if 'last_date' not in st.session_state:
    st.session_state.last_date = None

@st.cache_data(ttl=3600)
def predict_fires(target_date):
    """Fetches fire prediction data from the API for a specific date."""
    formatted_date = target_date.strftime("%Y-%m-%d")
    try:
        response = requests.get(f"{API_URL}/{formatted_date}", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from API: {e}")
        return []

# --- Sidebar ---
with st.sidebar:
    st.title("🔥 Configuration")
    st.markdown("Select a date to run the prediction model for the Northwest region.")
    
    selected_date = st.date_input(
        "Target Date", 
        value=vn_today if vn_today >= START_DATE else START_DATE,
        min_value=START_DATE,
        max_value=vn_today if vn_today >= START_DATE else START_DATE
    ) 
    
    if st.button("Run Prediction", type="primary", use_container_width=True):
        with st.spinner("Fetching data..."):
            st.session_state.fire_data = predict_fires(selected_date)
            st.session_state.last_date = selected_date
    
    st.divider()
    st.markdown("""
    ### About
    This system provides early warning for wildfire in the **Northwest region of Vietnam**.
    
    **Blue Border:** Prediction Area
    """)

# --- Main Content ---
st.title("🔥 Vietnam Wildfire Early Warning System")

def create_map(fire_points=None):
    m = folium.Map(
        location=DEFAULT_MAP_CENTER, 
        zoom_start=DEFAULT_ZOOM,
        tiles=None,
        prefer_canvas=True 
    )
    
    # Base Layers
    folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        attr="Google Hybrid",
        name="Google Satellite (Names)",
        overlay=False,
        control=True
    ).add_to(m)
    
    folium.TileLayer(
        tiles="openstreetmap",
        name="OpenStreetMap",
        overlay=False,
        control=True
    ).add_to(m)

    # Northwest Highlight
    folium.PolyLine(
        NORTHWEST_POLYGON,
        color="#3388ff",
        weight=3,
        opacity=0.8,
        tooltip="Northwest Region Area"
    ).add_to(m)
    
    folium.Polygon(
        NORTHWEST_POLYGON,
        color="#3388ff",
        weight=0,
        fill=True,
        fill_color="#3388ff",
        fill_opacity=0.05
    ).add_to(m)

    # Fire Markers
    if fire_points:
        for point in fire_points:
            lat, lon = point["latitude"], point["longitude"]
            conf = point.get("confidence_score", 0)
            grid_id = point.get("grid_id", "N/A")
            
            icon_html = '<div style="font-size: 24px;">🔥</div>'
            popup_text = f"Grid: {grid_id}<br>Confidence: {conf:.1%}"
            
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_text, max_width=200),
                icon=folium.DivIcon(html=icon_html)
            ).add_to(m)
    
    folium.LayerControl().add_to(m)
    return m

# Render Dashboard
if st.session_state.fire_data is not None:
    data = st.session_state.fire_data
    
    col1, col2= st.columns(2)
    with col1:
        st.metric("Total Hotspots", len(data))
    with col2:
        st.metric("Date", st.session_state.last_date.strftime("%Y-%m-%d"))
        # avg_conf = sum(f['confidence_score'] for f in data) / len(data) if data else 0
        # st.metric("Average Confidence", f"{avg_conf:.1%}")
    # with col3:

    m = create_map(data)
    # Use returned_objects=[] to prevent lagging during pan/zoom
    st_folium(m, width="100%", height=600, key="fire_map", returned_objects=[])
else:
    # Initial View
    m = create_map()
    st_folium(m, width="100%", height=600, key="initial_map", returned_objects=[])
