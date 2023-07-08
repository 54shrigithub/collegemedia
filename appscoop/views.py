from django.shortcuts import render,HttpResponse,redirect
from appscoop.models import *
from django.apps import apps
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from PIL import Image
from datetime import datetime,timedelta
from django.db.models import Q,Count
import threading
import io
import uuid

import os


def send_email_thread(subject, message, from_email, recipient_list, fail_silently=False):
    send_mail(subject, message, from_email, recipient_list, fail_silently=fail_silently)


# Create your views here.

def index(request):
    images=publics.objects.order_by('-date','-id')
    return render(request,'index.html',{'images': images})

def logins(request):
    if not request.user.is_anonymous:
        if request.session['remember']:
            user=request.user
            if user.is_superuser:
                    login(request,user)
                    return redirect('adminn')
            elif user.is_staff:
                    login(request,user)
                    return redirect('staff')
            else:
                    login(request,user)
                    return redirect('student')
    
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        remember=request.POST.get('rem')
        print(remember)
        if remember:
            request.session['remember']=1
        else:
            request.session['remember']=0
        user=authenticate(request,username=username,password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return render(request,'signin.html',{'page':'adminn'})
                # return redirect('adminn')
            elif user.is_staff:
                login(request,user)
                return render(request,'signin.html',{'page':'staff'})
                # return redirect('staff')
            else:
                login(request,user)
                return render(request,'signin.html',{'page':'student'})
                # return redirect('student')
        else:
            messages.warning(request,'Wrong user ID or Password!!')
            return render(request,'signin.html')
    else:
        return render(request,'signin.html')
        
    
            

import uuid
def staff(request):
        if request.user.is_staff and request.user.is_superuser == False:
            if request.method=="POST":
                token = request.POST.get('form_token')
                if token in request.session.get('form_tokens', []):
                    form_token = str(uuid.uuid4())
                    images=college.objects.order_by('-date','-id')
                    inbox = Inbox.objects.filter(sender__classname__in=[request.user.classname, "college"]).order_by('-id')
                    return render(request, 'stfpage.html', {'form_token': form_token,'images': images,'inbox':inbox})
                elif request.POST.get("clg_btn"):
                        image_file=request.FILES.get('image')
                        imgname=request.POST['imagename']
                        imgcaption=request.POST['imgcaption']
                        user=request.user
                        col_post=college(student=user,image=image_file,imagename=imgname,imagecaption=imgcaption)
                        col_post.save()
                        messages.success(request,"Post uploaded to College Successfully...!")
                elif request.POST.get("pub_btn"):
                        image_file=request.FILES.get('image')
                        imgname=request.POST['imagename']
                        imgcaption=request.POST['imgcaption']
                        user=request.user
                        pub_post=publics(student=user,image=image_file,imagename=imgname,imagecaption=imgcaption)
                        pub_post.save()
                        messages.success(request,"Post uploaded to Public Successfully...!")
                request.session.setdefault('form_tokens', []).append(token)
            
            form_token = str(uuid.uuid4())
            images=college.objects.order_by('-date','-id')
            inbox = Inbox.objects.filter(sender__classname__in=[request.user.classname, "college"]).order_by('-id')
            return render(request,'stfpage.html',{'form_token': form_token,'images': images,'inbox':inbox})
        else:
            return redirect(logins)
        





def student(request):
    if request.method=="POST":
        if request.POST.get("post_btn"):
            image_file=request.FILES.get('image')
            imgname=request.POST['imagename']
            imgcaption=request.POST['imgcaption']
            user=request.user
            postreq=Post_req(student=user,imagename=imgname,image=image_file,imagecaption=imgcaption)
            postreq.save()

    if not request.user.is_anonymous and request.user.is_staff == False and request.user.is_superuser == False:
        current_month = datetime.now().month
        current_year=datetime.now().year
        try:
            top3 = college.objects.annotate(num_likes=Count('likes')).filter(Q(date__month=current_month) & Q(date__year=current_year)).order_by('-num_likes')[:3]
        except:
            today = datetime.now()
            first_day_of_current_month = today.replace(day=1)
            last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
            first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

            top3 = college.objects.annotate(num_likes=Count('likes')).filter(
                Q(date__year=first_day_of_previous_month.year) &
                Q(date__month=first_day_of_previous_month.month)
            ).order_by('-num_likes')[:3]

        images=college.objects.order_by('-date','-id')
        inbox = Inbox.objects.filter(sender__classname__in=[request.user.classname, "college"]).order_by('-id')
        return render(request,'studpage.html',{'images': images,'inbox':inbox,'mostliked':top3})
    else:
        return redirect(logins)
        
        
        



def adminn(request):
    if request.user.is_superuser:
            if request.method=="POST":
                token = request.POST.get('form_token')
                if token in request.session.get('form_tokens', []):
                    form_token = str(uuid.uuid4())
                    images=college.objects.order_by('-date','-id')
                    inbox=Inbox.objects.order_by('-id')
                    return render(request, 'adm.html', {'form_token': form_token,'images': images,'inbox':inbox})
                elif request.POST.get("clg_btn"):
                        image_file=request.FILES.get('image')
                        imgname=request.POST['imagename']
                        imgcaption=request.POST['imgcaption']
                        user=request.user
                        col_post=college(student=user,image=image_file,imagename=imgname,imagecaption=imgcaption)
                        col_post.save()
                        messages.success(request,"Post uploaded to College Successfully...!")
                elif request.POST.get("pub_btn"):
                        image_file=request.FILES.get('image')
                        imgname=request.POST['imagename']
                        imgcaption=request.POST['imgcaption']
                        user=request.user
                        pub_post=publics(student=user,image=image_file,imagename=imgname,imagecaption=imgcaption)
                        pub_post.save()
                        messages.success(request,"Post uploaded to Public Successfully...!")
                request.session.setdefault('form_tokens', []).append(token)
            
            form_token = str(uuid.uuid4())
            images=college.objects.order_by('-date','-id')
            inbox=Inbox.objects.order_by('-id')
            return render(request,'adm.html',{'form_token': form_token,'images': images,'inbox':inbox})
    else:
        return redirect(logins)



def addstafftoclasstab(request):
    if request.user.is_superuser:
        if request.method=="POST":
            if request.POST.get("add")=='':
                stfid=request.POST['stfid']
                mname=request.POST['mname']
                classname=request.POST['classname']
                password=request.POST['password']
                email=request.POST['email']
                mentor=User.objects.filter(username=stfid,classname=classname)
                if not mentor:
                    mentor=User.objects.create_user(username=stfid,classname=classname,is_staff=True,password=password,first_name=mname,email=email)
                    mentor.save()
                    messages.success(request,'successfully added a staff')
                    staffs=User.objects.filter(is_staff=True,is_superuser=False)
                    email_thread = threading.Thread(target=send_email_thread, args=('Created Account at College Media','Now you can visit to college media and login with the staff id = '+str(stfid), 'settings.EMAIL_HOST_USER', [email], False))
                # Start the thread
                    email_thread.start()
                    return render(request,'addstafftoclasstab.html',{"staffs":staffs,})
                else:
                    messages.warning(request,"The mentor "+ stfid +" is already present in "+ classname)
                    staffs=User.objects.filter(is_staff=True,is_superuser=False)
                    return render(request,'addstafftoclasstab.html',{"staffs":staffs,})
            elif request.POST.get("del")=='':
                        stid=request.POST['stafid']
                        st= User.objects.filter(username=stid)
                        if not st:
                            messages.warning(request,"The staff with ID "+stid+" does not exist." )
                            staffs=User.objects.filter(is_staff=True,is_superuser=False)
                            return render(request,'addstafftoclasstab.html',{"staffs":staffs,})
                        else:
                            std=st[0]
                            messages.success(request,"The staff with ID "+stid+" has been deleted." )
                            email_thread = threading.Thread(target=send_email_thread, args=('Deleted Account at College Media','Your staff id = '+str(stid)+' has been deleted . You can no more login with this ID.', 'settings.EMAIL_HOST_USER', [std.email], False))
                # Start the thread
                            email_thread.start()
                            std.delete()
                            staffs=User.objects.filter(is_staff=True,is_superuser=False)
                            return render(request,'addstafftoclasstab.html',{"staffs":staffs,})
            elif request.POST.get("chg")=='':
                        stid=request.POST['stafid']
                        ncls=request.POST['cls']
                        st= User.objects.filter(username=stid)
                        if not st:
                            messages.warning(request,"The staff with ID "+stid+" does not exist." )
                            staffs=User.objects.filter(is_staff=True,is_superuser=False)
                            return render(request,'addstafftoclasstab.html',{"staffs":staffs,})
                        else:
                            std=st[0]
                            std.classname=ncls
                            std.save()
                            messages.success(request,"The staff with ID "+stid+" is now of class"+ncls )
                            staffs=User.objects.filter(is_staff=True,is_superuser=False)
                            return render(request,'addstafftoclasstab.html',{"staffs":staffs,})
        else:
            staffs=User.objects.filter(is_staff=True,is_superuser=False)
            return render(request,'addstafftoclasstab.html',{"staffs":staffs,})
    else:
        return redirect(logins)

def studview(request):
    if request.user.is_superuser:
        distinct_rows = User.objects.exclude(is_superuser=True).values('classname').distinct()
        print(distinct_rows)
        if request.method=="POST":
            if request.POST.get("view"):
                classname=request.POST['classname']
                students=User.objects.filter(classname=classname,is_staff=False).order_by("username")
                mentor=User.objects.filter(classname=classname,is_staff=True)
                return render(request,'allstudview.html',{'students':students,'mentor' : mentor,'classname':distinct_rows,})
        else:
            return render(request,'allstudview.html',{'classname':distinct_rows,})
    else:
        return redirect(logins)


def addstudenttoclasstab(request):
            if request.user.is_staff and request.user.is_superuser == False:
                if request.method=="POST":
                    if request.POST.get("add")=='':
                        sname=request.POST['sname']
                        password=request.POST['password']
                        roleno=request.POST['roleno']
                        email=request.POST['email']
                        stud=User.objects.filter(username=roleno)
                        if not stud:
                            stud=User.objects.create_user(username=roleno,password=password,first_name=sname,classname=request.user.classname,email=email)
                            stud.save()
                            # classname=apps.get_model(app_label='appscoop', model_name=request.user.classname)
                            # addingtoclass=classname(student=stud,roleno=roleno,studentname=sname)
                            # addingtoclass.save()
                            messages.success(request,'successfully added a student')
                            studs=User.objects.filter(classname=request.user.classname,is_staff=False)
                            return render(request,'addstudenttoclasstab.html',{"students":studs,})
                        else:
                            messages.info(request,'student with the role-number '+roleno+' already exist')
                            studs=User.objects.filter(classname=request.user.classname,is_staff=False)
                            return render(request,'addstudenttoclasstab.html',{"students":studs,})
                    elif request.POST.get("del")=='':
                        rlno=request.POST['rollNo']
                        print(rlno)
                        st= User.objects.filter(username=rlno)
                        if not st:
                            messages.warning(request,"The student with Role Number "+rlno+" does not exist." )
                            studs=User.objects.filter(classname=request.user.classname,is_staff=False)
                            return render(request,'addstudenttoclasstab.html',{"students":studs,})
                        else:
                            std=st[0]
                            std.delete()
                            studs=User.objects.filter(classname=request.user.classname,is_staff=False)
                            messages.warning(request,"The student with Role Number "+rlno+" has been deleted." )
                            return render(request,'addstudenttoclasstab.html',{"students":studs,})
                else:
                        studs=User.objects.filter(classname=request.user.classname,is_staff=False)
                        return render(request,'addstudenttoclasstab.html',{"students":studs,})
            else:
                return redirect(logins)
            
import random
def forgetpass(request):
    if request.method=="POST":
        if request.POST.get("get_otp"):
            email=request.POST['email']
            print(email)
            user=User.objects.filter(email=email)
            print(user)
            # fuser=user[0]
            if user:
                OTP=str(random.randrange(1000,9999))
                fu=User.objects.get(email=email)
                fu.otp=OTP
                fu.save()
                email_thread = threading.Thread(target=send_email_thread, args=('OTP to Reset Password', 'OTP= ' + OTP + ' ID = ' + fu.username, 'settings.EMAIL_HOST_USER', [fu.email], False))
                # Start the thread
                email_thread.start() 
                return render(request,'forgt.html',{'email':email})
            else:
                messages.warning(request,"The Email Entered is not Registerd!!!")
                return render(request,'forgt.html')
        elif request.POST.get("check_otp"):
            entered_otp=request.POST['otp']
            # print("e",entered_otp)
            o=User.objects.get(email=request.POST.get("check_otp"))
            if entered_otp==o.otp:
                o.otp='a'
                o.save()
                request.session['changed']=False
                return render(request,'forgt.html',{'change':o.email})
            else:
                messages.warning(request,"entered otp is wrong")
                return render(request,'forgt.html',{'email':o.email})
        elif request.POST.get("change_pass"):
            oc=User.objects.get(email=request.POST.get("change_pass"))
            password=request.POST['password']
            confirm_pass=request.POST['confirm_password']
            if request.session.get('changed', True):
                return render(request,"forgt.html")
            if password != confirm_pass:
                messages.warning(request,"The New Password and Confirm Password differs!!!")
                return render(request,'forgt.html',{'change':oc.email})
            else:
                oc.set_password(password)
                oc.otp='a'
                request.session['changed'] = True
                oc.save()
                return render(request,'forgt.html',{'success':'success'})
    else:
        return render(request,'forgt.html')
            
            
        

def logouts(request):
    logout(request)
    return  redirect('/')


def postaccept(request):
    if request.user.is_staff :
        if request.method=="POST":
            if request.POST.get("public_post"):
                post_id=request.POST.get("public_post")
                post_to_public=Post_req.objects.get(id=post_id)
                pub_post=publics(student=post_to_public.student,image=post_to_public.image,imagename=post_to_public.imagename,imagecaption=post_to_public.imagecaption)
                pub_post.save()
                post_to_delete=Post_req.objects.get(id=int(post_id))
                post_to_delete.delete()
                # images=Post_req.objects.all()
                images=Post_req.objects.filter(student__classname=request.user.classname,status='pending')
                return render(request,'postaccept.html',{'images': images})
            if request.POST.get("college_post"):
                post_id=request.POST.get("college_post")
                post_to_college=Post_req.objects.get(id=post_id)
                col_post=college(student=post_to_college.student,image=post_to_college.image,imagename=post_to_college.imagename,imagecaption=post_to_college.imagecaption)
                col_post.save()
                post_to_delete=Post_req.objects.get(id=int(post_id))
                post_to_delete.delete()
                # images=Post_req.objects.all()
                images=Post_req.objects.filter(student__classname=request.user.classname,status='pending')
                return render(request,'postaccept.html',{'images': images})
            if request.POST.get("reject_post"):
                post_id=request.POST.get("reject_post")
                post_to_delete=Post_req.objects.get(id=int(post_id))
                post_to_delete.status='Rejected'
                # post_to_delete.deletion_date=datetime.now()
                post_to_delete.save()
                # post_to_delete.delete()
                # images=Post_req.objects.all()
                images=Post_req.objects.filter(student__classname=request.user.classname,status='pending')
                return render(request,'postaccept.html',{'images': images})

        images=Post_req.objects.filter(student__classname=request.user.classname,status='pending')
        return render(request,'postaccept.html',{'images': images})
    else:
        return redirect(logins)





def adminpostaccept(request):
    if request.user.is_superuser:
        if request.method=="POST":
                if request.POST.get("public_post"):
                    post_id=request.POST.get("public_post")
                    post_to_public=Post_req.objects.get(id=post_id)
                    pub_post=publics(student=post_to_public.student,image=post_to_public.image,imagename=post_to_public.imagename,imagecaption=post_to_public.imagecaption)
                    pub_post.save()
                    post_to_delete=Post_req.objects.get(id=int(post_id))
                    post_to_delete.delete()
                    images=Post_req.objects.filter(status='pending')
                    return render(request,'postaccept.html',{'images': images})
                if request.POST.get("college_post"):
                    post_id=request.POST.get("college_post")
                    post_to_college=Post_req.objects.get(id=post_id)
                    col_post=college(student=post_to_college.student,image=post_to_college.image,imagename=post_to_college.imagename,imagecaption=post_to_college.imagecaption)
                    col_post.save()
                    post_to_delete=Post_req.objects.get(id=int(post_id))
                    post_to_delete.delete()
                    images=Post_req.objects.filter(status='pending')
                    return render(request,'postaccept.html',{'images': images})
                if request.POST.get("reject_post"):
                    post_id=request.POST.get("reject_post")
                    post_to_delete=Post_req.objects.get(id=int(post_id))
                    post_to_delete.delete()
                    images=Post_req.objects.filter(status='pending')
                    return render(request,'postaccept.html',{'images': images})

        images=Post_req.objects.filter(status='pending')
        return render(request,'postaccept.html',{'images': images})
    else:
        return redirect(logins)







def toggle_like_post(request, post_id):
    post = get_object_or_404(college, id=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        is_liked=False
    else:
        post.likes.add(user)
        is_liked=True
    post.save()
    data = {'likes': post.likes.count(),'is_liked':is_liked}
    return JsonResponse(data)


def ref_toggle_like_post(request, user_id,post_id):
    post = get_object_or_404(college, id=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        is_liked=False
    else:
        post.likes.add(user)
        is_liked=True
    post.save()
    data = {'likes': post.likes.count(),'is_liked':is_liked}
    return JsonResponse(data)



def newmail(request,title,msg):
    user = request.user
    print(title,msg)
    mail=Inbox(sender=user,title=title,message=msg)
    mail.save()
    if user.classname == "college":
        inbox=Inbox.objects.order_by('-id')
    else:
        inbox = Inbox.objects.filter(sender__classname__in=[request.user.classname, "college"]).order_by('-id')
    content=""
    for mail in inbox:
        content+="<tr><td>"+mail.sender.first_name+"<br /><font size='1'>"+mail.date.strftime('%d-%m-%Y')+"</font><i class='fas fa-trash-alt del' onclick='deli("+str(mail.id)+")'></i></td><td style='white-space: normal;max-width: 200px; overflow: hidden;'><strong>"+mail.title+"</strong><br />"+mail.message+"</td></tr>"
    data = {'newmail':content}
    # messages.success(request,"New mail sent")
    return JsonResponse(data)

# send_mail('trial','this is a mesage','settings.EMAIL_HOST_USER',['shriramnaik50@gmail.com'],fail_silently=False) 

# <tr>

# <td>Principal<br>date</td> 

# <td> title <br> This is a message </td>

# </tr>

def viewprofile(request):
    if not request.user.is_anonymous :
        images=college.objects.filter(student=request.user).order_by('-id')
        return render(request,"viewprofile.html",{'images': images})
    return redirect(logins)

def update_profile(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        bio_text = request.POST.get('bio')
        user=request.user
        if user.profile_img=='/static/images/default.jpg':
            user.profile_img=image_file
            user.bio=bio_text
            user.save()
        else:
            file_path = os.path.join(settings.MEDIA_ROOT, str(user.profile_img))
            os.remove(file_path)
            user.profile_img=image_file
            user.bio=bio_text
            user.save()
        return JsonResponse({'message': 'Image and Bio uploaded successfully.'})
    return JsonResponse({'error': 'No image received.'})


def search(request):
    if not request.user.is_anonymous:
        if request.method=="POST":
            nam=request.POST['searchInput']
            user_list=User.objects.filter(first_name__icontains=nam)
            if user_list:
                return render(request,"search.html",{"result":user_list})
        return render(request,"search.html")
    else:
        return redirect(logins)

def profile_view(request,user_id):
    if not request.user.is_anonymous:
        person=User.objects.get(id=user_id)
        images=college.objects.filter(student=person).order_by('-id')
        return render(request,"searchedprofile.html",{'images': images,'person':person})
    else:
        return redirect(logins)

def pending(request):
    if request.user.is_staff == False and request.user.is_superuser == False:
        std=request.user
        pendingpost=Post_req.objects.filter(student=std)
        return render(request,"pending.html",{"images":pendingpost})
    else:
        return redirect(logins)


def delpost(request,pstid):
    post=college.objects.get(id=pstid)
    file_path = os.path.join(settings.MEDIA_ROOT, str(post.image))
    os.remove(file_path)
    post.delete()
    messages.success(request,"The Post was deleted successfully")
    return redirect('/adminn/')

def pdelpost(request,pstid,pid):
    post=college.objects.get(id=pstid)
    post.delete()
    return redirect('/profile/'+str(pid)+'/')

def signin(request):
    return render(request,"signin.html")

def delinbox(request,iid):
    inbox=Inbox.objects.get(id=iid)
    inbox.delete()
    messages.success(request,"The Inbox was deleted successfully")
    return redirect('/adminn/')

def pubpost(request):
    images=publics.objects.all()
    return render(request,'pub.html',{'images': images})

def pubdelpost(request,pstid):
    post=publics.objects.get(id=pstid)
    file_path = os.path.join(settings.MEDIA_ROOT, str(post.image))
    os.remove(file_path)
    post.delete()
    messages.success(request,"The Post was deleted successfully")
    return redirect('/adminn/pub')


