from django.shortcuts import render,HttpResponse
from django.views.generic import View
from operation.models import UserCourse,UserFavorrate,CourseComments
from django.db.models import Q
from .models import Course

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

class Courselistview(View):
    def get(self,request):
        search_key = request.GET.get('keywords')

        sort = request.GET.get('sort','')
        print('--->type-->',sort)
        if sort == '':
            courses_list = Course.objects.order_by('-add_time')
            if search_key:
                courses_list = courses_list.filter(Q(name__icontains=search_key)|Q(desc__icontains=search_key)|Q(detail__icontains=search_key))
        elif sort == 'hot':
            courses_list = Course.objects.order_by('click_nums')
        elif sort == 'students':
            courses_list = Course.objects.order_by('students')

        try:
            page = request.GET.get('page', 1)

        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(courses_list, 3,request=request)

        courses = p.page(page)
        print('--->>????')
        return render(request,'course-list.html',{'courses_list':courses,'sort':sort})

class CourseDetailView(View):
    def get(self,request,course_id):
        print('------suanl ba ---->',course_id)
        course = Course.objects.get(id=course_id)
        lesson_count = course.lesson_set.all()#章节数

        #相关推荐
        tag = course.tag
        if tag:
            course_relate = Course.objects.filter(tag=tag)
        else:
            course_relate = []
        #判断用户状态
        org_has_fav = False
        course_has_fav= False

        # if request.user.is_authenticated():
        #     if UserFavorrate.objects.filter(user=request.user,fav_id=course.id,fac_type=1):
        #         course_has_fav = True
        #     if UserFavorrate.objects.filter(user=request.user,fav_id=course.org.id,fac_type=2):
        #         org_has_fav = True
        return render(request,'course-detail.html',{'course':course,
                                                    'lesson_count':lesson_count,
                                                    'course_relate':course_relate,
                                                    'course_has_fav':course_has_fav,

                                                    'org_has_fav':org_has_fav})

from tradApp.models import Coach_Orders
from utils.alipay import AliPay
from Lyonline.settings import private_key_path,ali_pub_key_path
from datetime import datetime



def get_alipayUrl(order_no,pay_mount):
    alipay = AliPay(
        appid="2016091100490098",
        app_notify_url="http://192.168.192.131:8000/pay/notyfile_return/",
        app_private_key_path=private_key_path,
        alipay_public_key_path=ali_pub_key_path,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        debug=True,  # 默认False,
        return_url="http://192.168.192.131:8000/pay/alipay_return/"
    )
    url = alipay.direct_pay(
        subject="测试订单2",
        out_trade_no=order_no,
        total_amount=pay_mount,
        return_url="http://192.168.192.131:8000/pay/alipay_return/"

    )
    re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
    return re_url


class CourseInfoView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=course_id)
        user = request.user

        #学过该课程的其他同学 还学过什么
        other_course_list = []
        usercourse_list = UserCourse.objects.filter(course=course)[:3]

        for usercourse in usercourse_list:
            u = usercourse.user
            user_course = UserCourse.objects.filter(user=u)[:1][0]

            other_course_list.append(user_course.course)
        #系统生成订单 和支付的url  随机订单号
        # request.post('username','') 正常获取
        # 现在是get  后来要改成  post
        coachOrder = Coach_Orders()

        coachOrder.order_sn = '20150320010101006'
        coachOrder.course_name = 'c1过弯基础课程'
        coachOrder.username = '徐璟灏'
        coachOrder.order_mount = '4650'
        coachOrder.coach_name = '汪鹏'
        coachOrder.pay_type = 'aplipay'
        coachOrder.pay_mount = '4500'
        coachOrder.order_status = 'WAIT_BUYER_PAY'
        print('---->??????????')
        coachOrder.save()
        alipayUrl = get_alipayUrl(coachOrder.order_sn,coachOrder.pay_mount)
        return render(request,'course-video.html',{'course':course,'other_course_list':other_course_list,'coach_order':coachOrder,'alipay_url':alipayUrl})


class CourseCommentView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=course_id)
        return render(request,'course-comment.html',{'course':course})


class AddCommentView(View):
    def post(self,request):
        print('---->添加评论')
        if not request.user.is_authenticated:

            return HttpResponse("{'status':'fail','msg':'用户未登录'}",content_type='application/json')

        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')
        print('真的是你吗----》',comments)
        if int(course_id) >0 and comments:
            course = Course.objects.get(id=int(course_id))
            course_comment = CourseComments()
            course_comment.course = course
            course_comment.comments = comments
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse("{'status':'success','msg':'添加成功'}",content_type='application/json')
        else:
            return HttpResponse("{'status':'fail','msg':'添加失败'}",content_type='application/json')


