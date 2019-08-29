import datetime

from django.db import models
from django.urls import reverse
from shared.models import Sponsor, Contact


# set the year choices for various drop-downs - earliest data is from 2014
YEAR_CHOICES = []
for yr in range(2014, (datetime.datetime.now().year + 2)):
    YEAR_CHOICES.append((yr, str(yr)))


class Filecatlist(models.Model):
    """

    Stores list of categories for proposal file uploads, related to :model:`mou.Fileupload`.

    """

    cat_list = models.CharField(
        max_length=50,
        blank=True
    )

    class Meta:
        verbose_name = 'file category'
        verbose_name_plural = 'file categories'

    def __str__(self):
        return self.cat_list


class Status(models.Model):
    """

    Stores a list of MOU statuses, related to :model:`mou.Mou`

    """
    status = models.CharField(
        max_length=20,
        blank=True
    )

    class Meta:
        verbose_name_plural = 'statuses'

    def __str__(self):
        return self.status


class Mou(models.Model):
    """

    Stores information about PMEL research proposals.

    """
    mou_id = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        verbose_name='MOU ID'
    )
    mou_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='MOU Title'
    )
    investigator_supported = models.ForeignKey(
        Contact,
        help_text='The Principal Investigator on the MOU',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='PI',
        related_name='mou_contact'
    )
    sponsor = models.ForeignKey(
        Sponsor,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    status = models.ForeignKey(
        Status,
        help_text='Current status of the MOU.',
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    effective_date = models.DateField(
        help_text='Date the MOU became effective.',
        verbose_name='Effective',
        blank=True,
        null=True
    )
    expiration_date = models.DateField(
        help_text='Date the MOU will Expire',
        verbose_name='Expires',
        blank=True,
        null=True
    )
    mou_notes = models.TextField(
        blank=True
    )
    slug = models.SlugField(
        help_text='A short label, used in the URLs to obfuscate the primary key - autogenerated == mou_id.',
        unique=True,
        max_length=10,
    )

    class Meta:
        ordering = ['mou_id']

    def __str__(self):
        return str(self.mou_id)

    def get_absolute_url(self):
        return reverse('mou:mou_detail', kwargs={'slug': self.slug})


class Fileupload(models.Model):
    """

    Uploads MOU files to media/documents/mous, related to :model:`mou.Mou`.

    """
    mou_id = models.ForeignKey(
        Mou,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    file_category = models.ForeignKey(
        Filecatlist,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )
    file_upload = models.FileField(
        upload_to='documents\mous'
    )
