# 📚 Bookshelf API

**A clean, minimal RESTful API for managing your bookshelf** — create, read, update, and delete books with ease.  
Built with Python, lightweight by design, and ready to run locally or deploy anywhere.

[![Repo](https://img.shields.io/badge/repo-bookshelf--api-181717?logo=github)](https://github.com/sooraj-m-s/bookshelf-api)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)

---

## Stack and Core Concepts

- Framework: Django + Django REST Framework
- Auth: JWT (rest_framework_simplejwt)
- Apps: users, books, reading_lists
- Database: PostgreSQL (configure via env)
- Media: Book cover uploads via Cloudinary (upload preset required)
- Global requirements:
  - All API endpoints under /api/
  - Default permission: IsAuthenticated (JWT)
  - Throttling: anon 100/hour, user 1000/hour
  - Pagination: page/page_size on list endpoints (defaults: size=10, max=100)

---

## 🚀 Getting Started

**Prerequisites**
- Python 3.10+
- pip or poetry 
- Git

**Clone and set up:**
```bash
git clone https://github.com/sooraj-m-s/bookshelf-api.git
cd bookshelf-api

# Create & activate virtual environment
python -m venv .bookshelf_env

# Windows
. .bookshelf_env/Scripts/activate

# macOS/Linux
source .bookshelf_env/bin/activate

# Install dependencies
pip install -r requirements.txt
# or
poetry install && poetry shell
```

---

## 🔧 Configuration

Set environment variables (create a `.env`):

---

## Running the API

- Apply migrations, then run the server:
  - python manage.py migrate
  - python manage.py runserver 0.0.0.0:8000

Base URL:
- http://localhost:8000/api/

Authentication:
- Obtain JWT via login, then include:
  - Authorization: Bearer <access_token>

---

## Contributing

We welcome contributions to Bookshelf! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


Please ensure your code follows our coding standards and includes appropriate tests.

---

## 🙌 Acknowledgements
- [Python](https://www.python.org/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [JWT (JSON Web Tokens)](https://jwt.io/)
- [Cloudinary](https://cloudinary.com/)
- You, for checking out **Bookshelf API**!

---


## 📞 Contact

For questions or feedback, reach out to **[soorajms4@gmail.com](mailto:soorajms4@gmail.com)**.