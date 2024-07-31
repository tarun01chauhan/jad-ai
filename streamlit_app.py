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

# Function for the "About Us" page
def about_us():
    st.title("About Us ℹ️")
    st.write("At JAD AI, we're passionate about making travel planning easy and enjoyable for everyone. "
             "Our team of experienced professionals is dedicated to providing innovative solutions "
             "that help travelers explore the world with confidence.")
    st.write('\n' * 3)
    # Team Bios
    st.header("MEET OUR TEAM")
    st.write("Get to know the talented individuals behind JAD AI:")
    
    # Team Members
    team_members = [
        {"name": "Aryan Patel", "role": "User Interface", "bio": "Aryan is a creative designer who focuses on delivering intuitive user experiences.",
         "image": "1aryan.jpg"},
        {"name": "Dhairya Patel", "role": "API Research", "bio": "Dhairya is a tech enthusiast with expertise in API research and integration.",
         "image": "1dhairya.jpg"},
        {"name": "Jay Vaishnav", "role": "Documentation", "bio": "Jay is a detail-oriented writer who specializes in technical documentation and content creation.",
         "image": "3jay.jpg"},
    ]
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(team_members[0]["image"])
        st.write(team_members[0]["name"])
        st.write(team_members[0]["role"])
        st.write(team_members[0]["bio"])

    with col2:
        st.image(team_members[1]["image"])
        st.write(team_members[1]["name"])
        st.write(team_members[1]["role"])
        st.write(team_members[1]["bio"])

    with col3:
        st.image(team_members[2]["image"])
        st.write(team_members[2]["name"])
        st.write(team_members[2]["role"])
        st.write(team_members[2]["bio"])


    st.write('\n' * 3)
    
    st.header("CONNECT WITH US")
    st.write("Follow us on social media to stay updated:")

    social_media = [
        {"platform": "Instagram", "handle": " @jadai.travel", "icon": "instagram.png"},
        {"platform": "Gmail", "handle": " jadai.travel@gmail.com", "icon": "email.png"},
    ]

    col1, col2 = st.columns([1,15])

# Iterate over social media platforms
    for platform in social_media:
        # Add icon and handle to respective columns
        with col1:
            st.image(f"{platform['icon']}", width=25)
        with col2:
             st.markdown(f"<p style='font-size:16px;'>{platform['platform']}: {platform['handle']}</p>", unsafe_allow_html=True)

        st.write('\n' * 3)
    
    # Customer Testimonials
    st.header("CUSTOMER TESTIMONIALS")
    
    testimonials = [
        {"user": "Sarah Patel", "review": "I absolutely love using JAD AI for all my travel planning needs! The platform is intuitive, and it helps me discover hidden gems in every destination. Highly recommended. Thanks to JAD Ai!"},
        {"user": "Aditya Kumar", "review": "JAD AI has revolutionized the way I plan my trips. The personalized itineraries and insightful recommendations make every journey memorable. Thanks to the team for their exceptional service!"},
        {"user": "Yogendra ", "review": "As a frequent traveler, I rely on JAD AI to streamline my itinerary planning process. The platform's user-friendly interface and AI-powered suggestions have saved me countless hours of research!"}
    ]
    st.write('\n' * 3)
    testimonial_cols = st.columns(3)
    
    for i, testimonial in enumerate(testimonials):
        with testimonial_cols[i % 3]:
            st.markdown(f"<p style='text-align:center; font-weight:bold;font-size:20px;'>{testimonial['user']}</p>", unsafe_allow_html=True)
            st.write(f"\"{testimonial['review']}\"")
            st.write("---")

# Function for the "Plan New Trip" page
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
<form action="https://submit-form.com/W8y04J5LF">
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
page = st.sidebar.radio("Navigation", ["About Us", "Plan New Trip", "Feedback", "Home"])

# Page selection based on sidebar navigation
if page == "About Us":
    about_us()
elif page == "Plan New Trip":
    plan_new_trip()
elif page == "Feedback":
    feedback()
elif page == "Home":
    home()
    
