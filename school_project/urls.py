"""
URL configuration for school_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/

This module defines the URL routing for the entire project, including:
- Admin interface
- REST API endpoints
- API documentation (Swagger/ReDoc)
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Import views
from core import views as core_views

# Initialize the default router for REST framework
router = routers.DefaultRouter()

# Register API endpoints with the router
router.register(r'teachers', core_views.TeacherViewSet, basename='teacher')
router.register(r'students', core_views.StudentViewSet, basename='student')
router.register(r'classes', core_views.SchoolClassViewSet, basename='class')

# Configure API documentation with drf-yasg
schema_view = get_schema_view(
    openapi.Info(
        title="School Management API",
        default_version='v1',
        description="""
        REST API for managing school resources including teachers, students, and classes.
        
        ## Authentication
        This API uses JWT authentication. Include the token in the Authorization header:
        `Authorization: Bearer <token>`
        
        ## Endpoints
        - `/api/teachers/` - Manage teachers
        - `/api/students/` - Manage students
        - `/api/classes/` - Manage classes
        
        ## Documentation
        - Swagger UI: [/swagger/](/swagger/)
        - ReDoc: [/redoc/](/redoc/)
        - Schema: [/swagger.json](/swagger.json)
        """,
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Public schema, but actual API requires auth
)

urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints (versioned under /api/)
    path('api/', include(router.urls)),
    
    # JWT authentication endpoints
    path('api/token/', 
         TokenObtainPairView.as_view(), 
         name='token_obtain_pair'),
    path('api/token/refresh/', 
         TokenRefreshView.as_view(), 
         name='token_refresh'),
    
    # API Documentation
    # - JSON schema
    path('swagger.json', 
         schema_view.without_ui(cache_timeout=0), 
         name='schema-json'
    ),
    # - Swagger UI
    path('swagger/', 
         schema_view.with_ui('swagger', cache_timeout=0), 
         name='schema-swagger-ui',
    ),
    # - ReDoc
    path('api/docs/', 
         schema_view.with_ui('swagger', cache_timeout=0), 
         name='schema-swagger-ui',
    ),
    path('api/redoc/', 
         schema_view.with_ui('redoc', cache_timeout=0), 
         name='schema-redoc',
    ),
]
