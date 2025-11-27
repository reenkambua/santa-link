from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
import os


class User(AbstractUser):
    pass



class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_groups")
    members = models.ManyToManyField(User, related_name="member_groups")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Pair(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="pairs")
    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="giving")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiving")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
        send_mail(
            subject=f"🎅 Your Secret Santa Recipient for {self.group.name}",
            message=f"Hi {self.giver.username}, your recipient is {self.receiver.username}!Have fun and enjoy the gifting. Cant wait to share the gifts.",
            from_email=os.getenv("EMAIL_HOST_USER"),
            recipient_list=[self.giver.email],
            fail_silently=True
        )

    def __str__(self):
        return f"{self.giver} -> {self.receiver}"



class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="wishlists")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}: {self.name}"



class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"
