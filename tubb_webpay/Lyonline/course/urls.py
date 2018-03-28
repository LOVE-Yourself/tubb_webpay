from django.conf.urls import url

from .views import Courselistview,CourseDetailView,CourseInfoView,CourseCommentView,AddCommentView

urlpatterns = [

    # url(r'course_list/(?P<sort>\d+)$',Courselistview.as_view() ,name='courseList'),
    url(r'course_list/$',Courselistview.as_view() ,name='courseList'),
    url(r'course_detail/(?P<course_id>\d+)$',CourseDetailView.as_view() ,name='course_detail'),
    url(r'course_info/(?P<course_id>\d+)$', CourseInfoView.as_view(), name='course_info'),
    url(r'course_comment/(?P<course_id>\d+)$',CourseCommentView.as_view(),name='course_comment'),
    url(r'add_comment/$',AddCommentView.as_view(),name='add_comment'),

]