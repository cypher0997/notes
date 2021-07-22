from django.db import models
from uer_register_login.models import CustomUser


class Label(models.Model):
    label_name = models.CharField(max_length=200)


class NewNotes(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    discription = models.CharField(max_length=500)
    label = models.ManyToManyField(Label)

    @property
    def is_notes_instance(self):
        """
        method used specifically for testing purpose
        :return:
        """
        return self.id > 0



