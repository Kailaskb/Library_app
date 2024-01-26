
from django.contrib import auth
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import (BookCategoryModel, BookModel, LibrarianModel,
                         LibrarystaffProfileModel, PublisherModel, User)
from root.utils import fail, slug_generate, success

from .permissions import IsAdmin, IsLibrarian
from .serializers import (AdminLoginModelSerializer, AdminLoginSerializer,
                          BookCategoryModelSerializer, BookCategorySerializer,
                          BookModelSerializer, BookSerializer,
                          LibrarystaffProfileModelSerializer,
                          LibrarystaffProfileSerializer, LoginSerializer,
                          PublisherModelSerializer, PublisherSerializer,
                          SignupSerializer, UserObjectSerializer)

# Create your views here.


class SignupAPI(APIView):
    def post(self, request):
        try:
            serializer = SignupSerializer(data=request.data)
            if serializer.is_valid():
                first_name = serializer.validated_data['first_name']
                last_name = serializer.validated_data['last_name']
                email = serializer.validated_data['email']
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password,
                    is_admin=False,
                    is_librarian=True,
                    is_library_staff=False,
                    is_active=True,
                )
                librarian = LibrarianModel.objects.create(
                    user=user,
                    gender=serializer.validated_data['gender'],
                    dob=serializer.validated_data['dob'],
                    profile_image=serializer.validated_data['profile_image'],
                    slug=slug_generate('librarian')
                )

                data = UserObjectSerializer(librarian, many=False).data
                return Response(success(data), status=201)
            return Response(fail(serializer.errors), status=400)
        except Exception as e:
            return Response(fail(str(e)), status=500)


class LoginAPI(APIView):
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(fail(serializer.errors), status=400)
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = auth.authenticate(
                username=username,
                password=password
            )
            if user is not None:
                token = Token.objects.filter(user=user)
                user = LibrarianModel.objects.get(user=user)
                data = UserObjectSerializer(user, many=False)
                data = success(data.data)
                if token.exists():
                    data['token'] = token.first().key
                    return Response(success(data), status=200)
                token = Token.objects.create(user=user.user)
                data['token'] = token.key
                return Response(success(data), status=200)
            return Response(fail("invalid password"), status=401)
        except Exception as e:
            return Response(fail(str(e)), status=500)


class AdminLoginAPI(APIView):
    def post(self, request):
        try:
            serializer = AdminLoginSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(fail(serializer.errors), status=400)
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = auth.authenticate(
                username=username,
                password=password
            )
            if user is not None:
                token = Token.objects.filter(user=user)
                data = AdminLoginModelSerializer(user, many=False)
                data = success(data.data)
                if token.exists():
                    data['token'] = token.first().key
                    return Response(success(data), status=200)
                token = Token.objects.create(user=user)
                data['token'] = token.key
                return Response(success(data), status=200)
            return Response(fail("invalid password"), status=401)
        except Exception as e:
            return Response(fail(str(e)), status=500)


class LibrarystaffProfileViewSet(viewsets.ViewSet):

    permission_classes = (IsLibrarian | IsAdmin,)

    def create(self, request):
        try:
            serializer = LibrarystaffProfileSerializer(
                data=request.data, context={'user': request})

            if serializer.is_valid():
                first_name = serializer.validated_data['first_name']
                last_name = serializer.validated_data['last_name']
                email = serializer.validated_data['email']
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']

                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password,
                    is_admin=False,
                    is_librarian=False,
                    is_library_staff=True,
                    is_active=True,
                )
                user.save()

                obj = LibrarystaffProfileModel.objects.create(
                    user=user,
                    gender=serializer.validated_data['gender'],
                    dob=serializer.validated_data['dob'],
                    staff_profile_image=serializer.validated_data['staff_profile_image'],
                    slug=slug_generate('librarystaff'),
                    # use .first()-[to filter data from request]
                )
                if user.is_admin:
                    obj.senior_staff = serializer.validated_data['senior_staff']
                else:
                    obj.senior_staff = LibrarianModel.objects.filter(
                        user=request.user).first()
                obj.save()
                data = LibrarystaffProfileModelSerializer(obj, many=False,)
                return Response(success(data.data), status=201)
            return Response(fail(serializer.errors), status=400)
        except Exception as e:
            return Response(fail(str(e)), status=500)

    def list(self, request):
        try:
            obj = LibrarystaffProfileModel.objects.all()
            if obj.exists():
                serializer = LibrarystaffProfileModelSerializer(obj, many=True)
                return Response(success(serializer.data), status=200)
            return Response(fail(serializer.errors), status=400)
        except Exception as e:
            return Response(fail(str(e)), status=500)

    def retrieve(self, request, pk=None):
        try:
            obj = LibrarystaffProfileModel.objects.filter(slug=pk)
            if obj.exists():
                user = get_object_or_404(obj)
                serializer = LibrarystaffProfileModelSerializer(user)
                return Response(success(serializer.data), status=200)
            return Response(fail(serializer.errors), status=400)
        except Exception as e:
            return Response(fail(str(e)), status=500)

    def update(self, request, pk):
        try:
            obj = LibrarystaffProfileModel.objects.filter(slug=pk)
            serializer = LibrarystaffProfileModelSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(fail(serializer.errors), status=400)
            obj.update(
                gender=serializer.validated_data['gender'],
                dob=serializer.validated_data['dob'],
                staff_profile_image=serializer.validated_data['staff_profile_image']
            )
            data = LibrarystaffProfileModelSerializer(obj.first(), many=False)
            return Response(success(data.data), status=201)
        except Exception as e:
            return Response(fail(str(e)), status=500)

    def destroy(self, request, pk):
        try:
            obj = LibrarystaffProfileModel.objects.filter(slug=pk)
            if obj.exists():
                obj.delete()
                return Response(success('Staff profile deleted'), status=204)
            return Response(fail('Staff profile does not exists'), status=400)
        except Exception as e:
            return Response(fail(str(e)), status=500)


class BookCategoryViewSet(viewsets.ViewSet):
    permission_classes = (IsLibrarian | IsAdmin,)

    def create(self, request):
        try:
            serializer = BookCategorySerializer(data=request.data)
            if serializer.is_valid():
                user = BookCategoryModel.objects.create(
                    slug=slug_generate('bookcategory'),
                    manager=serializer.validated_data['manager'],
                    librarian=serializer.validated_data['librarian'],
                    label=serializer.validated_data['label'],
                    description=serializer.validated_data['description']
                )
                data = BookCategoryModelSerializer(user, many=False)
                return Response(success(data.data), status=201)
            return Response(fail(serializer.errors), status=400)
        except Exception as e:
            return Response(success(str(e)), status=500)

    def list(self, request):
        try:
            obj = BookCategoryModel.objects.all()
            if obj.exists():
                serializer = BookCategoryModelSerializer(obj, many=True)
                return Response(success(serializer.data), status=200)
            return Response(success(serializer.errors), status=400)
        except Exception as e:
            return Response(fail(str(e)), status=500)

    def retrieve(self, request, pk):
        try:
            obj = BookCategoryModel.objects.filter(slug=pk)
            if obj.exists():
                user = get_object_or_404(obj)
                serializer = BookCategoryModelSerializer(user)
                return Response(success(serializer.data), status=200)
            return Response(fail(serializer.errors), status=400)
        except Exception as e:
            return Response(fail(str(e)), status=500)

    def update(self, request, pk):
        try:
            obj = BookCategoryModel.objects.filter(slug=pk)
            serializer = BookCategorySerializer(data=request.data)
            if not serializer.is_valid():
                return Response(fail(serializer.errors), status=400)
            if not obj.exists():
                return Response(fail('object does not exists'))
            obj.update(
                manager=serializer.validated_data['manager'],
                librarian=serializer.validated_data['librarian'],
                label=serializer.validated_data['label'],
                description=serializer.validated_data['description']
            )
            data = BookCategoryModelSerializer(obj.first(), many=False)
            return Response(success(data.data), status=200)
        except Exception as e:
            return Response(fail(str(e)), status=500)

    def destroy(serlf, request, pk):
        try:
            obj = BookCategoryModel.objects.filter(slug=pk)
            if obj.exists():
                obj.delete()
                return Response(success('Book category deleted'), status=204)
            return Response(fail('Book category does not exists'), status=400)
        except Exception as e:
            return Response(fail(str(e)), status=500)


class PublisherViewSet(viewsets.ViewSet):
    permission_classes = (IsLibrarian | IsAdmin,)

    def create(self, request):
        try:
            serializer = PublisherSerializer(data=request.data)
            if serializer.is_valid():
                user = PublisherModel.objects.create(
                    slug=slug_generate('publisher'),
                    label=serializer.validated_data['label'],
                    description=serializer.validated_data['description']
                )
                data = PublisherModelSerializer(user, many=False)
                return Response(success(data.data), status=201)
            return Response(fail(serializer.errors), status=400)
        except Exception as e:
            return Response(fail(str(e)), status=500)

    def list(self, request):
        try:
            obj = PublisherModel.objects.all()
            if obj.exists():
                serializer = PublisherModelSerializer(obj, many=True)
                return Response(success(serializer.data), status=200)
            return Response(fail(serializer.errors), status=400)
        except Exception as e:
            return Response(fail(str(e)), status=500)

    def retrieve(self, request, pk):
        try:
            obj = PublisherModel.objects.filter(slug=pk)
            if obj.exists():
                user = get_object_or_404(obj)
                serializer = PublisherModelSerializer(user)
                return Response(success(serializer.data), status=200)
            return Response(fail(serializer.errors), status=400)
        except Exception as e:
            return Response(fail(str(e)), status=500)

    def update(self, request, pk):
        try:
            obj = PublisherModel.objects.filter(slug=pk)
            serializer = PublisherSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(fail(serializer.errors), status=400)
            if not obj.exists():
                return Response(fail('object does not exists'), status=400)
            obj.update(
                label=serializer.validated_data['label'],
                description=serializer.validated_data['description']
            )
            data = PublisherModelSerializer(obj.first(), many=False)
            return Response(success(data.data), status=200)
        except Exception as e:
            return Response(fail(str(e)), status=500)

    def destroy(self, request, pk):
        try:
            obj = PublisherModel.objects.filter(slug=pk)
            if obj.exists():
                obj.delete()
                return Response(success('Deleted'), status=204)
            return Response(fail('object does not exists'), status=400)
        except Exception as e:
            return Response(fail(str(e)), status=500)


class BookViewset(viewsets.ViewSet):
    permission_classes = (IsLibrarian | IsAdmin,)

    def create(self, request):
        try:
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                book = BookModel.objects.create(
                    slug=slug_generate('books'),
                    label=serializer.validated_data['label'],
                    description=serializer.validated_data['description'],
                    publisher=serializer.validated_data['publisher'],
                )
                data = BookModelSerializer(book)
                return Response(success(data.data), status=201)
            return Response(fail(serializer.errors), status=400)
        except Exception as e:
            return Response(fail(str(e)), status=500)

    def save(self):
        user = BookCategoryModel.objects.create(
            manager=self.validated_data['manager'],
            librarian=self.validated_data['librabrian'],
            label=self.validated_data['label'],
            description=self.validated_data['description']
        )
        user.save()
        obj = BookModel.objects.create(
            label=self.validated_data['label'],
            description=self.validated_data['description'],
            publisher=self.validated['publisher'],
        )
        obj.save()
        obj.category.add(user)
        obj.save()

    def list(self, request):
        try:
            obj = BookModel.objects.all()
            if obj.exists():
                serializer = BookModelSerializer(obj, many=True)
                return Response(success(serializer.data), status=200)
            return Response(fail(serializer.errors), status=400)
        except Exception as e:
            return Response(fail(str(e)), status=500)

    def retrieve(self, request, pk):
        try:
            obj = BookModel.objects.filter(slug=pk)
            if obj.exists():
                user = get_object_or_404(obj)
                serializer = BookModelSerializer(user)
                return Response(success(serializer.data), status=200)
            return Response(fail(serializer.errors), status=400)
        except Exception as e:
            return Response(fail(str(e)), status=500)

    def update(self, request, pk):
        try:
            obj = BookModel.objects.filter(slug=pk)
            serializer = BookSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(fail(serializer.errors), status=400)
            if not obj.exists():
                return Response(fail('object does not exists'), status=400)
            obj.update(
                label=serializer.validated_data['label'],
                description=serializer.validated_data['description'],
                publisher=serializer.validated_data['publisher'],

            )
            data = BookModelSerializer(obj.first(), many=False)
            return Response(success(data.data), status=200)
        except Exception as e:
            return Response(fail(str(e)), status=500)

    def destroy(self, request, pk):
        try:
            obj = BookModel.objects.filter(slug=pk)
            if obj.exists():
                obj.delete()
                return Response(success('Deleted'), status=204)
            return Response(fail('Object does not exists'), status=400)
        except Exception as e:
            return Response(fail(str(e)), status=500)
