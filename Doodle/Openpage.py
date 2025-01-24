import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK
cred = credentials.Certificate('/Users/prajwalu/dev/SRH/Python2/Doodle_frontend/Doodle_main/Doodle/doodle-3e015-351df71b0db7.json')
try:
    firebase_admin.initialize_app(cred)
except ValueError:
    # Firebase already initialized
    pass

# State management for navigation
if "page" not in st.session_state:
    st.session_state.page = "home"  # Default page is the home page
if "user" not in st.session_state:
    st.session_state.user = None

# Helper Functions
def signup(email, password, display_name):
    """
    Function to sign up a new user using Firebase Authentication.
    """
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        st.success(f"Account created successfully for {display_name}! You can now log in.")
        return user
    except auth.EmailAlreadyExistsError:
        st.error("This email is already in use. Please try logging in.")
    except Exception as e:
        st.error(f"Error: {e}")
    return None


def login(email, password):
    """
    Function to log in a user using Firebase Authentication.
    """
    try:
        user = auth.get_user_by_email(email)
        # Simulating login (Firebase Admin SDK doesn't directly handle user passwords)
        if user:
            st.session_state.user = user
            st.success(f"Welcome back, {user.display_name or 'User'}!")
            return True
    except firebase_admin._auth_utils.UserNotFoundError:
        st.error("User not found. Please check your credentials.")
        return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False


def logout():
    """
    Function to log out the user.
    """
    st.session_state.user = None
    st.session_state.page = "home"
    st.success("You have been logged out.")

# Page Navigation
if st.session_state.page == "home":
    # Home Page
    st.title("Welcome to Doodle")
    st.write("**Doodle: Empowering Recruitment with AI**")
    st.write(
        """
        Doodle is an AI-powered recruitment platform designed to streamline the hiring process for recruiters and 
        provide candidates with tailored opportunities. Whether you're a recruiter seeking top talent or a candidate 
        looking for your dream job, Doodle has got you covered.
        """
    )
    st.subheader("Features")
    st.write("- Intelligent candidate matching using AI.")
    st.write("- Streamlined application and evaluation processes.")
    st.write("- Secure and seamless authentication.")
    st.write("- Tailored job opportunities for candidates.")

    st.subheader("Get Started")
    if st.button("Recruiter Login/Signup"):
        st.session_state.page = "signup_recruiter"
    if st.button("Candidate Login"):
        st.session_state.page = "login_candidate"

    st.write("---")
    st.write("[About Us](#) | [Contact](#) | [Help/FAQ](#)")

elif st.session_state.page == "signup_recruiter":
    # Recruiter Signup Page
    st.subheader("Recruiter Signup")
    with st.form("signup_form"):
        display_name = st.text_input("Name", placeholder="Enter your full name")
        email = st.text_input("Email", placeholder="Enter your email address")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
        submitted = st.form_submit_button("Sign Up")

        if submitted:
            if not display_name or not email or not password or not confirm_password:
                st.error("Please fill in all the fields.")
            elif password != confirm_password:
                st.error("Passwords do not match. Please try again.")
            else:
                signup(email, password, display_name)

    if st.button("Already have an account? Log In"):
        st.session_state.page = "login_recruiter"

elif st.session_state.page == "login_recruiter":
    # Recruiter Login Page
    st.subheader("Recruiter Login")
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email address")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Log In")

        if submitted:
            if not email or not password:
                st.error("Please fill in all the fields.")
            else:
                login(email, password)

    if st.button("Don't have an account? Sign Up"):
        st.session_state.page = "signup_recruiter"

elif st.session_state.page == "login_candidate":
    # Candidate Login Page
    st.subheader("Candidate Login")
    with st.form("candidate_login_form"):
        email = st.text_input("Email", placeholder="Enter your email address")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Log In")

        if submitted:
            if not email or not password:
                st.error("Please fill in all the fields.")
            else:
                login(email, password)

    if st.button("Back to Home"):
        st.session_state.page = "home"

# Authenticated Area
if st.session_state.user:
    st.subheader(f"Welcome, {st.session_state.user.display_name}")
    st.write("You are now logged in.")
    if st.button("Logout"):
        logout()
