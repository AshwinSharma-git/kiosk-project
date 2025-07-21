
# 🚀 ISRO Kiosk Web Application – Internship Project

An interactive, modular, and secure **Kiosk Web Application** built as part of my internship at the **Indian Space Research Organisation (ISRO)**. Designed for deployment in ISRO campuses and visitor centers, this application enables real-time public outreach, visitor engagement, and admin control — all packed in a beautiful offline-first interface.

> 👨‍💻 Built with Flask + HTML/CSS/JS  
> 🧠 Integrated AI Chatbot using Ollama  
> 📊 Feedback & registration data stored in Google Sheets (secure access removed)  
> 🔒 Admin login & dashboard with data viewing  
> 📺 Optimized for large screens and public kiosks

---

## 🎯 Project Objective

To create a public-facing digital Kiosk System for ISRO that:
- Educates visitors and students about Indian space missions.
- Collects visitor data and feedback securely.
- Offers an **offline-ready intelligent chatbot**.
- Supports real-time administrative control.

---

## 📸 Project Preview

![Home Page UI](assets/kiosk-preview.png)

---

## 🧩 Complete Module Breakdown

### 1. 📝 Visitor Registration / Feedback
- Collects details from users visiting the ISRO premises.
- Accepts feedback and stores it directly in **Google Sheets** using the GSheets API.
- Data is **viewable only via the Admin Dashboard**.
- ⚠️ Credentials have been stripped for public GitHub version.

---

### 2. 📹 Videos
- Embeds educational and promotional ISRO videos.
- Useful for school tours and public demos.

---

### 3. 🤖 Outreach Bot (Offline AI Chatbot)
- Built using **Ollama**, an open-source LLM runner (works offline).
- Trained on ISRO-specific Q&A and FAQs.
- Flask backend handles the prompt-response flow.
- Clean frontend interface (`chatbot.html`) for real-time chat.

---

### 4. 📈 Future Missions of ISRO
- Displays cards/info panels about upcoming ISRO missions.
- Helps users stay informed about launches and research.

---

### 5. 🛰 NRSC (National Remote Sensing Centre)
- Educates users on NRSC functions and satellite data use.
- Links or embeds NRSC resources.

---

### 6. 🌐 Virtual Tour
- A guided simulation of ISRO facilities and achievements.
- Can be upgraded with 360° panoramic content later.

---

### 7. 🛠 Working Models
- Showcases miniature replicas or images/videos of:
  - PSLV
  - GSLV
  - Chandrayaan
  - Mangalyaan
  - Satellites

---

### 8. ❓ Space Quiz
- Interactive MCQ-based quiz to test visitors' knowledge.
- Can be expanded to score-based games for schools.

---

### 9. 🔐 Admin Dashboard (Login Protected)
- Admin can securely:
  - View submitted feedback and registrations (from Google Sheets).
  - Access internal content or logs.
- Username and password stored as **environment variables**:
  ```python
  os.environ.get('ADMIN_USERNAME', 'set ur username')
  os.environ.get('ADMIN_PASSWORD', 'set ur pasword')
```

---

## 🧠 AI Integration with Ollama

* 🧩 Ollama runs a local LLM model for chatbot capability.
* 🤖 Chat interface (chatbot.html) interacts with Flask server.
* 📴 Completely offline — no OpenAI or external APIs used.

> ✅ Privacy-focused & fast
> ✅ Ideal for secure ISRO internal systems

---

## 🧰 Tech Stack

| Component  | Tech Used                      |
| ---------- | ------------------------------ |
| Frontend   | HTML5, CSS3, Bootstrap, JS     |
| Backend    | Python (Flask)                 |
| AI Model   | Ollama + Local LLM             |
| Data Store | Google Sheets via API (hidden) |
| Hosting    | Localhost / Kiosk Device       |

---

  Project Structure

#```
├── static/                # CSS, images, JS files
├── templates/             # All HTML templates (pages)
│   ├── index.html         # Main homepage
│   ├── chatbot.html       # AI chatbot UI
│   ├── admin_login.html   # Admin login
│   ├── admin_dashboard.html # Admin panel
│   └── *.html             # All module pages
├── app.py                 # Flask application
├── gsheet_utils.py        # Google Sheets handler
├── requirements.txt       # Python dependencies
├── runtime.txt            # Runtime for deployment (Heroku-ready)
├── .gitignore             # Ignores sensitive files
└── README.md              # You're here!
```

---

## 🚀 How to Run Locally

> Requires Python 3.x installed.

### 🔧 Step 1: Clone the Repo

```bash
git clone https://github.com/AshwinSharma-git/kiosk-project.git
cd kiosk-project
```

### 📦 Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔐 Step 3: Set Environment Variables

```bash
# Windows
set ADMIN_USERNAME='set ur username'
set ADMIN_PASSWORD='set ur password'

# Linux/Mac
export ADMIN_USERNAME='set ur username'
export ADMIN_PASSWORD='set ur password'
```

### ▶️ Step 4: Run Flask Server

```bash
python app.py
```

Access the kiosk at:
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📌 Future Enhancements

* [ ] Add local database (SQLite or MongoDB)
* [ ] Deploy on Raspberry Pi for real kiosk mode
* [ ] QR-based attendance or quiz system
* [ ] AI voice assistant for visually impaired
* [ ] Video analytics to track visitor interaction

---

## 🧑‍💻 Developed By

**Ashwin Sharma**
ISRO Intern | B.Tech ECE | Full-stack Learner
📧 [ashwinsharmaofficial@gmail.com](mailto:ashwinsharmaofficial@gmail.com)
🔗 [GitHub](https://github.com/AshwinSharma-git) | [LinkedIn](https://www.linkedin.com/in/ashwinsharma-git/)

---

## 💖 Support & Connect

If you liked this project or found it inspiring:

* 🌟 Star this repo
* 🍴 Fork it and build your own version
* 📬 Reach out for collaborations



> *“Built with pride, purpose, and a love for space technology 🚀”*
> — Ashwin Sharma





