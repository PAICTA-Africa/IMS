from django.shortcuts import render, redirect
from PIL import Image
import numpy as np
import os
import io
import base64
import uuid
import re
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from .models import Employee
from ipware import get_client_ip

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from .models import employees
from .models import resignation_model, Project, Leave, Termination, clockin
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Sum
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from geopy.geocoders import Nominatim
import time
#from django.db.models.signals import pre_save
#from django.dispatch import receiver

def landing(request):
    return render(request, "landing.html", {})
def detect_face(image_path):
    """
    This function takes an image path, detects and returns the face region of the image
    """
    image = Image.open(image_path).convert('L')
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(np.array(image), 1.3, 5)
    
    if len(faces) == 0:
        return None
    
    (x, y, w, h) = faces[0]
    face = np.array(image)[y:y+h, x:x+w]
    return face

def compare_faces(img1, img2):
    """
    This function takes two images and returns True if they belong to the same person
    """
    face1 = detect_face(img1)
    face2 = detect_face(img2)
    
    if face1 is None or face2 is None:
        return False
    
    # Resize the images to the same size
    face1 = cv2.resize(face1, (100, 100))
    face2 = cv2.resize(face2, (100, 100))
    
    # Calculate the euclidean distance between the faces
    dist = np.sqrt(np.sum(np.square(face1 - face2)))
    
    # If the distance is less than 70, the faces belong to the same person
    if dist < 70:
        return True
    
    return False

def login(request):
    """
    This function handles the login request
    """
    # if request.method == 'POST':
    #     # Get the user's submitted image
    #     submitted_img = request.POST.get('image')
        
    #     # Get the user's saved image from the database
    #     user = User.objects.get(email=request.user.email)
    #     saved_img = user.profile_image
        
    #     # Compare the faces
    #     if compare_faces(submitted_img, saved_img):
    #         # If the faces belong to the same person, unlock
    #         return render(request, 'unlock.html')
    #     else:
    #         # If the faces do not belong to the same person, show error message
    #         messages.error(request, 'Authentication failed.')
            
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        name = request.POST['name']
        lastname = request.POST['lastname']
        id_number = request.POST['id_number']
        cell = request.POST['cell']
        dept = request.POST['dept']
        HAddress = request.POST['HAddress']
        WAddress = request.POST['WAddress']
        PAddress = request.POST['PAddress']
        ip, is_routable = get_client_ip(request)
        mac_address = hex(uuid.getnode())
        mac_address = mac_address.replace('0x', '')
        mac_address = re.findall('..', mac_address)
        
        if password != password2:
            messages.error(request, "Failed to register: Password characters do not match")
            datatemplate = loader.get_template('authenticate/register.html')
            return HttpResponse(datatemplate.render(context, request))
            exit 
            
        if id_number == "":
            message.error(request, "Failed to register: ID Number cannot be null")
            datatemplate = loader.get_template('authenticate/register.html')
            return HttpResponse(datatemplate.render(context, request))
            exit 
            
        fpassword = make_password(password)
        post = Employee.objects.create_user(email=email, password=fpassword)
        post.first_name = name
        post.email = email
        post.last_name = lastname
        post.password = fpassword
        post.id_number = id_number
        post.email = email
        post.mobile = cell
        post.department = dept
        post.homeAddress = HAddress
        post.workAddress = WAddress
        post.postal = PAddress
        # post.password = make_password(password, salt="ioutrfucvbuio;)(*&^%)")
        post.ip_address = ip
        post.mac_address = mac_address
        post.save()
        
        dtemplate = loader.get_template('authentication/login.html') 
        messages.success(request, "Account created! Login to continue accessing the system.")
        mydata = Employee.objects.all().values()
        context = {
            'mydata': mydata,
            'name': name
        }
        return HttpResponse(dtemplate.render(context, request))
    return render(request, 'authentication/register.html', {})

def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if not user.email == 'tech10@paicta.africa':
                # login(user) 
                return render(request, 'index.html', {'user': user})
            else:
                return render(request, 'IMS_empDash.html', {'user': user})
        else:
            messages.error(request, "Login failed: Incorrect user details")
    return render(request, 'authentication/login.html', {})

@login_required
def ClockingView(request):
    employee = request.employee
    return render(request, 'index.html', {'employee': employee})

# @login_required
def clock_action(request, user_id):
    if request.method == "POST":
        IDNumber = request.POST["myid"]
        FirstName = request.POST["name"]
        LastName = request.POST["lastname"]
        ip, is_routable = get_client_ip(request)
        geolocator = Nominatim(user_agent="my-app")
        location = geolocator.geocode("me")
        final = "{:.6f} {:.6f}".format(location.latitude, location.longitude)
        
        post = clockin()
        post.user_id = user_id
        post.IDNumber = IDNumber
        post.FirstName = FirstName
        post.LastName = LastName
        post.ip_address = ip
        post.geolocation = final
        post.save()
        
        
        if is_routable == 'FALSE':
            messages.warning(request, "Successfully clocked is. However, your device is not routable!")
            return render(request, "timesheet_success.html", {})
        else:
            messages.success(request, "Successfully clocked in, your device is routable!")
            # messages.info(request, "Failed to load live location, Access denied!")
            dtemplate = loader.get_template('timesheet_success.html') 
            # messages.success(request, "Account created! Login to continue accessing the system.")
            mydata = clockin.objects.filter(user_id=user_id)
            context = {
                'mydata': mydata
                # 'name': name
            }
            return HttpResponse(dtemplate.render(context, request))
            # return render(request, "timesheet_success.html", {"user": user})
        
        return render(request, "index.html", {})

def my_profile(request):
    return render(request, 'profile.html', {})

def update_profile(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        birth_date = request.POST['birth_date']
        gender = request.POST['gender']
        address = request.POST['address']
        state = request.POST['state']
        country = request.POST['country']
        zip_code = request.POST['zip_code']
        phone_number = request.POST['phone_number']
        department = request.POST['department']
        designation = request.POST['designation']
        report = request.POST['report']
        post = UserProfile()
        post.fname = fname
        post.lname = lname
        post.birth_date = birth_date
        post.gender = gender
        post.address = address
        post.state = state
        post.country = country
        post.zip_code = zip_code
        post.phone_number = phone_number
        post.department = department
        post.designation = designation
        post.report = report
        post.save()
    return render(request, 'profile.html')

def update_info(request):
    if request.method == "POST":
        id_num = request.POST['id_num']
        pass_num = request.POST['pass_num']
        pass_expdate = request.POST['pass_expdate']
        phone_num = request.POST['phone_num']
        nationality = request.POST['nationality']
        religion = request.POST['religion']
        marital_st = request.POST['marital_st']
        emp_spouse = request.POST['emp_spouse']
        num_child = request.POST['num_child']
        post = PersInfo()
        post.id_num = id_num
        post.pass_num = pass_num
        post.pass_expdate = pass_expdate
        post.phone_num = phone_num
        post.nationality = nationality
        post.religion = religion
        post.marital_st = marital_st
        post.emp_spouse = emp_spouse
        post.num_child = num_child
        post.save()
    return render(request, 'profile.html')

def update_emerg(request):
    if request.method == "POST":
        emerg_name = request.POST['emerg_name']
        emerg_rel = request.POST['emerg_rel']
        phone_1 = request.POST['phone_1']
        phone_2 = request.POST['phone_2']
        em_name = request.POST['em_name']
        em_rel = request.POST['em_rel']
        em_phone_1 = request.POST['em_phone_1']
        em_phone_2 = request.POST['em_phone_2']
        post = EmergCon()
        post.emerg_name = emerg_name
        post.emerg_rel = emerg_rel
        post.phone_1 = phone_1
        post.phone_2 = phone_2
        post.em_name = em_name
        post.em_rel = em_rel
        post.em_phone_1 = em_phone_1
        post.em_phone_2 = em_phone_2
        post.save()
    return render(request, 'profile.html')

def update_family_info(request):
    if request.method == "POST":
        fam_member_name = request.POST['fam_member_name']
        fam_rel = request.POST['fam_rel']
        date_of_birth = request.POST['date_of_birth']
        fam_member_phone = request.POST['fam_member_phone']
        post = FamilyInfo()
        post.fam_member_name = fam_member_name
        post.fam_rel = fam_rel
        post.date_of_birth = date_of_birth
        post.fam_member_phone = fam_member_phone
        post.save()
    return render(request, 'profile.html')

def update_education_info(request):
    if request.method == "POST":
        inst = request.POST['inst']
        subject = request.POST['subject']
        start_date = request.POST['start_date']
        compl_date = request.POST['compl_date']
        qual_name = request.POST['qual_name']
        grade = request.POST['grade']
        sec_inst = request.POST['sec_inst']
        sec_subject = request.POST['sec_subject']
        sec_start_date = request.POST['sec_start_date']
        sec_compl_date = request.POST['sec_compl_date']
        sec_qual_name = request.POST['sec_qual_name']
        sec_grade = request.POST['sec_grade']
        post = EducationInfo()
        post.inst = inst
        post.subject = subject
        post.start_date = start_date
        post.compl_date = compl_date
        post.qual_name = qual_name
        post.grade = grade
        post.sec_inst = sec_inst
        post.sec_subject = sec_subject
        post.sec_start_date = sec_start_date
        post.sec_compl_date = sec_compl_date
        post.sec_qual_name = sec_qual_name
        post.sec_grade = sec_grade
        post.save()
    return render(request, 'profile.html')


def update_experience_info(request):
    if request.method == "POST":
        company_name = request.POST['company_name']
        location = request.POST['location']
        job_position = request.POST['job_position']
        period_f = request.POST['period_f']
        period_t = request.POST['period_t']
        sec_company_name = request.POST['sec_company_name']
        sec_location = request.POST['sec_location']
        sec_job_position = request.POST['sec_job_position']
        sec_period_f = request.POST['sec_period_f']
        sec_period_t = request.POST['sec_period_t']
        post = ExperienceInfo()
        post.company_name = company_name
        post.location = location
        post.job_position = job_position
        post.period_f = period_f
        post.period_t = period_t
        post.sec_company_name = sec_company_name
        post.sec_location = sec_location
        post.sec_job_position = sec_job_position
        post.sec_period_f = sec_period_f
        post.sec_period_t = sec_period_t
        post.save()
    return render(request, 'profile.html')

@login_required
def account(request):
    # logout(request)
    return redirect('landing')

def DashboardApp(request):
    x = employees.objects.all().values()
    template = loader.get_template('IMS_empDash.html')
    context = {
        'content': x
    }

    return HttpResponse(template.render(context, request))
    # return render(request, 'IMS_empDash.html')

# def employees(request):
#     return render(request, 'employees.html')

"""
def leaves(request):
    leave = Leave.objects.all()
    return render(request, 'leaves.html', {'leave':leave})

@receiver(pre_save, sender=Leave)
def update_remaining_number(sender, instance, **kwargs):
    instance.calculate_remaining_number()
"""
        

def resignation(request):
    if request.method == "POST":
        x = resignation_model.objects.all().values()
        template = loader.get_template('resignation.html')
        context = {
            'info': x
        }
        myfiles = request.FILES['resignation_letter']
        fs = FileSystemStorage()
        # data = dict()
        messages.success(request, "Success: You have successfully uploaded your resignation letter!")
        filename = fs.save(myfiles.name, myfiles)
        post = resignation_model()
        post.empname = request.POST['name']
        post.filename = myfiles
        post.reason = request.POST['reason']
        # post.noticedate = request.POST['noticedate']
        # post.resigndate = request.POST['resignation']
        post.save()
        uploaded_file_url = fs.url(filename)
        
        return HttpResponse(template.render(context, request))
        # return render(request, 'resignation.html', {'uploaded_file_url':uploaded_file_url})
    else:
        return render(request, 'resignation.html')

def termination(request):
    if request.method == "POST":
        x = Termination.objects.all().values()
        template = loader.get_template('termination.html')
        context = {
            'info': x
        }
        myfiles = request.FILES['termination_letter']
        fs = FileSystemStorage()
        # data = dict()
        messages.success(request, "Success: You have successfully uploaded your Termination letter!")
        filename = fs.save(myfiles.name, myfiles)
        post = Termination()
        post.empname = request.POST['name']
        post.filename = myfiles
        post.reason = request.POST['reason']
        # post.noticedate = request.POST['noticedate']
        # post.resigndate = request.POST['resignation']
        post.save()
        uploaded_file_url = fs.url(filename)
        
        return HttpResponse(template.render(context, request))
        # return render(request, 'resignation.html', {'uploaded_file_url':uploaded_file_url})
    else:
        return render(request, 'resignation.html')
    
    """
    if request.method == "POST":
        myfiles = request.FILES['termination_letter']
        fs = FileSystemStorage()
        filename = fs.save(myfiles.name, myfiles)
        uploaded_file_url = fs.url(filename)
        
        return render(request, 'termination.html', {'uploaded_file_url':uploaded_file_url})
    else:
        return render(request, 'termination.html')
    """
        
def employee(request):
    x = employees.objects.all()
    return render(request, 'employees.html')
 
def IMS_empDash(request):
    return render(request, 'IMS_empDash.html')    

def project_view(request):
    projects= Project.objects.all().values()
    return render(request, 'project_view.html',{'projects':projects})



def leaves_view(request):
    persons = Leave.objects.all()
    context = {'persons': persons}

    return render(request, 'leaves.html', context)

class LeaveListView(ListView):
    model = Leave
    template_name = 'leaves.html'

class LeaveDetailView(DetailView):
    model = Leave
    template_name = 'employee_detail.html'

def leave_summary(request, year):
    leaves = Leave.objects.filter(start_date__year=year)
    leave_counts = {}

    for leave in leaves:
        if leave.leave_type not in leave_counts:
            leave_counts[leave.leave_type] = {
                'total': 0,
                'taken': 0,
                'remaining': 0,
            }

    leave_counts[leave.leave_type]['total'] += leave.duration
    leave_counts[leave.leave_type]['taken'] += leave.duration

    for leave_type, counts in leave_counts.items():
        counts['remaining'] = counts['total'] - counts['taken']

    return render(request, 'leaves.html', {
        'year': year,
        'leave_counts': leave_counts,
    })
