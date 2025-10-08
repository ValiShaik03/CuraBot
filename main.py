import os
import sqlite3
import hashlib
import streamlit as st
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

# ==== Load environment variables ====
load_dotenv()

# ==== API KEYS ====
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# ==== Initialize clients ====
import openai
import cohere
import google.generativeai as genai
from groq import Groq

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
if COHERE_API_KEY:
    cohere_client = cohere.Client(COHERE_API_KEY)
else:
    cohere_client = None
if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)
else:
    groq_client = None
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ==== Database setup ====
conn = sqlite3.connect('users1.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS users1 (
    firstname TEXT,
    email TEXT UNIQUE,
    password TEXT,
    last_login TEXT
)
''')
conn.commit()

# ==== Utility functions ====
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    return hash_password(password) == hashed

# ==== RAG PDF processing ====
def process_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(text)
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
    return vectorstore

# ==== AI response functions ====
def get_openai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content'].strip()

def get_groq_response(prompt):
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def get_gemini_response(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()

def get_cohere_response(prompt):
    response = cohere_client.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=200
    )
    return response.generations[0].text.strip()

def get_ai_response(prompt):
    response = None
    errors = []
    try:
        if OPENAI_API_KEY:
            response = get_openai_response(prompt)
    except Exception as e:
        errors.append(f"OpenAI: {e}")

    try:
        if not response and GROQ_API_KEY:
            response = get_groq_response(prompt)
    except Exception as e:
        errors.append(f"Groq: {e}")

    try:
        if not response and GEMINI_API_KEY:
            response = get_gemini_response(prompt)
    except Exception as e:
        errors.append(f"Gemini: {e}")

    try:
        if not response and COHERE_API_KEY:
            response = get_cohere_response(prompt)
    except Exception as e:
        errors.append(f"Cohere: {e}")

    if not response:
        print("AI Errors:", errors)
        response = "This is a demo response. Connect your API keys for real answers."
    return response

# ==== Streamlit config ====
st.set_page_config(page_title="CuraBot - HealthMate", page_icon="🤖", layout="wide")

# ==== Session defaults ====
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "firstname" not in st.session_state:
    st.session_state.firstname = ""
if "menu_selection" not in st.session_state:
    st.session_state.menu_selection = "Home"

# ==== Sidebar ====
options = ["Home", "Profile", "General Medical Bot", "Chat with Reports"]
if st.session_state.menu_selection not in options:
    st.session_state.menu_selection = "Home"
default_index = options.index(st.session_state.menu_selection)

with st.sidebar:
    st.markdown("# CuraBot - HealthMate")
    st.write("---")
    menu = option_menu(
        None,
        options,
        icons=['house', 'person-circle', 'heart', 'file-earmark-text'],
        menu_icon="cast",
        default_index=default_index,
        orientation="vertical",
        styles={
            "container": {"padding": "0px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"6px 0"},
            "nav-link-selected": {"background-color": "#ff6b6b", "color":"white"},
        }
    )
    st.session_state.menu_selection = menu

selection = st.session_state.menu_selection

# ==== HOME PAGE ====
if selection == "Home":
    st.markdown("<h1 style='font-size:54px; margin-bottom: -8px;'>🤍 Welcome to CuraBot</h1>", unsafe_allow_html=True)
    st.subheader("Your personal AI medical assistant — fast, private, and easy to use.")
    st.markdown("### Features")
    st.markdown(
        """
        - **General Medical Bot** — Ask general health & symptom questions.  
        - **Chat with Reports** — Upload medical reports (PDF) and ask questions.  
        - **Multiple AI Providers** — OpenAI, Groq, Gemini, Cohere.  
        - **Profile & Account** — Sign up or log in to access restricted features.
        """
    )
    if st.button("Get Started"):
        st.session_state.menu_selection = "Profile"
        st.rerun()

# ==== PROFILE PAGE ====
elif selection == "Profile":
    st.header("Profile & Account")
    if not st.session_state.logged_in:
        tab = st.radio("Choose action", ["Login", "Sign Up"], horizontal=True)
        if tab == "Login":
            st.subheader("Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login", key="do_login"):
                c.execute("SELECT firstname, password FROM users1 WHERE email=?", (email,))
                result = c.fetchone()
                if result and verify_password(password, result[1]):
                    st.session_state.logged_in = True
                    st.session_state.firstname = result[0]
                    from datetime import datetime
                    c.execute("UPDATE users1 SET last_login=? WHERE email=?", (datetime.now().isoformat(), email))
                    conn.commit()
                    st.success(f"Welcome back, {result[0]}!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
        else:
            st.subheader("Sign Up")
            firstname = st.text_input("First Name", key="signup_firstname")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")
            if st.button("Sign Up", key="do_signup"):
                if not (firstname and email and password and confirm):
                    st.warning("Please fill all fields.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                else:
                    c.execute("SELECT * FROM users1 WHERE email=?", (email,))
                    if c.fetchone():
                        st.warning("Email already exists. Try logging in.")
                    else:
                        hashed = hash_password(password)
                        c.execute("INSERT INTO users1 (firstname,email,password,last_login) VALUES (?, ?, ?, ?)",
                                  (firstname, email, hashed, ""))
                        conn.commit()
                        st.success("Account created! You can now log in.")
                        st.rerun()
    else:
        st.success(f"Logged in as **{st.session_state.firstname}**")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.firstname = ""
            st.rerun()

# ==== GENERAL MEDICAL BOT ====
elif selection == "General Medical Bot":
    if not st.session_state.logged_in:
        st.info("Please log in from the Profile page to use the General Medical Bot.")
    else:
        st.header(f"General Medical Bot — Hello, {st.session_state.firstname}")

        if "gen_history" not in st.session_state:
            st.session_state.gen_history = []

        user_query = st.text_input("Describe your symptoms or ask a health question:")

        if st.button("Ask", key="gen_ask_btn"):
            if user_query.strip():
                with st.spinner("Analyzing..."):
                    answer = get_ai_response(user_query)
                    st.session_state.gen_history.append({"user": user_query, "bot": answer})
                    st.rerun()
            else:
                st.info("Please enter a question.")

        if st.session_state.gen_history:
            st.markdown("### Conversation History")
            for item in st.session_state.gen_history:
                st.markdown(f"**You:** {item['user']}")
                st.markdown(f"**🤖 CuraBot:** {item['bot']}")
                st.write("---")

# ==== CHAT WITH REPORTS ====
elif selection == "Chat with Reports":
    if not st.session_state.logged_in:
        st.info("Please log in from the Profile page to upload reports and ask about them.")
    else:
        st.header("Chat with Reports")

        if "report_history" not in st.session_state:
            st.session_state.report_history = []

        uploaded_file = st.file_uploader("Upload your medical report (PDF)", type="pdf", key="report_uploader")
        question = st.text_input("Ask a question about this report:")

        if st.button("Ask about report", key="ask_report_btn"):
            if not uploaded_file:
                st.warning("Please upload a PDF first.")
            elif not question.strip():
                st.info("Please type a question about the report.")
            else:
                with st.spinner("Processing PDF and generating answer..."):
                    vectorstore = process_pdf(uploaded_file)
                    all_text = "\n".join([doc.page_content for doc in vectorstore.docstore._dict.values()])
                    prompt = f"User report:\n{all_text}\n\nQuestion: {question}"
                    answer = get_ai_response(prompt)
                    st.session_state.report_history.append({"user": question, "bot": answer})
                    st.rerun()

        if st.session_state.report_history:
            st.markdown("### Report Chat History")
            for item in st.session_state.report_history:
                st.markdown(f"**You:** {item['user']}")
                st.markdown(f"**🤖 CuraBot:** {item['bot']}")
                st.write("---")

# ==== fallback ====
else:
    st.write("Select an option from the sidebar.")
