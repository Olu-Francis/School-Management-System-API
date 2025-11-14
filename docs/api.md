# API Documentation

## Base URL
```
http://http://127.0.0.1:8000/api/
```

## Authentication
This API uses JWT (JSON Web Tokens) for authentication. Include the token in the `Authorization` header:

```
Authorization: Bearer your.jwt.token.here
```

## Endpoints

### Authentication

#### Get JWT Token

```http
POST /api/token/
```

**Request Body:**
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**
```json
{
    "refresh": "your.refresh.token",
    "access": "your.access.token"
}
```

### Teachers

#### List All Teachers

```http
GET /api/teachers/
```

**Query Parameters:**
- `search`: Search by name, subject, or email (case-insensitive)
- `subject`: Filter by subject (exact match)
- `page`: Page number for pagination
- `page_size`: Number of items per page (default: 10)

**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "John Doe",
            "subject": "Mathematics",
            "email": "john.doe@example.com",
            "phone": "+1234567890"
        }
    ]
}
```

### Classes

#### List All Classes

```http
GET /api/classes/
```

**Query Parameters:**
- `search`: Search by class name (case-insensitive)
- `teacher`: Filter by teacher ID

**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Class 10-A",
            "teacherId": 1
        }
    ]
}
```

### Students

#### List All Students

```http
GET /api/students/
```

**Query Parameters:**
- `search`: Search by name, roll number, or email (case-insensitive)
- `classId`: Filter by class ID
- `class_assigned`: Alternative filter by class ID (for backward compatibility)

**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Alice Smith",
            "rollNumber": "S1024",
            "email": "alice@example.com",
            "classId": 1
        }
    ]
}
```

## Error Responses

### 400 Bad Request
```json
{
    "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
    "detail": "A server error occurred."
}
```