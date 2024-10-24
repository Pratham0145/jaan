# First, install all required packages by running these commands in your terminal:
"""
pip install streamlit
pip install Pillow
pip install streamlit-lottie
pip install requests
"""

# Then use this complete code:

import streamlit as st
from PIL import Image
import os
import time
from streamlit_lottie import st_lottie
import json
import requests

# Set page configuration
st.set_page_config(layout="wide")

# Title of the app
st.title("Button-Triggered Local Image Display")

# Load Lottie animation file
def load_lottieurl(path: str):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading animation file: {path}")
        st.error(f"Error details: {str(e)}")
        return None

# Alternative method to load Lottie from URL if local files don't work
def load_lottie_from_url(url: str):
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        st.error(f"Error loading animation from URL: {url}")
        return None

# Try loading local files first, if they fail, use URLs as fallback
try:
    animations = {
        1: load_lottieurl("Animation - 1729771319722.json"),
        2: load_lottieurl("angry.json"),
        3: load_lottieurl("missyou.json")
    }
except:
    # Fallback to online Lottie files
    animations = {
        1: load_lottie_from_url("https://assets6.lottiefiles.com/packages/lf20_xvrofzfk.json"),  # Happy animation
        2: load_lottie_from_url("https://assets8.lottiefiles.com/packages/lf20_wj7f3ver.json"),  # Angry animation
        3: load_lottie_from_url("https://assets7.lottiefiles.com/packages/lf20_kj1t9wtw.json")   # Sad animation
    }

# Add custom CSS to style the buttons
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        height: 100px;
        font-size: 24px;
        margin: 10px 0;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.02);
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }

    .image-container {
        margin: 20px 0;
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# Dictionary of local image paths
image_paths = {
    1: r"devva-happy-idi-tane-nann-joteyavagu-nagata-iru-kane-maja.jpg",
    2: r"im-sorry-kane-for-everything-ning-bhal-sala-bejar-madyan.jpg",
    3: r"miss-en-madalla-ni-nang-gottu-but-nang-mari-beda-handi.jpg"
}

# Initialize session states
if 'current_image' not in st.session_state:
    st.session_state.current_image = None
if 'loading' not in st.session_state:
    st.session_state.loading = False
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = None

# Function to handle button clicks
def handle_button_click(button_number):
    if animations[button_number] is not None:
        st.session_state.loading = True
        st.session_state.button_clicked = button_number
        with loading_container:
            try:
                st_lottie(animations[button_number], height=200, key=f"loading_{button_number}")
                time.sleep(2)
            except Exception as e:
                st.error(f"Error displaying animation: {str(e)}")
        st.session_state.current_image = button_number
        st.session_state.loading = False
        st.experimental_rerun()

# Create a container for the loading animation
loading_container = st.empty()

# If there's a current image, display it
if st.session_state.current_image:
    st.markdown("<div class='image-container'>", unsafe_allow_html=True)
    try:
        # Open and display the local image
        image = Image.open(image_paths[st.session_state.current_image])
        st.image(image, caption=f"Image {st.session_state.current_image}", use_column_width=True)
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add a button to go back to the home page
    if st.button("Back to Home"):
        st.session_state.current_image = None
        st.session_state.loading = False
        st.experimental_rerun()
else:
    # Create three big buttons (one below another)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("HAPPY NA 😊😍 CLICK MADU"):
            handle_button_click(1)
    
    with col2:
        if st.button("KOPA NA 😡😤 ILLI CLICK MADU"):
            handle_button_click(2)
    
    with col3:
        if st.button("MISSING AA 🥹🥺 CLICK MADU"):
            handle_button_click(3)

# Show loading animation if in loading state
if st.session_state.loading and st.session_state.button_clicked:
    with loading_container:
        try:
            st_lottie(
                animations[st.session_state.button_clicked], 
                height=200, 
                key=f"loading_{st.session_state.button_clicked}"
            )
        except Exception as e:
            st.error(f"Error displaying loading animation: {str(e)}")
