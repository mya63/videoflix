from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Video


@receiver(post_save, sender=Video)
def video_created(sender, instance, created, **kwargs):
    if created:
        print("Neues Video:", instance.id)


@receiver(post_delete, sender=Video)
def video_deleted(sender, instance, **kwargs):
    print("Video gelöscht:", instance.id)