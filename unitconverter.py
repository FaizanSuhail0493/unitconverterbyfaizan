import streamlit as st
import time

# Session state for dark mode
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Apply dark/light mode
dark_theme = """ <style>
body {
    background-color: #1e1e2f;
    color: white;
}
.stApp {
    background: linear-gradient(45deg, #0b5394, #351c75);
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
}
h1, h3, label {
    text-align: center;
    font-size: 36px;
    color: white !important;
}
.stButton>button {
    background: linear-gradient(45deg, #0b5394, #351c75);
    color: white;
    font-size: 18px;
    padding: 10px, 20px;
    transition: 0.3s;
    box-shadow: 0px 5px 15px rgba(0, 201, 255, 0.4);
}
.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(45deg, #92fe9d, #00c9ff);
    color: black;
}
.result-box {
    font-size: 20px;
    font-weight: bold;
    text-align: center;
    background: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 10px;
    color: #00c9ff;
    margin-top: 20px;
    box-shadow: 0px 5px 15px rgba(0, 201, 255, 0.3);
}
p.description { color: white !important; }
.history-entry {color: white !important; font-weight: bold;}
.no-history {color: #ff6b6b !important; font-style: italic;}
.footer {
    text-align: center;
    margin-top: 50px;
    font-size: 14px;
    color: white;
}
</style>"""
light_theme = """ <style>
    body {
        background-color: #1e1e2f;
        color: white;
    }
    .stApp {
        background: linear-gradient(135deg, #bcbcbc, #cfe2f3);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
    }
    h1, h2, h3, h4, h5, h6, label {
        text-align: center;
        font-size: 36px;
        color: black !important;
    }
    .stButton>button {
        background: linear-gradient(45deg, #0b5394, #351c75);
        color: white;
        font-size: 18px;
        padding: 10px, 20px;
        transition: 0.3s;
        box-shadow: 0px 5px 15px rgba(0, 201, 255, 0.4);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(45deg, #92fe9d, #00c9ff);
        color: black;
    }
    .result-box {
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        color: #00c9ff;
        margin-top: 20px;
        box-shadow: 0px 5px 15px rgba(0, 201, 255, 0.3);
    }
    .history-entry {
        color: #007bff !important;
        font-weight: bold;
    }
    .no-history {
        color: #dc3545 !important; 
        font-style: italic;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        font-size: 14px;
        color: black;
    }
</style>"""

st.markdown(dark_theme if st.session_state.dark_mode else light_theme, unsafe_allow_html=True)

st.sidebar.button("🌙 Toggle Dark Mode" if st.session_state.dark_mode else "☀️ Toggle Light Mode", on_click=toggle_theme)

# Title and description
st.markdown("<h1>🧮 Advanced Unit Converter</h1>", unsafe_allow_html=True)
st.markdown('<p class="description">Convert between multiple units effortlessly!</p>', unsafe_allow_html=True)

# Sidebar menu
conversion_type = st.sidebar.selectbox("Choose Conversion Type", ["Length", "Weight", "Temperature", "Data Storage"])

# Input value
value = st.number_input("Enter Value", value=0.0, min_value=0.0, step=0.1)

# Unit selection
unit_categories = {
    "Length": ["Meters", "Kilometers", "Centimeters", "Millimeters", "Miles", "Yards", "Feet", "Inches"],
    "Weight": ["Kilograms", "Grams", "Milligrams", "Pounds", "Ounces"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Data Storage": ["Bytes", "Kilobytes", "Megabytes", "Gigabytes", "Terabytes"]
}

col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox("From", unit_categories[conversion_type])
with col2:
    to_unit = st.selectbox("To", unit_categories[conversion_type])

# Conversion functions
def length_converter(value, from_unit):
    length_units = {"Meters": 1, "Kilometers": 0.001, "Centimeters": 100, "Millimeters": 1000, "Miles": 0.000621371, "Yards": 1.09361, "Feet": 3.28084, "Inches": 39.3701}
    return {unit: (value / length_units[from_unit]) * length_units[unit] for unit in length_units}

def data_storage_converter(value, from_unit):
    data_units = {"Bytes": 1, "Kilobytes": 1024, "Megabytes": 1024**2, "Gigabytes": 1024**3, "Terabytes": 1024**4}
    return {unit: (value / data_units[from_unit]) * data_units[unit] for unit in data_units}

def weight_converter(value, from_unit):
    weight_units = {"Kilograms": 1, "Grams": 1000, "Milligrams": 1000000, "Pounds": 2.20462, "Ounces": 35.274}
    return {unit: (value / weight_units[from_unit]) * weight_units[unit] for unit in weight_units}

def temp_converter(value, from_unit):
    conversions = {
        "Celsius": {"Fahrenheit": (value * 9/5) + 32, "Kelvin": value + 273.15},
        "Fahrenheit": {"Celsius": (value - 32) * 5/9, "Kelvin": (value - 32) * 5/9 + 273.15},
        "Kelvin": {"Celsius": value - 273.15, "Fahrenheit": (value - 273.15) * 9/5 + 32}
    }
    return conversions[from_unit]

conversion_functions = {
    "Length": length_converter,
    "Weight": weight_converter,
    "Temperature": temp_converter,
    "Data Storage": data_storage_converter
}

# Convert button
if st.button("🔄 Convert"):
    result = conversion_functions[conversion_type](value, from_unit).get(to_unit, "Conversion Error")
    
    # Display result in a single result box
    st.markdown(f"""<div class='result-box' style='border: 1px solid gray; padding: 10px; border-radius: 10px; text-align: center;'>
                 <h3>{value} {from_unit} = {result:.4f} {to_unit}</h3>
                 </div>""", unsafe_allow_html=True)
    
    # Store history
    if 'history' not in st.session_state:
        st.session_state.history = []
    st.session_state.history.insert(0, f"{value} {from_unit} → {result:.4f} {to_unit}")
    st.session_state.history = st.session_state.history[:5]

# Button to toggle conversion history
if 'show_history' not in st.session_state:
    st.session_state.show_history = False

def toggle_history():
    st.session_state.show_history = not st.session_state.show_history

if st.button("📜 Show Conversion History", on_click=toggle_history):
    pass

if 'history' in st.session_state and st.session_state.history:
    st.markdown("### Recent Conversions:")
    for entry in st.session_state.history:
        st.markdown(f"<p class='history-entry'>🕒 {entry}</p>", unsafe_allow_html=True)
else:
    st.markdown("<p class='no-history'>No recent conversions.</p>", unsafe_allow_html=True)


st.markdown("<div class='footer'>Created with ❤ by Faizan Suhail</div>", unsafe_allow_html=True)