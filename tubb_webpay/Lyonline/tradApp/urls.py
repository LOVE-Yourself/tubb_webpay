from django.conf.urls import url

from .views import AlipayReturnView,NotyfileReturnView

urlpatterns = [

    # url(r'course_list/(?P<sort>\d+)$',Courselistview.as_view() ,name='courseList'),
    # url(r'payfor/$',payView.as_view(),name='payfor'),
    url(r'alipay_return/$',AlipayReturnView.as_view(),name='alipay_return'),
    url(r'notyfile_return/$',NotyfileReturnView.as_view(),name='notyfile_return'),
]

