from unittest import result
from urllib import request
from django.shortcuts import redirect, render
from django.http import HttpResponse
from numpy import product
from home.utils import checkPay, convertPrice, convertVND, sendAcc, sendMess
from .models import AccCategory, AccGame, AccCategory
from user.models import Profile, ShopCart
from django.views import View
from django.contrib.auth.models import User

# Create your views here.
def GetAccAndCategory():
    allacc = AccGame.objects.all().filter(product=True)
    newacc = AccGame.objects.all().filter(product=True).order_by('-id')[:11]
    category = AccCategory.objects.all()
    allacc = convertPrice(allacc)
    newacc = convertPrice(newacc) 
    return {'allacc':allacc, 'newacc':newacc, 'category':category}

class index(View):
    template_name =  'home/index.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:     
            result = GetAccAndCategory()
            return render(request,self.template_name, result)

class home(View):
    template_name =  'home/home.html'
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('index')
        else:
            result = GetAccAndCategory()
            user = User.objects.all().get(pk=request.user.id)
            cart = ShopCart.objects.all().filter(user = user).count()
            money = Profile.objects.all().get(user = user).money
            money = convertVND(money)
            result.update({'username': request.user.username, 'money': money, 'cart':cart})
            return render(request,self.template_name, result)
        
class detail(View):
    template_name =  'home/detail.html'
    def get(self, request, slug):
        acc = AccGame.objects.all().get(slug=slug)
        price = convertVND(acc.price)
        sale = convertVND(acc.sale)
        cate = AccCategory.objects.all().get(accgame = acc)
        if request.user.is_authenticated:
            user = User.objects.all().get(pk=request.user.id)
            cart = ShopCart.objects.all().filter(user = user).count()
            money = Profile.objects.all().get(user = user).money
            money = convertVND(money)
            if(acc.product == False):
                return redirect('home')
            else:
                result = {'login' : True, 'username': request.user.username, 'money': money, 'acc':acc, 'price': price, 'sale':sale, 'cate':cate, 'cart':cart}
                return render(request,self.template_name,result)
        else:
            if(acc.product == False):
                return redirect('home')
            else:
                result = {'login' : False, 'acc':acc, 'price': price, 'sale':sale, 'cate':cate}
                return render(request,self.template_name,result)
class category(View):
    template_name =  'home/category.html'
    def get(self, request, slug):
        allCate = AccCategory.objects.all()
        cate = AccCategory.objects.all().get(slug=slug)
        acc = AccGame.objects.all().filter(category=cate)
        acc = convertPrice(acc)
        if request.user.is_authenticated:
            user = User.objects.all().get(pk=request.user.id)
            cart = ShopCart.objects.all().filter(user = user).count()
            money = Profile.objects.all().get(user = user).money
            money = convertVND(money)
            result = {'login' : True, 'username': request.user.username, 'money': money,'acc':acc, 'cate':cate, 'allCate':allCate, 'cart':cart }
            return render(request,self.template_name,result)
        else:
            result = {'login' : False, 'username': request.user.username, 'acc':acc, 'cate':cate, 'allCate':allCate, }
            return render(request,self.template_name,result)

class pay(View):
    template_name =  'home/pay.html'
    def get(self, request, slug):
        if request.user.is_authenticated:
            acc = AccGame.objects.all().get(slug=slug)
            user = User.objects.all().get(pk=request.user.id)
            cart = ShopCart.objects.all().filter(user = user).count()
            money = Profile.objects.all().get(user = user).money
            price = convertVND(acc.price)
            money = convertVND(money)
            if(acc.product == False):
                return redirect('home')
            else:
                result = {'login' : True, 'username': request.user.username, 'money': money, 'acc':acc, 'price': price, 'cart':cart}
                return render(request,self.template_name,result)
        else:
            return redirect('user-login')

    def post(self, request,slug):
        if request.user.is_authenticated:
            if request.method == 'POST':
                emailacc = request.POST["emailacc"]
                acc = AccGame.objects.all().get(slug=slug)
                user = User.objects.all().get(pk=request.user.id)
                money = Profile.objects.all().get(user = user).money
                price = acc.price
                newMoney = checkPay(price,money)
                if acc.product == False:
                    user = User.objects.all().get(pk=request.user.id)
                    money = Profile.objects.all().get(user = user).money
                    price = convertVND(acc.price)
                    money = convertVND(money)
                    error = "Tài khoản đã được mua, vui lòng mua tài khoản khác!"
                    cart = ShopCart.objects.all().filter(user = user).count()
                    result = {'login' : True, 'username': request.user.username, 'money': money, 'acc':acc, 'price': price, 'error':error, 'cart':cart}
                    return render(request,self.template_name,result)

                if (newMoney == False):
                    user = User.objects.all().get(pk=request.user.id)
                    money = Profile.objects.all().get(user = user).money
                    acc = AccGame.objects.all().get(slug=slug)
                    price = convertVND(acc.price)
                    money = convertVND(money)
                    error = "Số dư không đủ, vui lòng nạp thêm tiền!"
                    cart = ShopCart.objects.all().filter(user = user).count()
                    result = {'login' : True, 'username': request.user.username, 'money': money, 'acc':acc, 'price': price, 'error':error, 'cart':cart}
                    return render(request,self.template_name,result)
                else:
                    if(sendAcc(emailacc, acc.username, acc.password) == True):
                        user = User.objects.all().get(pk=request.user.id)
                        money = Profile.objects.all().get(user = user).money
                        acc = AccGame.objects.all().get(slug=slug)
                        price = convertVND(acc.price)
                        updateMoney = Profile.objects.all().get(user = user)
                        updateMoney.money = newMoney
                        updateMoney.save()
                        newMoney = convertVND(newMoney)
                        acc.product = False
                        acc.save()
                        try:
                            ShopCart.objects.all().get(user=user, product = acc).delete()
                        finally:
                            cart = ShopCart.objects.all().filter(user = user).count()
                            error = "Mua tài khoản thành công, vui lòng kiểm tra email để nhận tài khoản!"
                            result = {'login' : True, 'username': request.user.username, 'money': newMoney, 'acc':acc, 'price': price, 'error':error, 'cart':cart}
                            return render(request,self.template_name,result)
                    else:
                        user = User.objects.all().get(pk=request.user.id)
                        money = Profile.objects.all().get(user = user).money
                        acc = AccGame.objects.all().get(slug=slug)
                        cart = ShopCart.objects.all().filter(user = user).count()
                        price = convertVND(acc.price)
                        money = convertVND(money)
                        error = "Vui lòng nhập vào email hợp lệ! Ví dụ: nguyenvana@gmail.com!"
                        result = {'login' : True, 'username': request.user.username, 'money': money, 'acc':acc, 'price': price, 'error':error,'cart':cart}
                        return render(request,self.template_name,result)

            else:
                user = User.objects.all().get(pk=request.user.id)
                money = Profile.objects.all().get(user = user).money
                acc = AccGame.objects.all().get(slug=slug)
                price = convertVND(acc.price)
                result = {'login' : True, 'username': request.user.username, 'money': money, 'acc':acc, 'price': price}
                return render(request,self.template_name,result)
        else:
            return redirect('user-login')
class contact(View):
    template_name = 'home/contact.html'
    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.all().get(pk=request.user.id)
            money = Profile.objects.all().get(user = user).money
            cart = ShopCart.objects.all().filter(user = user).count()
            money = convertVND(money)
            result = {'login' : True, 'username': request.user.username, 'money': money, 'cart':cart }
            return render(request,self.template_name,result)
        else:
            result = {'login' : False}
            return render(request,self.template_name,result)
    def post(self, request):
        fullname = request.POST['fullname']
        email = request.POST['email']
        mess = request.POST['mess']
        if request.user.is_authenticated:
            if(sendMess(email, fullname, mess) == True):
                error = 'Cảm ơn bạn đã liên hệ với chúng tôi! Chúng tôi sẽ cố gắng trả lời bạn sớm nhất!'
                user = User.objects.all().get(pk=request.user.id)
                money = Profile.objects.all().get(user = user).money
                cart = ShopCart.objects.all().filter(user = user).count()
                money = convertVND(money)
                result = {'login' : True, 'username': request.user.username, 'money': money, 'cart':cart, 'error':error}
                return render(request,self.template_name,result)
            else:
                error = 'Vui lòng nhập email hợp lệ!'
                user = User.objects.all().get(pk=request.user.id)
                money = Profile.objects.all().get(user = user).money
                cart = ShopCart.objects.all().filter(user = user).count()
                money = convertVND(money)
                result = {'login' : True, 'username': request.user.username, 'money': money, 'cart':cart, 'error':error}
                return render(request,self.template_name,result)
        else:
            if(sendMess(email, fullname, mess) == True):
                error = 'Cảm ơn bạn đã liên hệ với chúng tôi! Chúng tôi sẽ cố gắng trả lời bạn sớm nhất!'
                result = {'login' : False,'error':error}
                return render(request,self.template_name,result)
            else:
                error = 'Vui lòng nhập email hợp lệ!'
                result = {'login' : False, 'error':error}
                return render(request,self.template_name,result)
def handler500(request):
    return render(request, '500.html', status=500)
def handler404(request, exception):
    return render(request, '404.html', status=404)

