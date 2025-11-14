from rest_framework import serializers, validators
from .models import Teacher, SchoolClass, Student

class SimpleTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'subject', 'email']
        read_only_fields = fields

class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'roll_number', 'email']
        read_only_fields = fields

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'subject', 'email', 'phone']
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True, 'allow_blank': False},
            'subject': {'required': True, 'allow_blank': False}
        }

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name is required.")
        return value

    def validate_subject(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Subject is required.")
        return value

class StudentSerializer(serializers.ModelSerializer):
    rollNumber = serializers.CharField(
        source='roll_number',
        help_text="Unique identifier for the student within their class",
        validators=[
            validators.UniqueValidator(
                queryset=Student.objects.all(),
                message='A student with this roll number already exists.'
            )
        ]
    )
    classId = serializers.PrimaryKeyRelatedField(
        source='class_assigned',
        queryset=SchoolClass.objects.all(),
        help_text="ID of the class this student is assigned to"
    )
    
    class Meta:
        model = Student
        fields = ['id', 'name', 'rollNumber', 'email', 'classId']
        read_only_fields = ['id']
        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False},
            'email': {'required': True}
        }
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'classId' in ret and ret['classId'] is not None:
            ret['classId'] = str(ret['classId'])
        return ret
    
    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name is required.")
        return value
    
    def validate_rollNumber(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Roll number is required.")
        return value

class SchoolClassSerializer(serializers.ModelSerializer):
    teacherId = serializers.PrimaryKeyRelatedField(
        source='teacher',
        queryset=Teacher.objects.all(),
        allow_null=True,
        required=False,
        help_text="ID of the teacher assigned to this class (optional)"
    )
    
    class Meta:
        model = SchoolClass
        fields = ['id', 'name', 'teacherId']
        read_only_fields = ['id']
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'teacherId' in ret and ret['teacherId'] is not None:
            ret['teacherId'] = str(ret['teacherId'])
        return ret
    
    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Class name is required.")
        return value

class SchoolClassDetailSerializer(SchoolClassSerializer):
    teacher = SimpleTeacherSerializer(
        read_only=True,
        help_text="Detailed information about the class teacher"
    )
    students = StudentListSerializer(
        many=True,
        read_only=True,
        help_text="List of all students enrolled in this class"
    )
    
    class Meta:
        model = SchoolClass
        fields = ['id', 'name', 'teacherId', 'teacher', 'students']
        read_only_fields = ['teacher', 'students']