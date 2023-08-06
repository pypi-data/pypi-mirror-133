from django.utils.translation import ngettext

from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pragmatic.serializers import ContentTypeSerializer
from whistle.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    description = serializers.CharField()
    short_description = serializers.CharField()
    object_content_type = ContentTypeSerializer(read_only=True)
    target_content_type = ContentTypeSerializer(read_only=True)

    class Meta:
        model = Notification
        exclude = []


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return super().get_queryset()\
            .for_recipient(self.request.user) \
            .select_related(
                'object_content_type',
                'target_content_type',
                'recipient',
                'actor'
            )


class MarkNotificationsAsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    operations = ['apply', 'ignore']

    def patch(self, request):
        notification_id = request.GET.get('notification_id', None)
        unread_notifications = request.user.notifications.unread()

        if notification_id:
            unread_notifications = unread_notifications.filter(id=notification_id)

        num_notifications = unread_notifications.count()
        unread_notifications.mark_as_read()
        request.user.clear_unread_notifications_cache()

        return Response(status=200, data=ngettext(
            '%(count)d notification marked as read',
            '%(count)d notifications marked as read',
            num_notifications,
        ) % {'count': num_notifications})
