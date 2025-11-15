# Django StudyBud

Django StudyBud is a study group management platform built with Django. It allows users to join, create, and manage study rooms, connect with other learners, and foster an online community for collaborative learning.

🚀 **Live Demo:**  
[https://django-studybud.onrender.com/](https://django-studybud.onrender.com/)

---

## Features

- **User Authentication:** Sign up, log in, and securely manage your account.
- **Study Rooms:** Create, join, and participate in topic-based study rooms.
- **Discussions:** Post messages and engage with others in each room.
- **User Profiles:** Customize your public profile and see others’ activity.
- **Search:** Easily find rooms and topics matching your interests.
- **Responsive Design:** Clean, mobile-friendly interface.

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- (Optional) Virtual environment tool (e.g., `venv` or `virtualenv`)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/M-Alhbyb/Django_StudyBud.git
   cd Django_StudyBud
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

5. Open `http://127.0.0.1:8000/` in your browser.

## Project Structure

```
.
├── base/          # Main application code
├── studybud/      # Django project configuration
├── templates/     # HTML templates
├── static/        # Static files (CSS, JS, images)
├── demos/         # Example/demo files (if any)
├── db.sqlite3     # SQLite database (for development)
├── manage.py      # Django management script
├── requirements.txt
└── README.md
```

## Deployment

The app is deployed on Render.  
See the live version: [django-studybud.onrender.com](https://django-studybud.onrender.com/)

## Contributing

Contributions are welcome! Please open issues or submit pull requests to improve the project.

## License

[Specify your license here]

---

**Author**: [M-Alhbyb](https://github.com/M-Alhbyb)
