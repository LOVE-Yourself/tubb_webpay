from django.shortcuts import render
# Create your views here.
import json

from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View

from .forms import CoachOrdersForm
from .models import Coach_Orders

# class payView(View):
#     def get(self,request):
#         resp = {'errorcode': 100, 'detail': 'Get success'}
#         #生成 订单 并展示订单信息
#         return HttpResponse(json.dumps(resp), content_type="application/json")
#
#     def get_alipay(self):
#         alipay = AliPay(
#             appid="2016091100490098",
#             app_notify_url="http://192.168.192.131:8000/pay/notyfile_return/",
#             app_private_key_path=private_key_path,
#             alipay_public_key_path=ali_pub_key_path,
#             # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
#             debug=True,  # 默认False,
#             return_url="http://192.168.192.131:8000/pay/alipay_return/"
#         )
#
#         return alipay
#
#     def post(self,request):
#         #将信息提交 到支付宝
#         #订单号 自己生成 order_sn
#         #
#         Orderform = CoachOrdersForm(request.POST)
#         if Orderform.is_valid():
#             order_sn = request.POST.get('order_sn','')
#             username = request.POST.get('username','')
#             order_mount = request.POST.get('order_mount','')
#             coach_name = request.POST.get('coach_name','')
#             pay_type = request.POST.get('pay_type','')
#             pay_mount = request.POST.get('pay_mount','')
#             #order_status = request.POST.get('order_status','')
#             #add_time = request.POST.get('add_time','')
#             coachOrder = Coach_Orders()
#
#             coachOrder.order_sn = order_sn
#             coachOrder.username = username
#             coachOrder.order_mount = order_mount
#             coachOrder.coach_name = coach_name
#             coachOrder.pay_type = pay_type
#             coachOrder.pay_mount = pay_mount
#             coachOrder.order_status = 'WAIT_BUYER_PAY'
#
#             print('---->??????????')
#             # coachOrder.order_status = order_status
#             # coachOrder.add_time = add_time
#             coachOrder.save()
#             #重定向到新的支付界面
#             alipay = self.get_alipay()
#             url = alipay.direct_pay(
#                 subject="测试订单2",
#                 out_trade_no="20170202172",
#                 total_amount=1.00,
#                 return_url="http://192.168.192.131:8000/pay/alipay_return/"
#
#             )
#             re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
#             return redirect()
#         else:
#             resp = {'errorcode': 404, 'detail': 'POST Get files'}
#         return HttpResponse(json.dumps(resp),content_type='application/json')


from urllib.parse import urlparse, parse_qs
from utils.alipay import AliPay
from Lyonline.settings import private_key_path,ali_pub_key_path
from datetime import datetime

from users.models import UserProfile
from driverSchool.models import Coach
#对返回来的url进行验证加密  防止别人伪造你的请求
class AlipayReturnView(View):
    def get(self,request):
        alipay = AliPay(
            appid="2016091100490098",
            app_notify_url="http://192.168.192.131:8000/pay/notyfile_return/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_pub_key_path,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://192.168.192.131:8000/pay/alipay_return/"
        )
        #sss = request.GET.get('trade_no','')
        #支付成功 跳转回来
        o = urlparse(request.get_full_path())
        query = parse_qs(o.query)
        processed_query = {}
        ali_sign = query.pop("sign")[0]
        for key, value in query.items():
            print('---??---->',key)
            processed_query[key] = value[0]
        s = alipay.verify(processed_query,ali_sign)#比对跳转回来的信息参数与之前发过去的信息参数（加密的sign）
        if s:
            #获取数据库里的记录
            trade_no = processed_query['trade_no']
            # order_status = processed_query['trade_status']
            order_status = 'TRADE_SUCCESS'
            order_sn = processed_query['out_trade_no']
            coachOrders = Coach_Orders.objects.filter(order_sn=order_sn)
            for coachOrder in coachOrders:
                coachOrder.trade_no = trade_no
                coachOrder.order_status = order_status
                coachOrder.pay_time = datetime.now()
                coachOrder.save()
                users = UserProfile.objects.filter(Coach_Orders_id=coachOrder.id)
                for user in users:
                    user.order_name = coachOrder.coach_name
                    user.save()
                #改变教练的学生人数
                coachs = Coach.objects.filter(name=coachOrder.coach_name)
                for coach in coachs:
                    coach.students += 1
                    coach.save()
            resp = 'success'
        else:
            resp = {'code': 500, 'detail': 'postchengg'}

        #更改用户表教练名称

        return HttpResponse(json.dumps(resp),content_type='application/json')


    def post(self,request):
        resp = {'code':300,'detail':'postchengg'}

        print('------------------------------?>>>>>>>>>>>>')
        #支付成功 跳转回来
        return HttpResponse(json.dumps(resp),content_type='application/json')

class NotyfileReturnView(View):
    def get(self):
        resp = {'code':666,'detail':'postchengg'}
        print('---------------get---------------?>>>>>>>>>>>>')
        #支付成功 跳转回来
        return HttpResponse(json.dumps(resp),content_type='application/json')


    def post(self,request):
        resp = {'code':333,'detail':'postchengg'}
        print('--------------post----------------?>>>>>>>>>>>>')
        #支付成功 跳转回来
        return HttpResponse(json.dumps(resp),content_type='application/json')