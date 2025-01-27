from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import UserProfile


user = settings.AUTH_USER_MODEL


@receiver(post_save, sender=user)
def create_user_profile(sender, instance, created, **kwargs):
    
    if created:
        UserProfile.objects.create(user=instance)
        
# @receiver(post_save, sender=UserProfile)       
# def profileUpdated(sender, instance, created, **kwargs):
#     profile = instance
#     if created == False:
#         profile.save()
    


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()
    
    
post_delete.connect(deleteUser, sender=UserProfile)