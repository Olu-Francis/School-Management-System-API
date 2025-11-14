# Installation Guide

This guide will help you set up the School Management System API on your local machine for development and testing purposes.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- PostgreSQL (recommended) or SQLite
- Git (for version control)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/school-management-api.git
cd school-management-api
```

### 2. Create and Activate Virtual Environment

#### Linux/macOS
```bash
python -m venv venv
source venv/bin/activate
```

#### Windows
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here

# Database Configuration (PostgreSQL example)
DATABASE_URL=postgres://user:password@localhost:5432/school_db

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=300    # 5 minutes
JWT_REFRESH_TOKEN_LIFETIME=86400  # 24 hours
```

### 5. Set Up Database

#### For SQLite (Development)
```bash
python manage.py migrate
```

#### For PostgreSQL (Production)
1. Create a new PostgreSQL database
2. Update the `DATABASE_URL` in `.env`
3. Run migrations:
   ```bash
   python manage.py migrate
   ```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## Running Tests

```bash
python manage.py test core.tests
```

## Production Deployment

For production deployment, consider the following:

1. **Web Server**: Use Gunicorn or uWSGI
2. **Database**: Use PostgreSQL
3. **Static Files**: Configure a web server (Nginx/Apache)
4. **Environment**: Set `DEBUG=False` and configure allowed hosts
5. **HTTPS**: Use Let's Encrypt for free SSL certificates

### Example Gunicorn Command

```bash
gunicorn --workers 3 school_project.wsgi:application
```

### Example Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/your/staticfiles/;
    }
}
```

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `False` | Enable/disable debug mode |
| `SECRET_KEY` | - | Django secret key |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | Database connection URL |
| `JWT_ACCESS_TOKEN_LIFETIME` | 300 | Access token lifetime in seconds |
| `JWT_REFRESH_TOKEN_LIFETIME` | 86400 | Refresh token lifetime in seconds |

## Troubleshooting

- **Database connection issues**: Verify your database is running and credentials are correct
- **Migrations not applying**: Try `python manage.py migrate --run-syncdb`
- **Static files not loading**: Run `python manage.py collectstatic`
- **Port already in use**: Use `lsof -i :8000` to find and kill the process

## Getting Help

If you encounter any issues, please:
1. Check the error logs
2. Search for similar issues in the issue tracker
3. Open a new issue with detailed information about the problem