from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

from wagtail.core.models import Page
from wagtail.core import fields
from wagtail.admin import edit_handlers as eh
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.api import APIField

from . import blocks

# Create your models here.

USER_MODEL = get_user_model()


class HomePage(RoutablePageMixin, Page):
    template = 'home/home_page.html'

    banner_title = models.CharField(max_length=100, null=True, blank=True)

    banner_subtitle = fields.RichTextField(features=["bold", "italic", "image"], null=True, blank=True)
    banner_image = models.ForeignKey("wagtailimages.Image", on_delete=models.SET_NULL, null=True, blank=True, related_name="image")
    banner_cta = models.ForeignKey("wagtailcore.Page", on_delete=models.SET_NULL, null=True, blank=True, related_name="link")

    staff_card = fields.StreamField([
        ("cards", blocks.CardBlock()),
    ], null=True, blank=True)

    api_fields = [
        banner_title,
        banner_subtitle,
        banner_image,
        banner_cta,
        staff_card
    ]

    content_panels = Page.content_panels + [
        eh.FieldPanel("banner_title"),
        eh.FieldPanel("banner_subtitle"),
        ImageChooserPanel("banner_image"),
        eh.PageChooserPanel("banner_cta"),
        eh.StreamFieldPanel("staff_card"),
    ]

    class Meta:
        verbose_name = "HOME PAGE"
        verbose_name_plural = "HOME PAGES"


#choices
class Person(models.Model):
    user = models.OneToOneField(
        USER_MODEL,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="Person_profile",
    )
    bio = models.TextField(_("bio"))
    birthday = models.DateField(_("Birthday"), auto_now=False, auto_now_add=False)
    deathday = models.DateField(
        _("Deathday"), auto_now=False, auto_now_add=False, blank=True, null=True
    )

    users = models.ManyToManyField(USER_MODEL, blank=True)
    custom_data = JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = "Person"




class Book(models.Model):
    title = models.CharField(_("title"), max_length=100)
    contributors = models.ManyToManyField(
        "datademo.Person",
        verbose_name=_("Contributors"),
        through="datademo.PersonBookRelation",
        related_name="books",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "book"


class PersonBookRelation(models.Model):
    person = models.ForeignKey("datademo.Person", on_delete=models.CASCADE)
    book = models.ForeignKey(
        "datademo.Book", verbose_name=_(""), on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.book.title} {self.person.user.username}"

    class Meta:
        verbose_name = "Personbookrelation"
