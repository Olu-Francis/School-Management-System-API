# School Management System API

A RESTful API for managing school resources including teachers, students, and classes.

## Features

- **Teacher Management**: Create, read, update, and delete teacher records
- **Class Management**: Manage school classes and assign teachers
- **Student Management**: Handle student records and class assignments
- **RESTful API**: Built with Django REST Framework
- **Filtering & Search**: Filter and search across resources
- **Comprehensive Testing**: Unit tests for all API endpoints

## Prerequisites

- Python 3.10+
- pip (Python package manager)
- SQLite (included with Python)

## Getting Started

### 1. Clone the Repository

```bash
git clone git@github.com:Olu-Francis/School-Management-System-API.git
cd school_project
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root with the following content:

```bash
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
```

> **Note**: Replace `your-secret-key-here` with a secure secret key for production use.

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser 

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

### 7. Access the API

The API will be available at `http://127.0.0.1:8000/api/`

You can use tools like `curl`, Postman, or the browsable API interface to interact with the API endpoints.

The API will be available at `http://127.0.0.1:8000/`

## API Documentation

### Base URL
```
http://127.0.0.1:8000/api/
```

### Authentication
To access you need to login as a superuser or given permission from a superuser

### Endpoints

#### Teachers

- **GET /api/teachers/** - List all teachers
- **POST /api/teachers/** - Create a new teacher
- **GET /api/teachers/{id}/** - Get teacher details
- **PUT /api/teachers/{id}/** - Update teacher
- **DELETE /api/teachers/{id}/** - Delete teacher

**Example Request (Create Teacher):**
```http
POST /api/teachers/
Content-Type: application/json

{
    "name": "Jane Smith",
    "subject": "Physics",
    "email": "jane@example.com",
    "phone": "1234567890"
}
```

#### Classes

- **GET /api/classes/** - List all classes
- **POST /api/classes/** - Create a new class
- **GET /api/classes/{id}/** - Get class details (includes teacher and students)
- **PUT /api/classes/{id}/** - Update class
- **DELETE /api/classes/{id}/** - Delete class

**Example Request (Create Class):**
```http
POST /api/classes/
Content-Type: application/json

{
    "name": "11th Grade - A",
    "teacher": 1
}
```

#### Students

- **GET /api/students/** - List all students
- **POST /api/students/** - Create a new student
- **GET /api/students/{id}/** - Get student details
- **PUT /api/students/{id}/** - Update student
- **DELETE /api/students/{id}/** - Delete student

**Example Request (Create Student):**
```http
POST /api/students/
Content-Type: application/json

{
    "name": "John Doe",
    "roll_number": "S1001",
    "email": "john@example.com",
    "class_assigned": 1
}
```

### Filtering and Search

#### Teachers
- Filter by subject: `/api/teachers/?subject=Mathematics`
- Search: `/api/teachers/?search=John` (searches in name, subject, and email)

#### Students
- Filter by class: `/api/students/?class_assigned=1`
- Search: `/api/students/?search=John` (searches in name, roll_number, and email)

### Testing

### Running Tests

To run the test suite, use one of the following commands in the project directory:

1. Run all tests in the core app:
   ```bash
   python manage.py test core.tests
   ```

### Test Coverage

To check test coverage:

1. Install pytest-cov if not already installed:
   ```bash
   pip install pytest-cov
   ```

### Common Test Issues

If you encounter import errors when running tests, try:
1. Ensuring you're in the project root directory
2. Activating your virtual environment
3. Installing all requirements: `pip install -r requirements.txt`
4. Making sure there's an empty `__init__.py` in the tests directory
5. Using the `-m pytest` approach instead of Django's test runner if issues persist

## Running Tests

To run the test suite, use:

```bash
python manage.py test core.tests.test_views -v 2
```

This will run all the test cases and show detailed output.

## Deployment

For production deployment, consider:

1. Using a production-grade web server (Gunicorn, uWSGI)
2. Setting up a production database (PostgreSQL, MySQL)
3. Configuring environment variables for sensitive data
4. Enabling HTTPS
5. Setting up proper authentication and permissions

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Support

For support, please open an issue in the repository.
