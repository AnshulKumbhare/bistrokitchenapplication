from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from bistrokitchen_app.models import menuitem, cart, contact, chef, order, testimonial
from django.db.models import Q
import random
import razorpay

# Create your views here.


def header(request):
    return render(request, 'header.html')

def footer(request):
    return render(request, 'footer.html')

def home(request):
    t = testimonial.objects.all()
    context = {}
    context['testimony'] = t
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['umail']
        username = request.POST['user']
        password = request.POST['upass']
        ucpass = request.POST['ucpass']

        if fname == "" or lname == "" or email == "" or username == "" or password == "" or ucpass == "":
            context = {}
            context['errmsg'] = "Fields cannot be Empty"
            return render(request, 'register.html', context)
        
        elif password != ucpass:
            context = {}
            context['errmsg'] = "Password did not match"
            return render(request, 'register.html', context)
        
        else:
            try:
                u = User.objects.create(first_name = fname, last_name = lname, email = email, username = username, password = password)
                u.set_password(password)
                u.save()
                context = {}
                context['success'] = "Account created Successfully"
                return render(request, 'home.html', context)
            except Exception:
                context = {}
                context['errmsg'] = "Username already Exists"
                return render(request,'register.html', context)
    else:
        return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['upass']
        ucpass = request.POST['ucpass']

        if username == "" or password == "" or ucpass == "":
            context = {}
            context['errmsg'] = "Fields cannot be empty"
            return render(request, 'login.html', context)
        
        elif password != ucpass:
            context = {}
            context['errmsg'] = "Password did not match"
            return render(request, 'login.html', context)
        
        else:
            u = authenticate(username = username, password = password)
            if u is not None:
                login(request, u)
                return redirect('/home')
            else:
                context = {}
                context['errmsg'] = "Invalid Username or Password"
                return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')
    

def user_logout(request):
    logout(request)
    return redirect('/home')
    

def menu(request):
    m = menuitem.objects.filter(is_active = True)
    # print(m)
    context = {}
    context['menu'] = m
    return render(request, 'menu.html', context)


def menufilter(request, mf):
    q1 = Q(is_active = True)
    q2 = Q(category = mf)
    m = menuitem.objects.filter(q1 & q2)
    context = {}
    context['menu'] = m
    return render(request, 'menu.html', context)

def pricefilter(request, pf):
    if pf == '0':
        col = 'price'   #Ascending Order
    else:
        col = '-price'  #Descending Order

    m = menuitem.objects.order_by(col)
    context = {}
    context['menu'] = m
    return render(request, 'menu.html', context)

def minmaxrange(request):
    min = request.GET['minval']
    max = request.GET['maxval']

    q1 = Q(price__gte = min)
    q2 = Q(price__lte = max)
    q3 = Q(is_active = True)
    
    m = menuitem.objects.filter(q1 and q2 and q3)
    context = {}
    context['menu'] = m
    return render(request, 'menu.html', context)


def menudetails(request, mdid):
    m = menuitem.objects.filter(id = mdid)
    context = {}
    context['menu'] = m
    return render(request, 'menudetails.html', context)

def addtocart(request, mdid):
    userid = request.user.id
    u = User.objects.filter(id = userid)
    print(u[0])
    m = menuitem.objects.filter(id = mdid)
    print(m[0])

    q1 = Q(uid = u[0])
    q2 = Q(pid = m[0])
    c = cart.objects.filter(q1 and q2)
    n = len(c)
    # print(n)
    context = {}
    context['menu'] = m
    
    if n >= 1:
        context['errmsg'] = "Item already exists in Cart !!!"
    else:
        c = cart.objects.create(uid = u[0], pid = m[0])
        c.save()
        context['success'] = "Product added successfully in the cart !!!"

    return render(request, 'menudetails.html', context)



def viewcart(request):
    userid = request.user.id
    c = cart.objects.filter(uid = userid)
    context = {}
    
    s = 0
    totalitems = 0
    for i in c:
        s += i.pid.price * i.qty
        totalitems += i.qty

    context['cartitems'] = c
    context['totalprice'] = s
    context['items'] = totalitems
    
    return render(request, 'cart.html', context)


def updateqty(request, qv, cid):
    c = cart.objects.filter(id = cid)
    if qv == "1":
        newqty = c[0].qty + 1
        c.update(qty = newqty)
    else:
        if c[0].qty > 1:
            newqty = c[0].qty - 1
            c.update(qty = newqty)
    return redirect('/viewcart')

def remove(request, cid):
    c = cart.objects.filter(id = cid)
    c.delete()
    return redirect('/viewcart')

def placeorder(request):
    userid = request.user.id
    c = cart.objects.filter(uid = userid)
    # print(c[0].pid.name, c[0].qty)
    
    oid = random.randrange(1000, 9999)
    print(oid)

    for i in c:
        o = order.objects.create(orderid = oid, uid = i.uid, pid = i.pid, qty = i.qty)
        o.save()
        i.delete()

    orders = order.objects.filter(uid = userid)

    s = 0
    totalitems = 0
    for i in orders:
        s += i.pid.price * i.qty
        totalitems += i.qty
    context = {}
    context['orderitems'] = orders
    context['totalprice'] = s
    context['items'] = totalitems

    return render(request, 'placeorder.html', context)

def removeorder(request, o_id):
    o = order.objects.filter(id = o_id)
    o.delete()
    return redirect('/placeorder')

def contactus(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        umail = request.POST['umail']
        usubject = request.POST['usubject']
        umsg = request.POST['umsg']

        if uname == "" or umail == "" or usubject == "" or umsg == "":
            context = {}
            context['errmsg'] = "Please enter all details !!!"
            return render(request, 'contact.html', context)
        else:
            m = contact.objects.create(name = uname, email = umail, subject = usubject, message = umsg)
            m.save()
            context = {}
            context['success'] = "Message sent Successfully !!!"
            return render(request, 'contact.html', context)
    else:
        return render(request, 'contact.html')
    
def chefs(request):
    c = chef.objects.all()
    context = {}
    context['chefinfo'] = c
    return render(request, 'chef.html', context)



def makepayment(request):
    orders = order.objects.filter(uid = request.user.id)
    # print(o[0].pid.price * o[0].qty)
    amt = 0
    for i in orders:
        amt += i.pid.price * i.qty
        oid = i.orderid

    # print(amt)
    # print(oid)
        
    client = razorpay.Client(auth=("rzp_test_9TH7HLFyaq2ysI", "0ESpk0Atz5iu8kPVRe6QJNWL"))

    DATA = {
        "amount": amt * 100,
        "currency": "INR",
        "receipt": oid,
        "notes": {
            "key1": "value3",
            "key2": "value2"
        }
    }
    payment = client.order.create(data = DATA)
    print(payment)
    context = {}
    context['data'] = payment
    client.order.create(data=DATA)

    return render(request, 'pay.html', context)