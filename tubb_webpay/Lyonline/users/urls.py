from django.conf.urls import url

from .views import LoginView,RegistView,ActiveEmail,ForgetView,ChangepwdEmail,AginChange,UserInfoView,UserUploadImageView,UserUploadPwd

urlpatterns = [

    url(r'login/$',LoginView.as_view() ,name='login'),
    url(r'register/$',RegistView.as_view(),name='register'),
    url(r'active/(?P<active_code>.*)/$',ActiveEmail.as_view(),name='active'),
    url(r'forgetpwd/$',ForgetView.as_view(),name='forgetpwd'),
    url(r'changepwd/(?P<change_code>.*)$',ChangepwdEmail.as_view(),name='change_pwd'),
    url(r'changeagin/',AginChange.as_view(),name='change_agin'),

    url(r'user_info/',UserInfoView.as_view(),name='user_info'),
    url(r'user_upload_image/',UserUploadImageView.as_view(),name='upload_image'),
    url(r'update/pwd/',UserUploadPwd.as_view(),name='upload_pwd'),

]