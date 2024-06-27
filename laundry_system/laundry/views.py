from audioop import reverse
import email
from multiprocessing import context
from unicodedata import category
from urllib import request
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import LaundryUser, LaundryshopeUser, Laundrytype, Order_details
from django.contrib.auth.hashers import make_password, check_password
from .forms import userlogin, Signup, lundey_user, lundey_cat, profile,oderformforupdate,shopform
from django.contrib.auth import authenticate, login, logout
import razorpay
from laundry_system.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
# Create your views here.


def user_login(request):
    fm = userlogin(request.POST or None)
    if fm.is_valid():
        email = fm.cleaned_data.get("email")
        request.session['userkey'] = email
        return redirect("/")
    return render(request, 'login.html', {'form': fm})


def home(request):
    if 'userkey' in request.session:
        user = LaundryUser.objects.get(email=request.session["userkey"])
        if user.user_type == "customer":
            shop_data = LaundryshopeUser.objects.all()

            context = {
                "shop_data": shop_data,
                "user": user
            }
            return render(request, "home.html", context)
        if user.user_type == "laundry_shop_user":
            return redirect("/laundry/")
        if user.user_type == "admin":
            return redirect("/admin/")

        return render(request, "home.html")
    return redirect("/login/")


def register_user(request):

    fm = Signup(request.POST or None)
    if fm.is_valid():
        sel = fm.save(commit=False)
        p = fm.cleaned_data.get('password')
        encp = make_password(p)
        sel.password = encp
        img = request.FILES.get("img")
        sel.img = img
        sel.save()
        return redirect("/login/")
    return render(request, 'register.html', {'form': fm})


def user_logout(request):
    if 'userkey' in request.session:
        del request.session['userkey']
        logout(request)
    return redirect("/login/")


def launder_user(request):
    if 'userkey' in request.session:
        user = LaundryUser.objects.get(email=request.session["userkey"])
        user_type = "laundry_shop_user"
        try:
            LaundryshopeUser.objects.get(
                name__email=request.session["userkey"])
        except:
            fm = lundey_user()
            if request.method == "POST":
                if fm.is_valid:
                    m = LaundryshopeUser()
                    m.name = LaundryUser.objects.get(
                        email=request.session["userkey"])
                    m.shop_address = request.POST.get("shop_address")
                    m.shop_name = request.POST.get("shop_name")
                    m.shop_img = request.FILES.get("shop_img")
                    m.save()
                    return redirect("/laundrycat/")
            context = {
                "form": fm,
                "user": user,
                "user_type_of": user_type
            }
            return render(request, "laundry.html", context)
        return redirect("/laundrycat/")
    else:
        return redirect("/login/")


def launder_cat(request):
    if 'userkey' in request.session:
        user_type = "laundry_shop_user"
        user = LaundryUser.objects.get(email=request.session["userkey"])
        fm = lundey_cat()
        if request.method == "POST":
            if fm.is_valid:
                m = Laundrytype()
                m.user = LaundryshopeUser.objects.get(
                    name__email=request.session["userkey"])
                m.type = request.POST.get("type")
                m.price = request.POST.get("price")
                m.status = request.POST.get("status")
                m.save()
                return redirect("/")
        context = {
            "form": fm,
            "user": user,
            "user_type_of": user_type
        }
    return render(request, "laundrycat.html", context)


def shop_details(request, username):
    if 'userkey' in request.session:
        user = LaundryUser.objects.get(email=request.session["userkey"])

        shop_data = LaundryshopeUser.objects.get(name__username=username)
        shop_cat = Laundrytype.objects.filter(user=shop_data)

        context = {
            "user": user,
            "shop_data": shop_data,
            "shop_cat": shop_cat
        }
    return render(request, "shop_details.html", context)


def shop_details(request, username):

    if 'userkey' in request.session:
        user = LaundryUser.objects.get(email=request.session["userkey"])
        shop_data = LaundryshopeUser.objects.get(name__username=username)
        shop_cat = Laundrytype.objects.filter(user=shop_data)

        context = {
            "user": user,
            "shop_data": shop_data,
            "shop_cat": shop_cat
        }
    return render(request, "shop_details.html", context)


def laundry_order(request, id, username):
    if 'userkey' in request.session:
        user = LaundryUser.objects.get(email=request.session["userkey"])
        launder_user = LaundryshopeUser.objects.get(id=id)
        cat = Laundrytype.objects.filter(user=launder_user)
        order = request.session.get(request.session["userkey"])

        if order:
            if request.method == "POST":
                cart = {}
                category = request.POST.get("select")
                qunt = request.POST.get("qnt")
                order[category] = qunt
                request.session.modified = True
        else:
            if request.method == "POST":
                cart = {}
                category = request.POST.get("select")
                qunt = request.POST.get("qnt")
                cart[category] = qunt
                request.session[request.session["userkey"]] = cart
        context = {
            "user": user,
            "cat": cat,
            "data": order,
            "id": id,
            "username": username

        }
    return render(request, "order.html", context)


def laundry_order_final(request, id, shopname):
    if 'userkey' in request.session:
        user = LaundryUser.objects.get(email=request.session["userkey"])
        order = request.session.get(request.session["userkey"])
        launder_user = LaundryshopeUser.objects.get(id=id)
        data_for_price = Laundrytype.objects.filter(user=launder_user)
        total_price = 0
        for cat, qunt in order.items():
            for i in data_for_price:
                if i.type == cat:
                    price = int(i.price)*int(qunt)
                    total_price += price

        context = {
            "order": order,
            "data_for_price": data_for_price,
            "total_price": total_price,
            "shop_id": id,
            "shop_name": shopname,
            "user": user


        }
    return render(request, "ordersummary.html", context)


def delet_cart(request, cat, id, username):
    if 'userkey' in request.session:
        cart = request.session[request.session["userkey"]]
        del cart[cat]
        request.session.modified = True
    return redirect("/order/%d/%s/" % (int(id), username))


def payment(request, shopid, shopname):
    if 'userkey' in request.session:
        user = LaundryUser.objects.get(email=request.session["userkey"])
        if request.method == "POST":
            paymentmode = request.POST.get("select")
            if paymentmode == "ONLINE":
                order = request.session.get(request.session["userkey"])
                launder_user = LaundryshopeUser.objects.get(id=shopid)
                data_for_price = Laundrytype.objects.filter(user=launder_user)
                total_price = 0
                for cat, qunt in order.items():
                    for i in data_for_price:
                        if i.type == cat:
                            price = int(i.price)*int(qunt)
                            total_price += price
                client = razorpay.Client(
                    auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
                data = {
                    "amount": total_price*100,
                    "currency": "INR",
                    "receipt": "order_rcptid_ashutosh_singh",
                    "notes": {
                        "name": "ashutosh",
                        "payment_for": "launday"
                    }
                }
                payment = client.order.create(data=data)
                order_id = payment['id']

                context = {
                    "RAZORPAY_API_KEY": RAZORPAY_API_KEY,
                    "order_id": order_id,
                    "shopid": shopid,
                    "shopname": shopname,
                    "user": user


                }
                return render(request, "payment_rozarpay.html", context)
            else:
                order = request.session.get(request.session["userkey"])
                o = Order_details()
                o.shop_id = shopid
                o.shop_name = shopname
                user = LaundryUser.objects.get(
                    email=request.session["userkey"])
                o.clint_id = user.id
                o.clint_name = user.name
                o.contact = user.phone
                o.clint_address = user.address+","+user.city+","+user.state+","+user.pin
                launder_user = LaundryshopeUser.objects.get(id=shopid)
                data_for_price = Laundrytype.objects.filter(user=launder_user)
                total_price = 0
                for cat, qunt in order.items():
                    for i in data_for_price:
                        if i.type == cat:
                            price = int(i.price)*int(qunt)
                            total_price += price
                            cat_list = []
                            cat_list.append(cat)
                            cat_list.append(qunt)
                            cat_list.append(price)
                            o.category.append(cat_list)
                o.total_amount = total_price
                o.save()
                del request.session[request.session["userkey"]]
                return HttpResponseRedirect("/confirmation/")
    return render(request, "pay.html", {"user": user})


def paymentSuccess(request, rppid, rpoid, rpsid, shopid, shopname):
    if 'userkey' in request.session:
        order = request.session.get(request.session["userkey"])
        o = Order_details()
        o.shop_id = shopid
        o.shop_name = shopname
        user = LaundryUser.objects.get(email=request.session["userkey"])
        o.clint_id = user.id
        o.clint_name = user.name
        o.contact = user.phone
        o.clint_address = user.address+","+user.city+","+user.state+","+user.pin
        launder_user = LaundryshopeUser.objects.get(id=shopid)
        data_for_price = Laundrytype.objects.filter(user=launder_user)
        total_price = 0
        for cat, qunt in order.items():
            for i in data_for_price:
                if i.type == cat:
                    price = int(i.price)*int(qunt)
                    total_price += price
                    cat_list = []
                    cat_list.append(cat)
                    cat_list.append(qunt)
                    cat_list.append(price)
                    o.category.append(cat_list)
        o.total_amount = total_price
        o.payment = 'Paid'
        o.payment_status = 'ONLINE'
        o.paymentId = rppid
        o.orderId = rpoid
        o.paymentsignature = rpsid
        o.save()
        del request.session[request.session["userkey"]]
    return HttpResponseRedirect('/confirmation/')


def confirmationPage(request):
    if 'userkey' in request.session:
        user = LaundryUser.objects.get(email=request.session["userkey"])
        # buyer = Buyer.objects.get(username=request.user)
        # subject = "Thanks to Shop with US"
        # # message = """
        # #                 Your Order is Successfully Received
        # #                 We will contact you soon for Delivery
        # #                 Team : MyShop.com
        # #             """
        # # email_from = "Ashutosh.Bluthink@gmail.com"
        # # recipient_list = [buyer.email,]
        # # try:
        # # send_mail( subject, message, email_from, recipient_list )
        # # except:
        # # messages.info(request,"some error in you mail")
        # subject = "Thanks to Shop with US"
        # html_content = "<p>Your Order is Successfully Received We will contact you soon for DeliveryTeam : MyShop.com</p>"
        # from_email = "Ashutosh.Bluethink@gmail.com"
        # to = buyer.email
        # msg = EmailMessage(subject, html_content, from_email, [to])
        # msg.content_subtype = "html"  # Main content is now text/html
        # try:
        #     msg.send()
        # except:
        #     messages.info(request, "some error in  mail sending")
        # ################## here implement sms ###################
        # client = Client(account_sid, auth_token)

        # message = client.messages.create(
        #                     body=f"hello {buyer.name} Your Order is Successfully Received We will contact you soon for DeliveryTeam : MyShop.com ",
        #                     from_='+13252306436',
        #                     to='+917524986362'
        #                 )
        # print(message.sid,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5")
        context = {
            "user": user
        }
    return render(request, "confirmation.html", context)


def order_list_for_user(request):
    if 'userkey' in request.session:
        user = LaundryUser.objects.get(email=request.session["userkey"])
        data = Order_details.objects.filter(clint_id=user.id)
        cod = "COD"
        context = {
            "user": user,
            "data": data,
            "COD": cod
        }
    return render(request, "user_order_list.html", context)


def order_list_for_shop(request):
    if 'userkey' in request.session:
        user = LaundryUser.objects.get(email=request.session["userkey"])
        laundary_user = LaundryshopeUser.objects.get(name=user)
        order_data = Order_details.objects.filter(shop_id=laundary_user.id)
        context = {
            "user": user,
            "data": order_data,
        }
    return render(request, "shop_order_list.html", context)


def after_oredr_pay(request, id):
    if 'userkey' in request.session:
        order_data = Order_details.objects.get(id=id)
        client = razorpay.Client(
            auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
        data = {
            "amount": order_data.total_amount*100,
            "currency": "INR",
            "receipt": "order_rcptid_ashutosh_singh",
            "notes": {
                "name": "ashutosh",
                "payment_for": "launday"
            }
        }
        payment = client.order.create(data=data)
        order_id = payment['id']

        context = {
            "RAZORPAY_API_KEY": RAZORPAY_API_KEY,
            "order_id": order_id,
            "oder_id": id
        }
    return render(request, "paymentSuccess_after_pay.html", context)


def paymentSuccess_after_order(request, rppid, rpoid, rpsid, oder_id):
    if 'userkey' in request.session:
        order_data = Order_details.objects.get(id=oder_id)

        order_data.payment = 'Paid'
        order_data.payment_status = 'ONLINE'
        order_data.paymentId = rppid
        order_data.orderId = rpoid
        order_data.paymentsignature = rpsid
        order_data.save()
    return HttpResponseRedirect('/confirmation/')


def update_profile(request):
    if 'userkey' in request.session:
        user = LaundryUser.objects.get(email=request.session["userkey"])
        fm = profile(instance=user)
        if request.method == "POST":
            fm = profile(request.POST, request.FILES, instance=user)
            if fm.is_valid:
                fm.save()
        context = {
            "form": fm,
            "user": user
        }

    return render(request, "profile.html", context)


def shop_profile(request):
    if 'userkey' in request.session:
        user = LaundryUser.objects.get(email=request.session["userkey"])
        shopuser=LaundryshopeUser.objects.get(name=user)
        fm = shopform(instance=shopuser)
        if request.method == "POST":
            fm =shopform(request.POST, request.FILES, instance=shopuser)
            if fm.is_valid:
                fm.save()
        context = {
            "form": fm,
            "user": user,
            "shopuser":shopuser
        }

    return render(request, "shopprofile.html", context)


def change_password(request):
    if 'userkey' in request.session:
        user = LaundryUser.objects.get(email=request.session["userkey"])
        if request.method == "POST":
            old_pass = request.POST.get("old")
            new = request.POST.get("new")
            data = check_password(old_pass, user.password)
            if data == True:
                newpass = make_password(new)
                user.password = newpass
                user.save()
                messages.success(request, "succesfully Password Change")
        context = {
            "user": user
        }
    return render(request, "updatepass.html", context)


def order_update(request, order_id):
    user = LaundryUser.objects.get(email=request.session["userkey"])
    order_data = Order_details.objects.get(id=order_id)
    fm = oderformforupdate(instance=order_data)
    if request.method == "POST":
        if order_data.payment == "Unpaid":
            fm = oderformforupdate(request.POST, instance=order_data)
            fm.save()
        else:
            order_data.user=order_data
            order_data.status=request.POST.get("status")
            order_data.delivery_date=request.POST.get("delivery_date")
            order_data.save()
            

    context={
            "user":user,
            "form":fm
    }
    return render(request,"orderupdate.html",context)


