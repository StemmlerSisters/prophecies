from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from prophecies.core.models import Project, Task, UserNotification
from prophecies.core.contrib.mentions import list_mentions, get_or_create_mention_action, mentioned, notify_mentioned_users

class Tip(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tip name", null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def mentions(self):
        """
        Returns a list of unique mentions, with their corresponding User.
        """
        return list_mentions(self.description)


    @property
    def mentioned_project(self):
        if mentioned(self.description, 'project'):
            try:
                return self.project
            except AttributeError:
                return None


    @property
    def mentioned_task(self):
        if mentioned(self.description, 'task'):
            try:
                return self.task
            except AttributeError:
                return None


    @staticmethod
    def signal_notify_mentioned_users(sender, instance, **kwargs):
        for mention in instance.mentions:
            user = mention.get('user')
            if user is not None:
                action, created = get_or_create_mention_action(instance.creator, user, instance)
                if created:
                    UserNotification.objects.create(recipient=user, action=action)


    @staticmethod
    def signal_notify_members_in_mentioned_project(sender, instance, **kwargs):
        project = instance.mentioned_project
        if project is not None:
            notify_mentioned_users(instance.creator, project.members, instance)


    @staticmethod
    def signal_notify_task_checkers_in_mentioned_task(sender, instance, **kwargs):
        task = instance.mentioned_task
        if task is not None:
            notify_mentioned_users(instance.creator, task.checkers.all(), instance)


signals.post_save.connect(Tip.signal_notify_mentioned_users, sender=Tip)
signals.post_save.connect(Tip.signal_notify_members_in_mentioned_project, sender=Tip)
signals.post_save.connect(Tip.signal_notify_task_checkers_in_mentioned_task, sender=Tip)
