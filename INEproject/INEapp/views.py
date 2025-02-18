from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from INEapp.form import FormSignin,FormSignup,FormIdea,FormEditUser,FormEditDatauser,Formsubidea
from INEapp.models import Idea,DataUser,SubIdea
from datetime import datetime,timezone,timedelta

# Create your views here.

def main(request):
    if request.method == 'POST':
        if request.POST.get('submit_signin') is not None: # Click Sign In
            try:
                email_user = User.objects.get(email=request.POST['username']).username
            except:
                return HttpResponse('''<h1 style="color: #ff0101; font-size: 30px;">Login failed !</h1>
                                    <p>This username or email does not exist. please check your username or email again.</p>
                                    <a href="/"><h3>back</h3></a>
                                    ''')
            user_login = authenticate(request=request,username=email_user,password=request.POST['password'])
            if user_login is not None:
                login(request,user_login) ; del user_login,email_user
                return redirect(f'/dashboard/{request.user}')
            else:
                return HttpResponse('''<h1 style="color: #ff0101; font-size: 30px;">Login failed !</h1>
                                    <p>This password does not exist. please check your password again.</p>
                                    <a href="/"><h3>back</h3></a>
                                    ''') 
        if request.POST.get('submit_signup') is not None:  # Click Sign Up
            form_signup = FormSignup(request.POST)
            username_all = User.objects.values('username','email')
            for name in username_all:
                if name.get('username') == request.POST['username']:
                    del form_signup,username_all
                    return HttpResponse('''<h1 style="color: #ff0101; font-size: 30px;">Sign Up faield !</h1>
                                        <p>This username is already in use.</p><a href="/"><h3>back</h3></a>
                                    ''')
                elif name.get('email') == request.POST['email']:
                    del form_signup,username_all
                    return HttpResponse('''<h1 style="color: #ff0101; font-size: 30px;">Sign Up faield !</h1>
                                        <p>This email is already in use.</p><a href="/"><h3>back</h3></a>
                                    ''')
                else:pass
            if form_signup.is_valid():
                username = form_signup.cleaned_data['username']
                email = form_signup.cleaned_data['email']
                password1 = form_signup.cleaned_data['password1']
                password2 = form_signup.cleaned_data['password2']
                if (password1 == password2) is not True:
                    del username,email,password1,password2,form_signup,username_all
                    return HttpResponse('''<h1 style="color: #ff0101; font-size: 30px;">Sign Up faield !</h1>
                                        <p>Password don't match. please check password again.</p><a href="/"><h3>back</h3></a>
                                    ''')
                else:
                    new_user = User.objects.create_user(username=username,email=email,password=password1)
                    new_user.save()
                    new_datauser = DataUser.objects.create(data_user=new_user)
                    new_datauser.save()
                    del username,email,password1,password2,form_signup,username_all,new_user,new_datauser
                    return HttpResponse('''<h1 style="color: #7bb589; font-size: 30px;">Sign Up Complete</h1>
                                        <p>You can login with your username.</p><a href="/"><h3>back</h3></a>
                                    ''')
            else:
                return HttpResponse('''<h1 style="color: #ff0101; font-size: 30px;">Sign Up failed !</h1>
                                        <p>please check information in signin up.</p><a href="/"><h3>back</h3></a>
                                    ''')
        else:
            return redirect('/')
    else:
        form = FormSignin()
        form2 = FormSignup()
        context = {'form':form,'form2':form2} ; del form,form2
        return render(request,'main.html',context)

@login_required(login_url='/')
def dashboard(request,name):
    if request.method == 'POST':
        if request.POST.get('btn_new_idea') is not None:
            user = User.objects.get(id=request.user.id)
            form_idea = FormIdea(request.POST)
            if form_idea.is_valid():
                if request.FILES.get('idea_image') is not None:
                    new_idea = Idea.objects.create(
                        idea_name=request.POST['idea_name'],
                        idea_description=request.POST['idea_description'],
                        idea_image=request.FILES['idea_image'],
                        key_user=user
                        )
                else:
                    new_idea = Idea.objects.create(
                        idea_name=request.POST['idea_name'],
                        idea_description=request.POST['idea_description'],
                        key_user=user
                        )
                new_idea.save() ; del new_idea,user
                return redirect(reverse('dashboard',kwargs={'name':name}))
            else:
                return HttpResponse('create new idea failed !')
    else:
        idea = FormIdea()
        user_idea = Idea.objects.filter(key_user = request.user)
        data_list = []
        idea_list = []
        method_complete_list = []
        project_complete_list = []
        count_method_complete = 0
        for list in user_idea:
            idea_list.append(f'P{list.id}')
            data_list.append(SubIdea.objects.filter(key_idea_id=list.id).count())
            for method in SubIdea.objects.filter(key_idea_id=list.id):
                if method.sub_complete is not None:
                    count_method_complete += 1
            if int(SubIdea.objects.filter(key_idea_id=list.id).count()) == 0:
                percen = 0
            else: 
                percen = float((int(count_method_complete) / int(SubIdea.objects.filter(key_idea_id=list.id).count())) * 100)
            method_complete_list.append(percen)
            count_method_complete = 0
        for check_complete in Idea.objects.filter(key_user_id=request.user.id):
            if check_complete.idea_complete is not None:
                count_method_complete += 1
        if int(Idea.objects.filter(key_user_id=request.user.id).count()) == 0:
            project_complete_list.append(0)
        else:
            project_complete_list.append(
                (int(count_method_complete) / int(Idea.objects.filter(key_user_id=request.user.id).count())) * 100
                )
            project_complete_list.append(
                100 - (int(count_method_complete) / int(Idea.objects.filter(key_user_id=request.user.id).count())) * 100
                ) 
        context = {
            'name':name,'form_idea':idea,
            'idea':user_idea,
            'list_idea':idea_list,
            'list_data':data_list,
            'complete_m':method_complete_list,
            'complete_p':project_complete_list
            }
        del name,idea,user_idea,idea_list,data_list,count_method_complete,project_complete_list
        return render(request,'dashboard.html',context)

@login_required(login_url='/')
def profile(request,name):
    if request.method == 'POST':
        if request.POST.get('btn-update') is not None: #start
            if request.FILES.get('image_profile') is not None:
                edit_image = DataUser.objects.get(data_user_id = request.user.id)
                edit_image.image_profile.delete()
                edit_image.image_profile = request.FILES['image_profile']
                edit_image.save() ; del edit_image
            else:pass
            edit_data = User.objects.get(id=request.user.id)
            edit_data.first_name = request.POST['first_name']
            edit_data.last_name = request.POST['last_name']
            edit_data.email = request.POST['email']
            edit_data.save() ; del edit_data
            return redirect(reverse('profile',kwargs={'name':name}))
        if request.POST.get('btn-back-to-dashboard') is not None: # beck
            return redirect(reverse('dashboard',kwargs={'name':name}))
    else:
        user = User.objects.get(username=request.user)
        data_image = DataUser.objects.get(data_user_id = request.user.id)
        data_user = FormEditUser(instance=user)
        form_image = FormEditDatauser()
        view_idea = Idea.objects.filter(key_user_id=request.user.id)
        context = {'name':name,'data':data_user,'form_img':form_image,'img':data_image,'idea':view_idea}
        del user,data_image,data_user,form_image,view_idea
        return render(request,'profile.html',context)

@login_required(login_url='/')
def idea(request,name,id):
    if request.method == 'POST':
        if request.POST.get('btn-start-project') is not None: #start
            status = request.POST.get('status_project')
            start_idea = Idea.objects.get(id=id)
            if status == 'private':
                start_idea.idea_status = True
            else:
                start_idea.idea_status = False
            start_idea.idea_start = True
            start_idea.save()
            del status,start_idea
            return redirect(reverse('idea',kwargs={'name':name,'id':id}))
        if request.POST.get('btn-delete-project') is not None: # delete
            return redirect(reverse('dashboard',kwargs={'name':name}))
        if request.POST.get('btn-new-subidea') is not None: # new method
            form_subidea = Formsubidea(request.POST,request.FILES)
            if form_subidea.is_valid():
                key = Idea.objects.get(id=id)
                idea = form_subidea.cleaned_data['sub_idea']
                body = form_subidea.cleaned_data['sub_body']
                image = None
                file = None
                if request.FILES.get('sub_image') is not None:
                    image = form_subidea.cleaned_data['sub_image']
                if request.FILES.get('sub_file') is not None:
                    file = form_subidea.cleaned_data['sub_file']
                else:pass
                new_method = SubIdea.objects.create(sub_idea=idea,sub_body=body,sub_image=image,sub_file=file,key_idea=key)
                new_method.save()
                del key,idea,body,image,file,form_subidea,new_method
                return redirect(reverse('idea',kwargs={'name':name,'id':id}))
            else:
                del form_subidea
                return HttpResponse('''<h1 style="color: #ff0101; font-size: 30px;">Create New Method failed !</h1>
                                        <p>please check information in form.</p><a href="{% url 'dashboard' name %}"><h3>dashboard</h3></a>
                                    ''')
        else:
            return redirect(reverse('idea',kwargs={'name':name,'id':id}))
    else:
        form_sub = Formsubidea()
        subidea = SubIdea.objects.filter(key_idea_id=id)
        image_profile = DataUser.objects.get(data_user_id=request.user.id)
        select_idea = Idea.objects.get(id=id)
        if select_idea.idea_complete is not None:
            count_day = int((datetime.date(select_idea.idea_complete) - datetime.date(select_idea.idea_datetime)).days)
        else:
            count_day = int((datetime.date(datetime.now()) - datetime.date(select_idea.idea_datetime)).days)
        context = {'name':name,'id':id,'idea':select_idea,'img':image_profile,'day_count':count_day,'form':form_sub,'sub':subidea}
        del select_idea,image_profile,count_day,form_sub,subidea
        return render(request,'idea.html',context)

@login_required(login_url='/')
def public(request,name):
    user_name = User.objects.values('id','username')
    image_profile = DataUser.objects.values('data_user_id','image_profile')
    public_idea = Idea.objects.values('id','key_user_id','idea_name','idea_datetime','idea_status','idea_start')
    if request.GET.get('search'):
        try:
            if request.GET.get('search')[0] == 'P':
                int(request.GET.get('search')[1:]) + 1
                search_idea_id = []
                search = Idea.objects.filter(id=request.GET.get('search')[1:])
                for value in search.values('id','key_user_id','idea_name','idea_datetime','idea_status','idea_start'):
                    if bool(list(value.values())[-1]) is True:
                        search_idea_id.append(value)
                public_idea = search_idea_id
                del search,search_idea_id
                context = {'name':name,'public':public_idea,'img':image_profile,'user':user_name} ; del public_idea,image_profile,user_name
                return render(request,'public.html',context)
            elif request.GET.get('search')[0] == '@':
                username_id = []
                search_username = []
                user_all = User.objects.values('id','username')
                for names in user_all:
                    if str(list(names.values())[-1]).find(request.GET.get('search')[1:]) is not int(-1):
                        username_id.append(list(names.values())[0])
                    else:pass
                for value in Idea.objects.all():
                    for id_user in username_id:
                        if value.key_user_id == id_user and value.idea_start == True:
                            search_username.append(value)
                        else:pass
                public_idea = search_username
                del user_all,username_id,search_username
                context = {'name':name,'public':public_idea,'img':image_profile,'user':user_name} ; del public_idea,image_profile,user_name
                return render(request,'public.html',context)
            else:pass
            int(request.GET.get('search')) + 1
            search_id = []
            search = Idea.objects.filter(key_user_id=request.GET.get('search'))
            for value in search.values('id','key_user_id','idea_name','idea_datetime','idea_status','idea_start'):
                if bool(list(value.values())[-1]) is True:
                    search_id.append(value)
                else:pass
            public_idea = search_id ; del search,search_id
        except:
            search = []
            idea_all = Idea.objects.values('id','key_user_id','idea_name','idea_datetime','idea_status','idea_start')
            for value in idea_all:
                if str(list(value.values())[2]).find(request.GET.get('search')) is not int(-1):
                    if bool(list(value.values())[-1]) is True:
                        search.append(value)
                    else:pass
                else:pass
            public_idea = search
            del idea_all,search
    else:pass
    context = {'name':name,'public':public_idea,'img':image_profile,'user':user_name} ; del public_idea,image_profile,user_name
    return render(request,'public.html',context)

@login_required(login_url='/')
def view_project(request,pk):
    sub_idea = SubIdea.objects.filter(key_idea_id=pk)
    view_idea = get_object_or_404(Idea,id=pk)
    user = User.objects.get(id=view_idea.key_user_id)
    img = DataUser.objects.get(data_user_id=user.id)
    context = {'view':view_idea,'user':user,'img':img,'name':request.user,'sub':sub_idea}
    if view_idea.idea_complete is not None:
        context.update({'project_day': int((datetime.date(view_idea.idea_complete) - datetime.date(view_idea.idea_datetime)).days)})
    else:pass
    del view_idea,user,img,sub_idea
    return render(request,'view.html',context)

@login_required(login_url='/')
def owner(request,pk):
    owner_idea = get_object_or_404(Idea,id=pk)
    owner = User.objects.get(id=owner_idea.key_user_id)
    data = DataUser.objects.get(data_user_id=owner.id)
    context = {'name':request.user,'owner':owner,'data':data,'pk':pk} ; del owner_idea,owner,data
    return render(request,'owner.html',context)

@login_required(login_url='/')
def good(request,pk):
    good_idea = get_object_or_404(Idea,id=pk)
    if good_idea.idea_good.filter(id=request.user.id):
        good_idea.idea_good.remove(request.user)
    else:
        good_idea.idea_good.add(request.user)
    del good_idea
    return redirect(reverse('view',kwargs={'pk':pk}))

@login_required(login_url='/')
def following(request,pk):
    owner = User.objects.get(id=pk)
    data = DataUser.objects.get(data_user_id=pk)
    context = {'name':request.user,'owner':owner,'data':data,'pk':pk} ; del owner,data
    return render(request,'following.html',context)

# follow in owner page
@login_required(login_url='/')
def follow(request,pk):
    is_idea = get_object_or_404(Idea,id=pk)
    follow_user = User.objects.get(id=is_idea.key_user_id)
    name_user_follow = DataUser.objects.get(data_user_id=follow_user.id)
    if name_user_follow.following.filter(id=request.user.id):
        name_user_follow.following.remove(request.user)
    else:
        name_user_follow.following.add(request.user)
    del is_idea,follow_user,name_user_follow
    return redirect(reverse('owner',kwargs={'pk':pk}))

# follow in profile page
@login_required(login_url='/')
def folloW(request,pk):
    follow_user = User.objects.get(id=pk)
    name_user_follow = DataUser.objects.get(data_user_id=pk)
    if name_user_follow.following.filter(id=request.user.id):
        name_user_follow.following.remove(request.user)
    else:
        name_user_follow.following.add(request.user)
    del follow_user,name_user_follow
    return redirect(reverse('following',kwargs={'pk':pk}))

@login_required(login_url='/')
def delete(request,pk):
    delete_idea = Idea.objects.get(id=pk)
    delete_sub = SubIdea.objects.filter(key_idea_id=pk)
    if delete_idea.idea_image is not None:
        delete_idea.idea_image.delete()
    else:pass
    for data_sub in delete_sub:
        if data_sub.sub_image is not None:
            data_sub.sub_image.delete()
        if data_sub.sub_file is not None:
            data_sub.sub_file.delete()
        else:pass
    delete_idea.delete() ; del delete_idea
    return redirect(reverse('dashboard',kwargs={'name':request.user}))

def idea_complete(request,name,id):
    complete_idea = Idea.objects.get(id=id)
    method_idea = SubIdea.objects.filter(key_idea_id=id)
    for method in method_idea:
        if method.sub_complete is not None:
            pass
        else:
            del complete_idea,method_idea
            return HttpResponse(f'''<h1 style="color: #ff0101; font-size: 30px;">failed !</h1>
                                        <p>method : M{method.id} is not complete.</p><a href="/dashboard/{name}/idea/{id}/"><h3>Back</h3></a>
                                    ''')
    complete_idea.idea_complete = datetime.now(tz=timezone(timedelta(hours=7)))
    complete_idea.save()
    del complete_idea,method_idea
    return redirect(reverse('idea',kwargs={'name':name,'id':id}))

def method_complete(request,name,id,pk):
    sub_idea_complete = SubIdea.objects.get(id=pk)
    sub_idea_complete.sub_complete = datetime.now(tz=timezone(timedelta(hours=7)))
    sub_idea_complete.save() ; del sub_idea_complete
    return redirect(reverse('idea',kwargs={'name':name,'id':id}))

def user_logout(request):
    logout(request)
    return redirect('/')
   
