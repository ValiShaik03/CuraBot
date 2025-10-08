# CuraBot — HealthMate

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg) ![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-orange.svg) ![SQLite](https://img.shields.io/badge/SQLite-3.41.2-lightgrey.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg) 

🤖 **CuraBot (HealthMate)** is a personal AI-powered health assistant. It lets you:

- Ask general health & symptom questions  
- Upload PDF medical reports & ask targeted questions  
- Maintain conversation history  
- Use multiple AI providers (OpenAI, Groq, Gemini, Cohere)  

---

## Demo

![CuraBot Demo GIF](https://github.com/ValiShaik03/CuraBot/blob/1f32f3d37a6a0407d345e450122321bd44bfbfc9/screenshots/home.png)  

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
