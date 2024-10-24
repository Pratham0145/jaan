import streamlit as st
from PIL import Image
import os
import time
from streamlit_lottie import st_lottie
import json

# Set page configuration
st.set_page_config(layout="wide")

# Title of the app
st.title("Button-Triggered Local Image Display")

# Load Lottie animation file
def load_lottieurl(path: str):
    with open(path, 'r') as f:
        return json.load(f)

# Load different animations for each button        
animations = {
    1: load_lottieurl("Animation - 1729771319722.json"),  # Happy/dance animation
    2: load_lottieurl("angry.json"),                      # Angry animation
    3: load_lottieurl("missyou.json")                     # Missing animation
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
    1: r"C:\Users\prathamesh.patil\Pictures\Screenshots\Screenshot 2024-08-09 160532.png",
    2: r"C:\Users\prathamesh.patil\Pictures\Screenshots\Screenshot 2024-08-19 112450.png",
    3: r"C:\Users\prathamesh.patil\Pictures\Screenshots\Screenshot 2024-08-28 162325.png"
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
    st.session_state.loading = True
    st.session_state.button_clicked = button_number
    with loading_container:
        st_lottie(animations[button_number], height=200, key=f"loading_{button_number}")
        time.sleep(2)
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
        st.error("Error loading image. Please check the image path or try again.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add a button to go back to the home page
    if st.button("Back to Home"):
        st.session_state.current_image = None
        st.session_state.loading = False
        # st.experimental_rerun()
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
        st_lottie(
            animations[st.session_state.button_clicked], 
            height=200, 
            key=f"loading_{st.session_state.button_clicked}"
        )