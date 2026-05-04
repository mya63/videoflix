import django_rq
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Video
from .tasks import process_video


@receiver(post_save, sender=Video)
def video_created(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue("default")
        queue.enqueue(process_video, instance.id)


@receiver(post_delete, sender=Video)
def video_deleted(sender, instance, **kwargs):
    print("Video gelöscht:", instance.id)