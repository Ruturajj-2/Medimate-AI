# Medimate-AI
MediMate AI is an intelligent medical chatbot that provides instant health guidance using AI. It features user authentication, real-time chat, chat history, and profile management. Built with Flask and OpenRouter API, it offers a simple and interactive healthcare assistant experience.

#Features

User Authentication (Login & Signup)
AI-powered Chat System
Medical Assistant (General Advice)
Recent Chat History
New Consultation (Reset Chat)
Profile Dropdown with Logout
Chat Access Control (Login Required)

---

#Tech Stack

**Frontend:** HTML, CSS, JavaScript
**Backend:** Python (Flask)
**Database:** SQLite
**AI API:** OpenRouter (LLaMA 3 Model)

## 📁 Project Structure

```
medimate/
│
├── app.py
├── users.db
│
├── templates/
│   ├── index.html
│   ├── login.html
│   └── signup.html
│
└── static/
    ├── style.css
    └── script.js
```

---

## Installation & Setup

#Install Dependencies
pip install flask openai
```

### 3️⃣ Set API Key

Replace in `app.py`:

```
YOUR_API_KEY
```

Or use environment variable:

```
set OPENROUTER_API_KEY=your_key   (Windows)
```

### 4️⃣ Run the Project

```
python app.py
```

### 5️⃣ Open in Browser

```
http://127.0.0.1:5000

## 📌 Future Improvements

* 🧠 AI disease prediction system
* 💬 Chat history with full conversation view
* 🧾 User dashboard
* 🌐 Deployment (Live Website)
* 🖼 Profile image upload

---

## 👨‍💻 Author

**Ruturaj Makwana**
Medimate AI Project

---

## 📄 License

This project is for educational purposes. All rights reserved.

