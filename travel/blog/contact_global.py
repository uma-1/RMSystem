from .models import Contact, Destination_Category, Destination, NewsletterUser
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import NewsletterSignUpForm
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect


def contact_details(request):
    content = {
        'contactData': Contact.objects.filter(status=1),
    }
    return content


def destination_category(request):
    data = {
        'destinationCategory': Destination_Category.objects.prefetch_related('destination_set').all()
    }
    return data


def descat_details(request, criteria):
    cat_list = Destination_Category.objects.prefetch_related('destination_set').filter(slug=criteria)
    page = request.GET.get('page', 1)
    paginator = Paginator(cat_list, 10)
    try:
        categoryData = paginator.page(page)
    except PageNotAnInteger:
        categoryData = paginator.page(1)
    except EmptyPage:
        categoryData = paginator.page(paginator.num_pages)

    data = {
        'title': "Category",
        'destinationCategory': categoryData

    }
    return render(request, 'pages/destination/destination_category_details.html', data)


def newsletter_signup(request):
    form = NewsletterSignUpForm(request.POST or None)
    back = request.META.get('HTTP_REFERER')
    if form.is_valid():
        if request.method == 'POST' and 'subscribe' in request.POST:
            instance = form.save(commit=False)
            if NewsletterUser.objects.filter(email=instance.email).exists():
                messages.warning(request, instance.email+ ' already exist. Please enter new email address',
                                 "alert alert-warning alert-dismissible")
                form = NewsletterSignUpForm()
            else:
                instance.save()
                messages.success(request, "Successfully Subscribed. You will receive email from Teenkanya at "+ instance.email, "alert alert-success alert-dismissible")
                text_content = render_to_string('pages/newsletters/sign_up_email.txt')
                html_content = render_to_string('pages/newsletters/sign_up_email.html')
                email = EmailMultiAlternatives("Newsletter Subscription", text_content)
                email.attach_alternative(html_content, "text/html")
                email.to = [instance.email]
                email.send()
                form = NewsletterSignUpForm()

        elif request.method == 'POST' and 'unsubscribe' in request.POST:
            instance = form.save(commit=False)
            if NewsletterUser.objects.filter(email=instance.email).exists():
                NewsletterUser.objects.filter(email=instance.email).delete()
                messages.success(request,
                                 "Successfully unsubscribed. You will no longer get email from Teenkanya",
                                 "alert alert-warning alert-dismissible")
                text_content = render_to_string('pages/newsletters/unsubscribe_email.txt')
                html_content = render_to_string('pages/newsletters/unsubscribe_email.html')
                email = EmailMultiAlternatives("Newsletter Unsubscription", text_content)
                email.attach_alternative(html_content, "text/html")
                email.to = [instance.email]
                email.send()
                form = NewsletterSignUpForm()
            else:
                messages.error(request, instance.email+ " has not subscribed for Newsletter" ,
                               "alert alert-warning alert-dismissible")
                form = NewsletterSignUpForm()

    context = {
        'form': form
    }
    return context
