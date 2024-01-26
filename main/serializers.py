from rest_framework import serializers

from main import permissions

from .models import (BookCategoryModel, BookModel, LibrarianModel,
                     LibrarystaffProfileModel, PublisherModel, User)


class SignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    gender = serializers.CharField(max_length=10)
    dob = serializers.DateField()
    profile_image = serializers.ImageField(allow_null=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('email is already in use')
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username is already in use")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                'password should at least have 8 characters')
        return value


class AdminLoginModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserObjectSerializer(serializers.ModelSerializer):
    user = AdminLoginModelSerializer()

    class Meta:
        model = LibrarianModel
        fields = ['user', 'dob', 'gender', 'profile_image', 'slug']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            return value
        raise serializers.ValidationError('Username does not exists')


class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            return value
        raise serializers.ValidationError('Username does not exists')


class LibrarystaffProfileSerializer(serializers.Serializer):

    staff_profile_image = serializers.ImageField(allow_null=True)
    dob = serializers.DateField()
    gender = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    senior_staff = serializers.IntegerField(allow_null=True)

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                'password should at least have 8 characters')
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username is already in use")
        return value

    def validate_user(self, value):

        user = User.objects.filter(id=value)
        if user.exists():
            return user.first()
        raise serializers.ValidationError('invalid user id')

    def validate_senior_staff(self, value):
        user = self.context.get("user").user
        if user.is_admin:
            senior_staff = User.objects.filter(id=value)
            if senior_staff.exists():
                return senior_staff.first()
            raise serializers.ValidationError('invalid senior staff id')


class LibrarystaffProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibrarystaffProfileModel
        fields = '__all__'


class BookCategorySerializer(serializers.Serializer):
    manager = serializers.IntegerField()
    librarian = serializers.IntegerField()
    label = serializers.CharField()
    description = serializers.CharField()

    def validate_manager(self, value):
        user = LibrarystaffProfileModel.objects.filter(id=value)
        if user.exists():
            return user.first()
        raise serializers.ValidationError('invalid user id')

    def validate_librarian(self, value):
        user = LibrarianModel.objects.filter(id=value)
        if user.exists():
            return user.first()
        raise serializers.ValidationError('no librarian exists')


class BookCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategoryModel
        fields = '__all__'


class PublisherSerializer(serializers.Serializer):
    label = serializers.CharField()
    description = serializers.CharField()


class PublisherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublisherModel
        fields = '__all__'


class BookSerializer(serializers.Serializer):
    label = serializers.CharField()
    description = serializers.CharField()
    publisher = serializers.IntegerField()
    category = serializers.IntegerField()

    def validate_publisher(self, value):
        user = PublisherModel.objects.filter(id=value)
        if user.exists():
            return user.first()
        raise serializers.ValidationError('No publisher exists')

    def validated_category(self, value):
        user = BookCategoryModel.objects.filter(id=value)
        if user.exists():
            return user.first()
        raise serializers.ValidationError('No book category exists')


class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel
        fields = '__all__'
