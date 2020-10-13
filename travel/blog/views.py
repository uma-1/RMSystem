from django.shortcuts import redirect
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.core.mail import send_mail
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import VacancyForm, UserRegister, DestinationForm, Contact_Form, NewsletterSignUpForm, \
    NewsletterCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as log, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import xlwt
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models import Q
from django.conf import settings
from django.views.generic.edit import UpdateView
from django.utils import timezone
import requests
from dateutil.relativedelta import relativedelta
from django.views.defaults import page_not_found
from django.core.exceptions import ValidationError


class UpdateBookingList(UpdateView):
    model = Destination_Booking
    template_name = "pages/bookinglist/bookinglistedit.html"
    fields = '__all__'


# Create your views here.
def index(request):
    data = {
        'title': "Home",
        'bannerData': Banner.objects.filter(status=1),
        'destinationData': Destination.objects.filter(category="3") &
                           Destination.objects.filter(popular=1) &
                           Destination.objects.filter(status=1),
        'destinationDataNepal': Destination.objects.filter(category="4") &
                                Destination.objects.filter(popular=1) &
                                Destination.objects.filter(status=1),
        'popupdata': PopUp.objects.filter(status=1),
        'testimonialData': Testimonial.objects.filter(status=1),
        'teamData': About.objects.filter(status=1)
    }
    return render(request, 'pages/home/home.view.html', data)


def about(request):
    data = {
        'title': "About us",
        'teamData': About.objects.filter(status=1)
    }
    return render(request, 'pages/about/about.view.html', data)


@csrf_exempt
def contact(request):
    if request.method == 'POST':
        back = request.META.get('HTTP_REFERER')
        form = Contact_Form(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phoneno')
        message = request.POST.get('message')
        subject = "Message From Customer"
        phone1 = str(phone)
        merger = "Name : " + name + ' ' + "Phone Number : " + phone1 + ' ' + "Email : " + email + ' ' + "Message : " + message
        send_mail(subject, merger, email, ['info.3kanya@gmail.com'])
        response = dict()
        response['success'] = "Thank You! We will contact You soon"
        # form.save()
        return JsonResponse(response)

    else:
        data = {
            'title': "Contact us",
            'ContactForm': Contact_Form
        }
        return render(request, 'pages/contact/contact.view.html', data)


def destination(request):
    destination_list = Destination.objects.filter(status=1).order_by("-id")
    page = request.GET.get('page', 1)
    paginator = Paginator(destination_list, 10)
    try:
        destination_data = paginator.page(page)
    except PageNotAnInteger:
        destination_data = paginator.page(1)
    except EmptyPage:
        destination_data = paginator.page(paginator.num_pages)

    data = {
        'title': "Destination",
        'destinationData': destination_data
    }
    return render(request, 'pages/destination/destination.view.html', data)


@csrf_exempt
def destination_details(request, criteria):
    destinationdetails = Destination.objects.get(slug=criteria)
    back = request.META.get('HTTP_REFERER')
    if request.method == 'POST' and 'booking' in request.POST:
        form = DestinationForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('contact')
            depature = request.POST.get('depature')
            person = request.POST.get('person')
            destination_name = request.POST.get('destination_name')
            # Dropdown ko name bata tanyeko destination_name
            message = request.POST.get('message')
            destination_obj = Destination_Booking(name=name, email=email, contact=phone, depature=depature,
                                                  person=person, destination_name=destination_name, message=message)
            destination_obj.save()

            # sending mail to customer start #
            subject = "Booking for " + destination_name + " has been received"
            merger = "Namaste 🙏 " + name + \
                     ". Your booking has been received successfully our sales team will contact you soon. " \
                     "Thank You for choosing Teenkanya Travel & Trek Pvt. Ltd."
            send_mail(subject, merger, email, [destination_obj.email])
            # sending mail to customer end #

            details = {'Name': name, 'Email': email, 'Contact': phone, 'Destination': destination_name,
                       'Depature': depature, 'person': person, 'Message': message}
            text_content = render_to_string('destination_booking_email_template/email.txt', details)
            html_content = render_to_string('destination_booking_email_template/email.html', details)
            email = EmailMultiAlternatives('Destination  Booking for  ' + destination_name, text_content)
            email.attach_alternative(html_content, "text/html")
            email.to = ['sales.3kanya@gmail.com']
            email.send()
            messages.success(request, 'Booking has been successful. We will contact you soon',
                             "alert alert-success alert-dismissible")
            return redirect(back)
        else:

            messages.error(request, 'Error in booking please fill the form again. Thank You!!',
                           "alert alert-warning alert-dismissible")
            return redirect(back)
    else:
        data = {
            'title': destinationdetails.title,
            'image': destinationdetails.image.url,
            'description': destinationdetails.description,
            'url': "https://3kanyatravel.com.np/destination-details/" + destinationdetails.slug,
            'destinationForm': DestinationForm,
            'destinationdetails': Destination.objects.get(slug=criteria),
            'destinationData': Destination.objects.all()
        }
        return render(request, 'pages/destination/destination-details.view.html', data)


@login_required(login_url='login')
def bookinglist(request):
    destination_list = Destination_Booking.objects.filter(status="Waiting").order_by("-id") | \
                       Destination_Booking.objects.filter(status="Contacted").order_by("-id")

    page = request.GET.get('page', 1)
    paginator = Paginator(destination_list, 30)
    try:
        booking = paginator.page(page)
    except PageNotAnInteger:
        booking = paginator.page(1)
    except EmptyPage:
        booking = paginator.page(paginator.num_pages)

    data = {
        'title': "Booking List",
        'bookingData': booking,
        'dashbar': 'bookinglist'
    }
    return render(request, 'pages/bookinglist/bookinglist.html', data)


def blogz(request):
    blog_list = BlogData.objects.filter(status=1).order_by("-id")
    page = request.GET.get('page', 1)
    paginator = Paginator(blog_list, 10)
    try:
        blogdata = paginator.page(page)
    except PageNotAnInteger:
        blogdata = paginator.page(1)
    except EmptyPage:
        blogdata = paginator.page(paginator.num_pages)

    data = {
        'blogData': blogdata,
        'title': "Blog"
    }
    return render(request, 'pages/blog/blog.view.html', data)


def blogz_details(request, criteria):
    get_view = BlogData.objects.get(slug=criteria)
    get_view.page_visit += 1
    get_view.save()
    data = {
        'title': get_view.title,
        'image': get_view.image.url,
        'description': get_view.description,
        'url': "https://3kanyatravel.com.np/blogz-details/" + get_view.slug,
        'blogData': BlogData.objects.filter(status=1),
        'blogzdetails': BlogData.objects.get(slug=criteria)

    }
    return render(request, 'pages/blog/blogs-details.view.html', data)


def vacancy(request):
    today = timezone.now().date()
    for reminder in Vacancy.objects.filter(lastdate__day=today.day,
                                           lastdate__month=today.month,
                                           lastdate__year=today.year):
        # for reminder in Vacancy.objects.filter(lastdate=date.today() + relativedelta(days=-1)):
        reminder.status = 0
        reminder.save()
    data = {
        'title': "Carrer",
        'vacancyData': Vacancy.objects.filter(status=1)
    }
    return render(request, 'pages/vacancy/vacancy.view.html', data)


@csrf_exempt
def vacancy_details(request, criteria):
    if request.method == 'POST' and 'vacancy_apply' in request.POST:
        form = VacancyForm(request.POST, request.FILES)
        back = request.META.get('HTTP_REFERER')
        if form.is_valid():
            name = request.POST.get('name')
            form_email = request.POST.get('email')
            phone = request.POST.get('phone')
            photo = request.FILES.get('photo')
            cv = request.FILES.get('cv')
            position = request.POST.get('position')

            if ApplicantData.objects.filter(email=form_email).exists():
                messages.error(request, 'Vacancy already applied from email ' + form_email,
                               "alert alert-warning alert-dismissible")
                return redirect(back)

            c = {'Name': name, 'Email': form_email, 'Contact': phone, 'Position': position}
            text_content = render_to_string('vacancy_email_template/email.txt', c)
            html_content = render_to_string('vacancy_email_template/email.html', c)
            email = EmailMultiAlternatives('Vacancy Applied for  ' + position, text_content)
            email.attach_alternative(html_content, "text/html")
            email.attach(cv.name, cv.read(), cv.content_type)
            email.attach(photo.name, photo.read(), photo.content_type)
            email.to = ['vacancy.3kanya@gmail.com']
            email.send()
            applicant_obj = ApplicantData(name=name, email=form_email, contact=phone, photo=photo, cv=cv,
                                          position=position)
            applicant_obj.save()
            messages.success(request, 'Vacancy Applied Successfully', "alert alert-success alert-dismissible")
            return redirect(back)
        get_view = Vacancy.objects.get(slug=criteria)
        get_view.page_visit += 1
        get_view.save()
        data = {
            'VacancyForm': form,
            'title': get_view.title,
            'description': get_view.job_description,
            'url': "https://3kanyatravel.com.np//vacancy-details/" + get_view.slug,
            'vacancydetails': Vacancy.objects.get(slug=criteria)
        }
        return render(request, 'pages/vacancy/vacancy-details.view.html', data)

    else:
        get_view = Vacancy.objects.get(slug=criteria)
        get_view.page_visit += 1
        get_view.save()
        data = {
            'VacancyForm': VacancyForm,
            'title': get_view.title,
            'description': get_view.job_description,
            'url': "https://3kanyatravel.com.np/vacancy-details/" + get_view.slug,
            'vacancydetails': Vacancy.objects.get(slug=criteria)
        }
        return render(request, 'pages/vacancy/vacancy-details.view.html', data)


@login_required(login_url='login')
def vacancylist(request):
    app_list = ApplicantData.objects.all().order_by("id")
    page = request.GET.get('page', 1)
    paginator = Paginator(app_list, 5)
    try:
        applicants = paginator.page(page)
    except PageNotAnInteger:
        applicants = paginator.page(1)
    except EmptyPage:
        applicants = paginator.page(paginator.num_pages)

    data = {
        'applicants': applicants,
        'title': "Applicant List",
        'dashbar': 'vacancylist'
    }
    return render(request, 'pages/vacancy/vacancy_list.html', data)


def login(request):
    if request.method == 'POST':
        forms = AuthenticationForm(data=request.POST)
        if forms.is_valid():
            user = forms.get_user()
            log(request, user)
            return redirect('vacancylist')
        else:
            back = request.META.get('HTTP_REFERER')
            messages.error(request, 'Username or Password Incorrect')
            return redirect(back)

    else:
        data = {
            'title': "login",
            'login_form': AuthenticationForm
        }
        return render(request, 'pages/users/login.view.html', data)


@login_required(login_url='login')
def register(request):
    if request.method == 'POST':
        back = request.META.get('HTTP_REFERER')
        forms = UserRegister(request.POST)
        if forms.is_valid():
            instance = forms.save(commit=False)
            if User.objects.filter(email=instance.email).exists():
                messages.info(request, instance.email + ' is already registered please use another email',
                              "alert alert-info alert-dismissible")
                return redirect(back)

            # if User.objects.filter(username=instance.username).exists():
            #     messages.error(request, 'Username Already Registered Please Use Another Username',
            #                    "alert alert-info alert-dismissible")
            #     return redirect(back)

            else:
                instance.save()
                messages.success(request, "Successfully Registered to", "alert alert-success alert-dismissible")
                subject = "User Created for Teenkanya Admin"
                email = settings.EMAIL_HOST_USER
                merger = "Welcome, to Teenkanya Travel & Trek Pvt. Ltd. User has been created successfully . " \
                         "Please visit login page to login with registered username and password "
                send_mail(subject, merger, email, [instance.email])
                return redirect(back)
        else:
            messages.error(request, "Something is error", "alert alert-warning alert-dismissible")
            return redirect(back)

    else:
        data = {
            'title': "User Register",
            'userForm': UserRegister,
            'dashbar': 'register'
        }
        return render(request, 'pages/users/register.view.html', data)


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

    else:
        return redirect('login')


def export_applicant_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="applicant.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('ApplicantData')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name', 'Email', 'Contact', 'Applied Postion', 'CV', 'Photo']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = ApplicantData.objects.all().values_list('name', 'email', 'contact', 'position', 'cv', 'photo')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def search(request):
    template = 'pages/destination/search.html'
    query = request.GET.get('q')

    results = Destination.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    data = {
        'items': results,
        'title': "Search Result",
    }

    return render(request, template, data)


# def newsletter_subscribe(request):
#     back = request.META.get('HTTP_REFERER')
#     form = NewsletterSignUpForm(request.POST or None)
#     back = request.META.get('HTTP_REFERER')
#     if request.method == 'POST' and 'subscribe' in request.POST:
#         if form.is_valid():
#             instance = form.save(commit=False)
#             if NewsletterUser.objects.filter(email=instance.email).exists():
#                 messages.warning(request, 'Email already exist. Please enter new email address',
#                                  "alert alert-warning alert-dismissible")
#                 return redirect(back)
#             else:
#                 instance.save()
#                 messages.success(request, "Successfully Subscribed", "alert alert-success alert-dismissible")
#                 text_content = render_to_string('pages/newsletters/sign_up_email.txt')
#                 html_content = render_to_string('pages/newsletters/sign_up_email.html')
#                 email = EmailMultiAlternatives("Newsletter Subscription", text_content)
#                 email.attach_alternative(html_content, "text/html")
#                 email.to = [instance.email]
#                 email.send()
#                 return redirect(back)
#
#     else:
#         context = {
#             'title': "Newsletter Unsubscribe",
#         }
#         return redirect(back)


def newsletter_unsubscribe(request):
    back = request.META.get('HTTP_REFERER')
    form_unsubscribe = NewsletterSignUpForm(request.POST or None)
    if request.method == 'POST' and 'unsubscribe' in request.POST:
        if form_unsubscribe.is_valid():
            instance = form_unsubscribe.save(commit=False)
            if NewsletterUser.objects.filter(email=instance.email).exists():
                NewsletterUser.objects.filter(email=instance.email).delete()
                messages.success(request,
                                 "Successfully unsubscribed. You will no longer get email for new deal from Teenkanya",
                                 "alert alert-warning alert-dismissible")
                text_content = render_to_string('pages/newsletters/unsubscribe_email.txt')
                html_content = render_to_string('pages/newsletters/unsubscribe_email.html')
                email = EmailMultiAlternatives("Newsletter Unsubscription", text_content)
                email.attach_alternative(html_content, "text/html")
                email.to = [instance.email]
                email.send()
                return redirect(back)
            else:
                messages.error(request, "No Email Found", "alert alert-warning alert-dismissible")
                return redirect(back)
    else:
        context = {
            'form_unsubscribe': form_unsubscribe,
            'title': "Newsletter Unsubscribe",
        }

        template = "pages/newsletters/unsubscribe.html"
        return render(request, template, context)


@login_required(login_url='login')
def control_newsletter(request):
    back = request.META.get('HTTP_REFERER')
    form = NewsletterCreationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            newsletter = Newsletter.objects.get(id=instance.id)
            if newsletter.status == "Published":
                subject = newsletter.subject
                body = newsletter.body
                # email = settings.EMAIL_HOST_USER
                # image = request.FILES.get('image')
                image = newsletter.image
                for email_list in newsletter.email.all():
                    # send_mail(subject, body, email, [email_list])
                    c = {'body': body, 'image': image}
                    text_content = render_to_string('pages/newsletters/newsletter_email_to_user.txt', c)
                    html_content = render_to_string('pages/newsletters/newsletter_email_to_user.html', c)
                    email = EmailMultiAlternatives(subject, text_content)
                    email.attach_alternative(html_content, "text/html")
                    email.attach(image.name, image.read())
                    email.to = [email_list]
                    email.send()
            messages.success(request, "Newsletter send successfully", "alert alert-success alert-dismissible")
            return redirect(back)
        else:
            return redirect(back)
    else:
        context = {
            'title': "Newsletter",
            "form": form,
            'dashbar': 'newsletter'
        }
    template = 'pages/newsletters/newsletter_form.html'
    return render(request, template, context)


#
# def error_404_view(request, exception):
#     context = {
#         'title': "Page Not Found",
#     }
#     render(request, '404.html', context)


# api

def covid19(request):
    get_url = "https://nepalcorona.info/api/v1/data/nepal"

    payload = {}
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", get_url, headers=headers, data=payload)

    data = {
        'title': "Nepal Corona Update",
        'newsdata': response.json(),

    }
    return render(request, 'pages/covid19/covid19.view.html', data)
# apiend
