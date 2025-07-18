from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Exam
from .serializers import ExamSerializer

class ExamPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all().order_by('-created_at')
    serializer_class = ExamSerializer
    pagination_class = ExamPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'year', 'subject', 'is_premium']
    search_fields = ['title', 'subject', 'type']
    ordering_fields = ['year', 'created_at']
