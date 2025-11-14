from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=100, help_text="Full name of the teacher")
    subject = models.CharField(max_length=100, help_text="Subject taught by the teacher")
    email = models.EmailField(unique=True, help_text="Unique email address")
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="Contact number (optional)"
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return f"{self.name} ({self.subject})"

class SchoolClass(models.Model):
    name = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Name of the class (e.g., 'Class 10-A')"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name="classes",
        blank=True,
        help_text="Primary teacher assigned to this class"
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100, help_text="Full name of the student")
    roll_number = models.CharField(
        max_length=50, 
        unique=True,
        help_text="Unique roll number"
    )
    email = models.EmailField(
        unique=True,
        help_text="Unique email address"
    )
    class_assigned = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="students",
        help_text="The class to which the student is assigned"
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

