from django.db import models
from uer_register_login.models import CustomUser


class Label(models.Model):
    label_name = models.CharField(max_length=200)

    @property
    def is_label_instance(self):
        """
        method used specifically for testing purpose
        :return:
        """
        return self.id > 0


class Notes(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notes_belong")
    title = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=500, null=True)
    label = models.ManyToManyField(Label)
    collaborator = models.ManyToManyField(CustomUser, related_name="collaborator")


    @property
    def is_notes_instance(self):
        """
        method used specifically for testing purpose
        :return:
        """
        return self.id > 0


