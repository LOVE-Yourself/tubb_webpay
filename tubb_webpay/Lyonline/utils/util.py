import random
from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from Lyonline.settings import EMAIL_FROM

def send_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    email_record.email = email
    code = random_str(16)
    email_record.send_type = send_type
    email_record.code = code
    email_record.save()
    if send_type == 'register':
        email_title = '乐创教育注册激活链接'
        email_body = '请点击链接激活你的账号http://192.168.192.130:8000/users/active/{0}/'.format(code)
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            print('--状态-->', email_body)
    elif send_type == 'forget':
        print('????????')
        email_title = '乐创教育修改密码链接'
        email_body = '请点击链接休修改密码http://192.168.192.130:8000/users/changepwd/{0}/'.format(code)
        # email_body = '求求你了让我通过把'
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            print('--状态-->',email_body)
            pass
        else:
            print('-->',send_status)
def random_str(random_length):
    str = ''
    chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    length = len(chars) -1
    random1 = random.Random()
    for i in range(random_length):
        str += chars[random1.randint(0,length)]
    return str

