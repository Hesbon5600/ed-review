from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, mixins, permissions

from rest_framework.decorators import detail_route
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import BrowsableAPIRenderer
# from rest_framework.views import APIView, CreateAPIView

from . import serializers
from . import models
from .permissions import isSuperUser
from .renderers import UserJSONRenderer


class SignupAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    renderer_classes = (UserJSONRenderer, BrowsableAPIRenderer,)
    serializer_class = serializers.RegistrationSerializer


class LoginAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.LoginSerializer
    # renderer_classes = (UserJSONRenderer,)
    renderer_classes = (UserJSONRenderer, BrowsableAPIRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer, BrowsableAPIRenderer,)
    serializer_class = serializers.UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


# class RegistrationAPIView(APIView):
#     # Allow any user (authenticated or not) to hit this endpoint.
#     permission_classes = (AllowAny,)
#     # renderer_classes = (UserJSONRenderer,)
#     serializer_class = serializers.RegistrationSerializer

#     def post(self, request):
#         user = {**request.data}
#         print(us)
#         # The create serializer, validate serializer, save serializer pattern
#         # below is common and you will see it a lot throughout this course and
#         # your own work later on. Get familiar with it.
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class LoginAPIView(APIView):
#     permission_classes = (AllowAny,)
#     renderer_classes = (UserJSONRenderer,)
#     serializer_class = LoginSerializer

#     def post(self, request):
#         user = request.data.get('user', {})

#         # Notice here that we do not call `serializer.save()` like we did for
#         # the registration endpoint. This is because we don't actually have
#         # anything to save. Instead, the `validate` method on our serializer
#         # handles everything we need.
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)


class ListCreateCourse(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer


class RetrieveUpdateDestroyCourse(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer


class ListCreateReview(generics.ListCreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    # Gets multiple items
    def get_queryset(self):
        return self.queryset.filter(course_id=self.kwargs.get('course_pk'))

    def perform_create(self, serializer):
        course = get_object_or_404(models.Course,
                                   pk=self.kwargs.get('course_pk'))
        serializer.save(course=course)


class RetrieveUpdateDestroyReview(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    # Get a single item
    def get_object(self):
        return get_object_or_404(self.get_queryset(),
                                 course_id=self.kwargs.get('course_pk'),
                                 pk=self.kwargs.get('pk'))


class CourseViewset(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    # custom permission class
    permission_classes = (
        isSuperUser,
        permissions.DjangoModelPermissions,)

    @detail_route(methods=['get'])
    def reviews(self, request, pk=None):
        # Custom pagination
        self.pagination_class.page_size = 1
        reviews = models.Review.objects.filter(course_id=pk)

        page = self.paginate_queryset(reviews)

        if page is not None:
            serializer = serializers.ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # course = self.get_object()
        serializer = serializers.ReviewSerializer(
            reviews, many=True
        )
        return Response(serializer.data)

# class ReviewViewset(viewsets.ModelViewSet):
#     queryset = models.Review.objects.all()
#     serializer_class = serializers.ReviewSerializer


# OR

class ReviewViewset(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet
                    ):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer


# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response


# class ListCreateCourse(APIView):
#     def get(self, request, format=None):
#         courses = models.Course.objects.all()
#         serializer = serializers.CourseSerializer(courses, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = serializers.CourseSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
