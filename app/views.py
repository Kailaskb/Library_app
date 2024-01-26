from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from main.permissions import IsLibrarian
from root.utils import fail, success

from .models import BookHolder
from .serializers import BookHolderSerializer

# Create your views here.


class BookHolderViewSet(ModelViewSet):
    permission_classes = (IsLibrarian,)
    queryset = BookHolder.objects.all()
    serializer_class = BookHolderSerializer
    filter_fields = '__all__'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(success(serializer.data), status=201, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(success(serializer.data), status=200)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(success(serializer.data), status=200)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(success(serializer.data), status=200)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(success("deleted"), status=204)