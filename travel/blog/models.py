from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import send_mail
import os
from email.mime.image import MIMEImage
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validator import validate_file_size


class Banner(models.Model):
    status = models.BooleanField(default=0, help_text='Tick to show this on website')
    title = models.CharField(max_length=255, unique=True)
    heading1 = models.CharField(max_length=255, unique=True)
    heading2 = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="banner", help_text="Size of Image must be 1200*600")
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Home Page Banner'

    def __str__(self):
        return self.title


class About(models.Model):
    status = models.BooleanField(default=0, help_text='Tick to show this on website')
    name = models.CharField(max_length=255, unique=True)
    post = models.CharField(max_length=255)
    image = models.ImageField(upload_to="our team", help_text="Size of Image must be 400*400")
    choosedescription = models.TextField(max_length=1000)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'About Page'

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    status = models.BooleanField(default=0, help_text='Tick to show this on website')
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="Testimonial", help_text="Size of Image must be 400*400")
    description = models.TextField()
    profession = models.CharField(max_length=255, blank=True)
    facebook = models.URLField()
    instagram = models.URLField()
    twitter = models.URLField()

    class Meta:
        verbose_name_plural = 'Customer Testimonial'

    def __str__(self):
        return self.name


class Contact(models.Model):
    status = models.BooleanField(default=0)
    slogan = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to="logo", help_text="Size of Image must be 219*55")
    location = models.CharField(max_length=255, unique=True)
    contact = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    facebook = models.URLField()
    instagram = models.URLField()
    twitter = models.URLField()
    youtube = models.URLField()
    google = models.URLField()
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return self.slogan


class Destination_Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    status = models.BooleanField()
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Destination Category'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('descat-details',
                       args=[self.slug])


class Destination(models.Model):
    status = models.BooleanField(default=0, help_text='Tick to show this on website')
    title = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    star = models.IntegerField(default=0)
    popular = models.BooleanField(default=0)
    category = models.ForeignKey(Destination_Category, on_delete=models.CASCADE)
    day = models.IntegerField(default=0)
    image = models.ImageField(upload_to="destination", help_text="Size of Image must be 500*333")
    image1 = models.ImageField(upload_to="destination", help_text="Size of Image must be 500*333")
    image2 = models.ImageField(upload_to="destination", help_text="Size of Image must be 500*333")
    image3 = models.ImageField(upload_to="destination", help_text="Size of Image must be 500*333")
    image4 = models.ImageField(upload_to="destination", help_text="Size of Image must be 500*333")
    price = models.CharField(max_length=255, help_text="Please Mention Currency")
    description = models.CharField(max_length=300)
    language = models.CharField(max_length=300)
    include = RichTextField()
    exclude = RichTextField()
    itenary = RichTextField()
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Destination Package'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('destination-details',
                       args=[self.slug])


class Destination_Booking(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    contact = models.IntegerField()
    depature = models.CharField(max_length=255)
    person = models.IntegerField()
    message = models.TextField()
    destination_name = models.CharField(max_length=255)
    status = (
        ('Waiting', 'Waiting'),
        ('Contacted', 'Contacted'),
        ('Done', 'Done')
    )
    status = models.CharField(max_length=255, choices=status, default="Waiting")
    handled_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    booking_confirm = (
        ('confirm', 'confirm'),
        ('cancel', 'cancel'),
        ('waiting', 'waiting')
    )
    booking = models.CharField(max_length=255, choices=booking_confirm, default="waiting")
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Destination Customer Booking'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('bookinglist')

    def save(self, *args, **kwargs):
        from_email = settings.EMAIL_HOST_USER
        if self.booking == "confirm":
            send_mail("Booking has been confirmed",
                      "Thank You for booking " + self.destination_name + ". Teenkanya Travel", from_email,
                      [self.email], fail_silently=False)
        elif self.booking == "cancel":
            send_mail("Booking has been canceled",
                      "Booking for " + self.destination_name + " has been canceled. Thanks for the query", from_email,
                      [self.email], fail_silently=False)

        super(Destination_Booking, self).save(*args, **kwargs)


class BlogData(models.Model):
    status = models.BooleanField(default=0, help_text='Tick to show this on website')
    created = models.DateField(null=True)
    star = models.IntegerField(default=0)
    latest = models.BooleanField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="blimage", help_text="Size of Image must be 400*400")
    description = RichTextUploadingField()
    page_visit = models.IntegerField(default=0)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Blog'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogz-details',
                       args=[self.slug])


class PopUp(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="Message From")
    status = models.BooleanField(default=0)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Home Page Pop Up'

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    status = models.BooleanField(default=0, help_text='Tick to show this on website')
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    level = models.CharField(max_length=255, choices=[('Low Level', 'Low Level'), ('Mid Level', 'Mid Level'),
                                                      ('High Level', 'High Level')])
    vacancynum = models.IntegerField()
    type = models.CharField(max_length=255, choices=[('Full Time', 'Full Time'), ('Part Time', 'Part Time'),
                                                     ('Contract', 'Contract')])
    location = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    lastdate = models.DateTimeField()
    educationlevel = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    job_specification = RichTextField()
    job_description = RichTextField()
    apply_procedure = models.CharField(max_length=500)
    notes = models.CharField(max_length=500)
    page_visit = models.IntegerField(default=0)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Vacancy Post'

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('vacancy-details',
                       args=[self.slug])


class ApplicantData(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    contact = models.IntegerField()
    photo = models.ImageField(upload_to='applicant_image', validators=[validate_file_size])
    cv = models.FileField(upload_to='application_cv')
    position = models.CharField(max_length=255)
    applied_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Vacanacy Application List'

    def __str__(self):
        return self.name


class NewsletterUser(models.Model):
    email = models.EmailField()
    date_added = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Newsletter Subscribed User'

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    Email_Status_Choices = (
        ('Draft', 'Draft'),
        ('Published', 'Published')
    )
    subject = models.CharField(max_length=255)
    body = RichTextUploadingField()
    email = models.ManyToManyField(NewsletterUser)
    image = models.ImageField(upload_to='Newsletterimage', blank=True, null=True)
    status = models.CharField(max_length=255, choices=Email_Status_Choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Newsletter Creation'

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        super(Newsletter, self).save(*args, **kwargs)
        if self.status == "Published":
            for email_list in self.email.all():
                self.name = self.posted_by.first_name + " " + self.posted_by.last_name
                content = {'body': self.body, 'user': self.name}
                text_content = render_to_string('pages/newsletters/newsletter_email_to_user.txt', content)
                html_content = render_to_string('pages/newsletters/newsletter_email_to_user.html', content)
                email = EmailMultiAlternatives(self.subject, text_content)
                email.attach_alternative(html_content, "text/html")
                email.mixed_subtype = 'related'
                email.attach(self.image.name, self.image.read())
                email.to = [email_list]
                for f in ['static/frontend/images/logo.png']:
                    fp = open(os.path.join(os.path.dirname(__file__), f), 'rb')
                    msg_img = MIMEImage(fp.read())
                    fp.close()
                    msg_img.add_header('Content-ID', '<{}>'.format(f))
                    email.attach(msg_img)
                email.send()


# Admin Personal Information Save
class Admin_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True)
    contact = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='Admin/Admin_Photo', blank=True, null=True)
    citizenship = models.FileField(upload_to='Admin/Admin_Citizenship', blank=True, null=True)
    slc_certificate = models.FileField(upload_to='Admin/Admin_SLC', blank=True, null=True)
    plus2_certificate = models.FileField(upload_to='Admin/Admin_Plus2', blank=True, null=True)
    bachelor_certificate = models.FileField(upload_to='Admin/Admin_Bachelor', blank=True, null=True)
    master_certificate = models.FileField(upload_to='Admin/Admin_Master', blank=True, null=True)
    birthdate = models.DateField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Admin_Profile.objects.create(user=instance)
        instance.admin_profile.save()


class Customer_Records(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, default="")
    contact = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='Customer_Record/Customer_Photo', blank=True, null=True)
    citizenship = models.FileField(upload_to='Customer_Record/Customer_Citizenship', blank=True, null=True)
    passport = models.FileField(upload_to='Customer_Record/Customer_Passport', blank=True, null=True)
    birthdate = models.DateField(null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Customer Record'
