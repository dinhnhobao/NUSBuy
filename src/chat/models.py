from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Contact(models.Model): #represent a User by (user, their friends)
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    contact = models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE, default = '')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.username


class Chat(models.Model):
    participants = models.ManyToManyField(Contact, related_name='chats', blank = True)
    '''
    ForeignKey.related_name:    
    The name to use for the relation from the related object back to this one.
    Contact ---chats ---> participants
    Contact.chats.all() ---> get all participants in the Chat.
    '''
    messages = models.ManyToManyField(Message, blank=True)
    
    def __str__(self):
        return "{}".format(self.pk)