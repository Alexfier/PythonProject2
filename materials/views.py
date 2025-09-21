from django.shortcuts import get_object_or_404
# from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Courses, Lessons, Subscription
from .paginators import PageSizePaginator
from .permissions import IsOwnerPermission, ModersPermission
from .serializers import CoursesModelSerializer, LessonsModelSerializer
from .tasks import send_mail_after_course_update


class CoursesViewSet(viewsets.ModelViewSet):
    serializer_class = CoursesModelSerializer
    queryset = Courses.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = PageSizePaginator

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        send_mail_after_course_update.delay()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~ModersPermission,)
        elif self.action == "list":
            self.permission_classes = (ModersPermission | IsOwnerPermission,)
        elif self.action in ("retrieve", "update"):
            self.permission_classes = (ModersPermission | IsOwnerPermission,)
        elif self.action == "destroy":
            self.permission_classes = (~ModersPermission | IsOwnerPermission,)
        return super().get_permissions()


class LessonsCreateAPIView(CreateAPIView):
    serializer_class = LessonsModelSerializer
    queryset = Lessons.objects.all()
    permission_classes = [IsAuthenticated, ~ModersPermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonsUpdateAPIView(UpdateAPIView):
    serializer_class = LessonsModelSerializer
    queryset = Lessons.objects.all()
    permission_classes = [IsAuthenticated, ModersPermission | IsOwnerPermission]


class LessonsDestroyAPIView(DestroyAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsModelSerializer
    permission_classes = [IsAuthenticated, IsOwnerPermission | ~ModersPermission]


class LessonsRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonsModelSerializer
    queryset = Lessons.objects.all()
    permission_classes = [IsAuthenticated, ModersPermission | IsOwnerPermission]


class LessonsListAPIView(ListAPIView):
    serializer_class = LessonsModelSerializer
    queryset = Lessons.objects.all()
    permission_classes = [IsAuthenticated, ModersPermission | IsOwnerPermission]
    pagination_class = PageSizePaginator

    def get_queryset(self):
        if ModersPermission().has_permission(self.request, self):
            return Lessons.objects.all()
        else:
            return Lessons.objects.filter(owner=self.request.user)


class SubscriptionAPIView(APIView):
    @swagger_auto_schema(
        operation_description='При добавлении подписки возвращает {"message":"подписка добавлена"}, '
        'при отмене подписки возвращает {"message":"подписка удалена"}'
    )
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Courses, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "подписка добавлена"
        return Response({"message": message})
