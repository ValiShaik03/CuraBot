# CuraBot — HealthMate

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg) ![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-orange.svg) ![SQLite](https://img.shields.io/badge/SQLite-3.41.2-lightgrey.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg) 

🤖 **CuraBot (HealthMate)** is a personal AI-powered health assistant. It lets you:

- Ask general health & symptom questions  
- Upload PDF medical reports & ask targeted questions  
- Maintain conversation history  
- Use multiple AI providers (OpenAI, Groq, Gemini, Cohere)  

---
## Tech Stack

- **Python 3.10+**  
- **Streamlit** — Web app interface  
- **SQLite** — Local database for storing user accounts and conversation history  
- **LangChain & PyPDF2** — PDF processing and RAG (retrieval-augmented generation)  
- **OpenAI / Groq / Google Gemini / Cohere** — AI response providers  
- **dotenv** — For managing API keys securely 

## Folder Structure
```
healthmate-curabot/
├─ main.py
├─ requirements.txt
├─ .env
├─ users1.db
├─ README.md
├─ screenshots/
    ├─ homepage
    ├─ signuppage
    ├─ loginpage
    ├─ general_medical_bot
    ├─ chat_with_reports
```
## Project Preview

## 🖼️ Project Preview

HomePage<br>
![CuraBot Homepage](https://github.com/ValiShaik03/CuraBot/blob/d417bea099f5fc0050eb9a6fd2659523b928fc86/screenshots/home.png) <br>
SignUpPage
![CuraBot signuppage](https://github.com/ValiShaik03/CuraBot/blob/d417bea099f5fc0050eb9a6fd2659523b928fc86/screenshots/signup.png)<br>
LogInPage
![CuraBot_loginpage](https://github.com/ValiShaik03/CuraBot/blob/d417bea099f5fc0050eb9a6fd2659523b928fc86/screenshots/login.png)<br>
General Medical Bot
![CuraBot_general_medical_bot](https://github.com/ValiShaik03/CuraBot/blob/d417bea099f5fc0050eb9a6fd2659523b928fc86/screenshots/general_medical_bot.png)<br>
Chat With Reports
![CuraBot_chat_with_reports](https://github.com/ValiShaik03/CuraBot/blob/d417bea099f5fc0050eb9a6fd2659523b928fc86/screenshots/chat_with_reports.png)
---

## Features

| Feature | Description |
|---------|-------------|
| General Medical Bot | Ask health questions & get AI responses |
| Chat with Reports | Upload PDF reports & ask questions |
| Profile & Login | Secure authentication & session management |
| Conversation History | Keep track of your previous queries & AI responses |
| Multi-AI Support | OpenAI, Groq, Gemini, Cohere (if API keys configured) |

---

## Installation

```bash
# Clone repository
git clone https://github.com/your-username/healthmate-curabot.git
cd healthmate-curabot

# Install dependencies
pip install -r requirements.txt

# Optional: Add .env file for AI API keys
# OPENAI_API_KEY=your_openai_key
# GROQ_API_KEY=your_groq_key
# GEMINI_API_KEY=your_gemini_key
# COHERE_API_KEY=your_cohere_key

# Run Streamlit app
streamlit run main.py
