from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import Teacher, SchoolClass, Student

User = get_user_model()

class TestSchoolAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            is_staff=True
        )
        
        refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        self.teacher = Teacher.objects.create(
            name='John Doe',
            subject='Mathematics',
            email='john.doe@example.com'
        )
        
        self.school_class = SchoolClass.objects.create(
            name='Class 10-A',
            teacher=self.teacher
        )
        
        self.student = Student.objects.create(
            name='Alice Smith',
            roll_number='S1024',
            email='alice@example.com',
            class_assigned=self.school_class
        )
    
    def test_teacher_list(self):
        url = reverse('teacher-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'John Doe')
    
    def test_create_teacher(self):
        url = reverse('teacher-list')
        data = {
            'name': 'Jane Smith',
            'subject': 'Science',
            'email': 'jane.smith@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.count(), 2)
        self.assertEqual(Teacher.objects.get(id=2).name, 'Jane Smith')
    
    def test_class_detail(self):
        url = reverse('class-detail', args=[self.school_class.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Class 10-A')
        self.assertEqual(response.data['teacher']['name'], 'John Doe')
        self.assertEqual(len(response.data['students']), 1)
    
    def test_create_student(self):
        url = reverse('student-list')
        data = {
            'name': 'Bob Johnson',
            'rollNumber': 'S1002',
            'email': 'bob@example.com',
            'classId': self.school_class.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)
        self.assertEqual(Student.objects.get(roll_number='S1002').name, 'Bob Johnson')
    
    def test_update_teacher(self):
        url = reverse('teacher-detail', args=[self.teacher.id])
        data = {'phone': '+1234567890'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.phone, '+1234567890')
    
    def test_delete_student(self):
        url = reverse('student-detail', args=[self.student.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)
    
    def test_invalid_teacher_creation(self):
        url = reverse('teacher-list')
        data = {'name': '', 'subject': '', 'email': 'invalid-email'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('subject', response.data)
        self.assertIn('email', response.data)
    
    def test_duplicate_student_roll_number(self):
        existing_roll = 'S9999'
        Student.objects.create(
            name='Existing Student',
            roll_number=existing_roll,
            email='existing@example.com',
            class_assigned=self.school_class
        )
        
        url = reverse('student-list')
        data = {
            'name': 'Duplicate Roll',
            'rollNumber': existing_roll,
            'email': 'duplicate@example.com',
            'classId': self.school_class.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('rollNumber', response.data)
    
    def test_class_without_teacher(self):
        url = reverse('class-list')
        data = {'name': 'Class 10-B'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(SchoolClass.objects.get(name='Class 10-B').teacher)
    
    def test_teacher_detail(self):
        url = reverse('teacher-detail', args=[self.teacher.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')
    
    def test_nonexistent_teacher(self):
        url = reverse('teacher-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_student_detail(self):
        url = reverse('student-detail', args=[self.student.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Alice Smith')
    
    def test_update_student_class(self):
        new_class = SchoolClass.objects.create(name='Class 10-B')
        url = reverse('student-detail', args=[self.student.id])
        data = {'classId': new_class.id}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.class_assigned.id, new_class.id)
    
    def test_pagination(self):
        for i in range(15):
            Teacher.objects.create(
                name=f'Teacher {i}',
                subject=f'Subject {i}',
                email=f'teacher{i}@example.com'
            )
        
        url = f"{reverse('teacher-list')}?page=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        
        url = f"{reverse('teacher-list')}?page=2"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
        self.assertLessEqual(len(response.data['results']), 10)
    
    def test_search_teachers(self):
        Teacher.objects.create(name='Jane Smith', subject='Physics', email='jane@example.com')
        Teacher.objects.create(name='Bob Johnson', subject='Chemistry', email='bob@example.com')
        
        url = f"{reverse('teacher-list')}?search=Jane"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Jane Smith')
        
        url = f"{reverse('teacher-list')}?search=Chemistry"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['subject'], 'Chemistry')
    
    def test_unauthorized_access(self):
        client = APIClient()
        
        url = reverse('teacher-list')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        client.credentials(HTTP_AUTHORIZATION='Bearer invalid.token.here')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
