# Data Models

This document outlines the data models used in the School Management System API.

## Teacher

Represents a teacher in the school system.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | Integer | Auto | Unique identifier |
| name | CharField | Yes | Full name of the teacher |
| subject | CharField | Yes | Subject taught by the teacher |
| email | EmailField | Yes | Unique email address |
| phone | CharField | No | Contact number |
| created_at | DateTime | Auto | When the record was created |
| updated_at | DateTime | Auto | When the record was last updated |

## SchoolClass

Represents a class in the school.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | Integer | Auto | Unique identifier |
| name | CharField | Yes | Name of the class (e.g., "Class 10-A") |
| teacher | ForeignKey | No | Reference to the assigned teacher |
| created_at | DateTime | Auto | When the record was created |
| updated_at | DateTime | Auto | When the record was last updated |

## Student

Represents a student in the school.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | Integer | Auto | Unique identifier |
| name | CharField | Yes | Full name of the student |
| roll_number | CharField | Yes | Unique roll number |
| email | EmailField | Yes | Unique email address |
| class_assigned | ForeignKey | Yes | Reference to the assigned class |
| created_at | DateTime | Auto | When the record was created |
| updated_at | DateTime | Auto | When the record was last updated |

## Relationships

- A `Teacher` can be assigned to multiple `SchoolClass`es (one-to-many)
- A `SchoolClass` has one `Teacher` (many-to-one)
- A `SchoolClass` can have multiple `Student`s (one-to-many)
- A `Student` is assigned to one `SchoolClass` (many-to-one)

## Validation Rules

### Teacher
- `name`: Required, cannot be blank
- `subject`: Required, cannot be blank
- `email`: Required, must be unique and valid email format

### SchoolClass
- `name`: Required, cannot be blank, must be unique

### Student
- `name`: Required, cannot be blank
- `roll_number`: Required, must be unique
- `email`: Required, must be unique and valid email format
- `class_assigned`: Required, must reference an existing class