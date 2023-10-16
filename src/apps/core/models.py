from django.db import models


class GenericModel(models.Model):
    """Model definition for GenericModel."""

    created_at = models.DateField(auto_now=False, auto_now_add=True)
    modified_at = models.DateField(auto_now=True, auto_now_add=False)
    deleted_at = models.DateField(auto_now=True, auto_now_add=False)

    class Meta:
        """Meta definition for GenericModel."""

        abstract = True
