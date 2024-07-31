import streamlit as st
from dotenv import load_dotenv
from fpdf import FPDF
import os
import google.generativeai as genai
from io import BytesIO

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="TRIP PLANNER",
    page_icon="🌴",
    layout="wide",
)


# Configure Google generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# Function to generate response from Gemini model
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

# Function to generate PDF from text
def generate_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Split the text into lines
    lines = text.split('\n')
    
    # Add each line of text as a separate cell
    for line in lines:
        pdf.cell(200, 5, txt=line, ln=True)
    
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes

# Function to style the sidebar
def set_sidebar_style():
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def plan_new_trip():
    st.title("Plan New Trip 🗺️")
    destination = st.text_input("Destination:", "")
    from_date = st.date_input("From Date:")
    to_date = st.date_input("To Date:")
    budget = st.selectbox("Budget:", ["Low", "Mid", "High"])
    trip_type = st.radio("Trip Type:", ["Solo", "Couple", "Family", "Friends"])
    activity_types = st.multiselect("Activity Types:", ["Exploring temples", "Visiting historical sites", "Enjoying nature","Adventure"])
    submit = st.button("Generate Itinerary")

    if submit:
        prompt = f"Plan a trip to {destination} from {from_date.strftime('%Y-%m-%d')} to {to_date.strftime('%Y-%m-%d')}. "
        prompt += f"The budget for the trip is {budget.lower()} and the trip type is {trip_type.lower()}. "
        prompt += f"The main activities you'd like to include are {', '.join(activity_types)}. "
        prompt += "Please generate a personalized itinerary, provide tips for the trip, and forecast the weather."
        
        response = get_gemini_response(prompt)
        st.subheader("Generated Itinerary:")
        st.write(response)

        # Save response as PDF
        if response:
            pdf_bytes = generate_pdf(response)
            st.download_button(label="Download PDF", data=pdf_bytes, file_name='trip_itinerary.pdf', mime='application/pdf')

# Function for the "Feedback" page
def feedback():
    st.title("Feedback 📝")
    st.write("Please provide your feedback using the form below:")
    # Embed Google Form using Markdown
    st.markdown(
        """<style>
    /* Container */
    .form-container {
        max-width: 400px;
        margin: 0;
    }

    /* Labels */
    label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    }

    /* Input fields and textarea */
    input[type="text"],
    input[type="email"],
    textarea {
        width: 100%;
        padding: 8px;
        margin-bottom: 15px;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
    }

    /* Button */
    button[type="submit"] {
        background-color: #4caf50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    button[type="submit"]:hover {
        background-color: #45a049;
    }
</style>

<div class="form-container">
<form action="https://submit-form.com/Wf715lesS">
        <label for="name">Name</label>
        <input type="text" id="name" name="name" placeholder="Name" required="" />
        <label for="email">Email</label>
        <input type="email" id="email" name="email" placeholder="Email" required="" />
        <label for="message">Message</label>
        <textarea
            id="message"
            name="message"
            placeholder="Message"
            required=""
        ></textarea>
        <button type="submit">Send</button>
    </form>
</div>

        """, unsafe_allow_html=True
    )


# Function for the "Home" page
def home():
    st.title("Home 🏠")
    st.write("Welcome to the home page. Add your content here.")

# Set sidebar style
set_sidebar_style()

# Sidebar navigation
page = st.sidebar.radio("Navigation", [ "Plan New Trip", "Feedback", "Home"])

# Page selection based on sidebar navigation
if page == "Plan New Trip":
    plan_new_trip()
elif page == "Feedback":
    feedback()
elif page == "Home":
    home()
    
