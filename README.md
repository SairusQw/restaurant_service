# 🍽️ Kitchen Service Management System

## Overview
Kitchen Service is a web-based application designed for restaurant teams to manage their internal operations efficiently. It allows tracking of dish types, ingredients, specific dishes, and the staff (cooks) responsible for preparing them.

## Key Features
- **Dashboard & Statistics:** Overview of total counts for dishes, ingredients, and staff.
- **Cook Management:** Detailed profiles for cooks, including their years of experience.
- **Dish Tracking:** Manage a list of dishes with their prices, ingredients, and assigned cooks.
- **Advanced Search:** Robust filtering system for all lists (alphabetical ordering, search by name/model with automatic whitespace stripping).
- **Secure Interactions:** Protected comment system ensuring only authenticated users can participate.
- **Pagination:** Seamless navigation through large datasets while preserving search filters.

## Tech Stack
- **Framework:** [Django](https://www.djangoproject.com/) (Python)
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Forms:** Django Crispy Forms
- **Testing:** Django TestCase (unit & integration tests)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd kitchen-service

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   
5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   
6. **Run the server:**
   ```bash
   python manage.py runserver
   
## Development & Testing
- To ensure the system's reliability, I've implemented a comprehensive test suite. Run tests with:
   ```bash
   python manage.py runserver
  
- The tests cover model validation, search filtering, and server-side permission checks for anonymous users.
