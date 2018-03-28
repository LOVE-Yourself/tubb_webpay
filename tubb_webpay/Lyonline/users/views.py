from django.contrib.auth import authenticate, login, hashers
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render,HttpResponse
from django.views.generic import View
from django.contrib.auth.hashers import make_password
import json
from  utils.util import send_email
from .forms import LoginForm, RegisterForm,ForgetForm,ChangeForm,UploadImageForm
from .models import UserProfile,EmailVerifyRecord


# Create your views here.

#
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username)|Q(nick_name=username))
            if user.check_password(password):
                return user
            return None

        except Exception as e :
            print(e)
            return None

#点击邮箱链接激活
class ActiveEmail(View):
    def get(self,request,active_code):

        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, 'login.html', )
        return render(request,'active.html')

#忘记密码
class ForgetView(View):
    def get(self,request):
        forget_form = ForgetForm()

        return render(request,'forgetpwd.html',{'forget_form':forget_form})
    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email','')
            try:
                user = UserProfile.objects.get(email=email)
            except:
                return render(request,'forgetpwd.html',{'forget_form':forget_form,'msg':'账号不存在'})


            send_email(email,send_type='forget')
            return render(request,'success.html')
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

#修改密码
class ChangepwdEmail(View):
    def get(self,request,change_code):
        c = change_code.strip('/')
        print(change_code)
        all_record = EmailVerifyRecord.objects.filter(code=c)
        print('????->',all_record)
        if all_record:
            for record in all_record:
                email = record.email
                #user = UserProfile.objects.get(email=email)
                return render(request,'password_reset.html',{'email':email})
        return render(request,'active.html')


class AginChange(View):
    def post(self,request):
        print('???????????????????')
        email = request.POST.get('email')
        print('------->',email)
        # return render(request,'login.html')
        user = UserProfile.objects.get(email=email)
        change_form = ChangeForm(request.POST)
        if change_form.is_valid():
            new_pwd = request.POST.get('password','')
            reset_pwd= request.POST.get('password2','')
            if new_pwd == reset_pwd:

                user.password = make_password(new_pwd)

                user.save()
                return render(request,'login.html')
            else:
                return render(request,'password_reset.html',{'email':email,'msg':'前后密码不一致'})
        return render(request,'password_reset.html',{'change_form':change_form,'email':email})

class LoginView(View):
    def get(self,request):
        return render(request,'login.html',{})
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username','')
            password = request.POST.get('password','')
            user = authenticate(username = username,password = password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return render(request,'index.html')
                return render(request,'login.html',{'msg':'用户未激活'})
            else:
                return render(request,'login.html',{'msg':'用户名或密码错误'})
        return render(request,'login.html',{'login_form':login_form})

class RegistView(View):

    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'RegisterForm':register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        print('------->1')

        if register_form.is_valid():
            username = request.POST.get('email','')
            email = request.POST.get('email','')
            try:
                user = UserProfile.objects.get(email=email)
                if user:
                    return render(request, 'register.html', {'RegisterForm':register_form,'msg': '该邮箱已注册过'})
            except:
                print('可以注册')

            password = request.POST.get('password','')
            pwd = hashers.make_password(password)
            user = UserProfile()
            user.username = username
            user.email = email
            user.password = pwd
            user.is_active = False
            user.save()
            print('-------->2')
            send_email(email,send_type='register')
            return render(request,'login.html')

        return render(request,'register.html',{'RegisterForm':register_form})
#------------个人详情页------------------------------------------------------------------------>>>>>>>>>>>>>>



class UserInfoView(View):
    def get(self,request):
        if not request.user.is_authenticated():
            return render(request,'login.html')
        return render(request,'usercenter-info.html')



class UserUploadImageView(View):
    def post(self,request):
        print('lail吗 小伙子--->')
        uploadForm = UploadImageForm(request.POST,request.FILES)
        print('lail吗 小伙子--->')
        if uploadForm.is_valid():
            request.user.image = uploadForm.cleaned_data['image']
            request.user.save()
            print('成功了  我想你 ')
            return HttpResponse("{'status':'success'}",content_type='application/json')


        return HttpResponse("{'status':'fail'}",content_type='application/json')

class UserUploadPwd(View):
    def post(self,request):


        # if not request.user.is_authenticated():
        #     return render(request,'login.html')

        user = request.user
        change_form = ChangeForm(request.POST)
        if change_form.is_valid():
            print('-->user', request.user)
            new_pwd = request.POST.get('password','')
            reset_pwd= request.POST.get('password2','')
            if new_pwd == reset_pwd:

                print('------>pwd',user.password)
                user.password = make_password(new_pwd)
                print('------------------->yuntoy ')
                user.save()
                print('充公了吗？？？？//复杂化了把')

                return HttpResponse("{'status':'success'}", content_type='application/json')
            else:
                return HttpResponse("{'status':'fail','msg':'前后密码不一致'}",content_type='application/json')

        return HttpResponse(json.dumps(change_form.errors), content_type='application/json')

from django.shortcuts import render_to_response
def page_not_found(request):
    response = render_to_response('404.html',{})
    response.status_code =404
    return response
# class page_not_found(View):
#     print('lail---------------->')
#     def get(self,request):
#          return render(request,'404.html')


