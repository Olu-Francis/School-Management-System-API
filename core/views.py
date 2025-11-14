from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from .models import Teacher, SchoolClass, Student
from .serializers import (
    TeacherSerializer,
    SchoolClassSerializer,
    SchoolClassDetailSerializer,
    StudentSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TeacherViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Teacher.objects.all().order_by('id')
    serializer_class = TeacherSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'subject', 'email']
    filterset_fields = ['subject']
    pagination_class = StandardResultsSetPagination


class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all().order_by('id')
    serializer_class = StudentSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'roll_number', 'email']
    filterset_fields = ['class_assigned']

    def get_queryset(self):
        queryset = super().get_queryset()
        if class_id := self.request.query_params.get('classId'):
            queryset = queryset.filter(class_assigned_id=class_id)
        return queryset


class SchoolClassViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SchoolClass.objects.all().order_by('id')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['teacher']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SchoolClassDetailSerializer
        return SchoolClassSerializer

