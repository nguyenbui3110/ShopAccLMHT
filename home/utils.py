from posixpath import split
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from matplotlib.pyplot import pink

def convertVND(price):
    price = int(price)
    formatted_number = "{:,}".format(price)
    return formatted_number

def checkPay(price, money):
    money = money - price
    if(money >= 0):
        return money
    else:
        return False

def sendAcc(emailacc, username, password):
    try:
        subject = 'LoLShop.com - Thông tin mua tài khoản !'
        message = 'Chào bạn! Bạn đã hoàn tất quá trình mua tài khoản và thanh toán tại LoLShop.com. \nTài khoản:  ' + username + '\nMật khẩu: ' + password + '\nCảm ơn bạn đã tin tưởng và ủng hộ chúng tôi!'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [emailacc,]
        print(emailacc)
        if (send_mail(subject, message, 'LoLShop.Com ' + email_from, recipient_list, fail_silently=False)):
            return True
        else:
            return False
    except:
        return False

def convertPrice(acc):
    for i in range(len(acc)):
        acc[i].price = convertVND(acc[i].price)
        acc[i].sale = convertVND(acc[i].sale)
    return acc


def sendMess(email, fullname, mess):
    try:
        subject = 'LoLShop.com - Tin nhắn khách hàng!'
        message = 'Khách hàng: ' + fullname + '\nEmail: ' + email + '\nTin nhắn: ' + mess
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['nguyenbui31102002@gmail.com',]
        if (send_mail(subject, message, 'LoLShop.Com ' + email_from, recipient_list, fail_silently=False)):
            return True
        else:
            return False
    except:
        print()
        return False