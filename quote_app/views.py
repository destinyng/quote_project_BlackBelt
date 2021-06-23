from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt


# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method != 'POST':
        return redirect ('/')
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        request.session['userid'] = new_user.id
        request.session['first_name'] = new_user.first_name
        request.session['last_name'] = new_user.last_name
        #messages.info(request, "User registered; log in now")
    return redirect('/quotes')
   


def login(request):
    if request.method != 'POST':
        return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                request.session['first_name'] = logged_user.first_name
                request.session['last_name'] = logged_user.last_name
            return redirect('/quotes')
        messages.error(request, "Email and password are incorrect")
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def quotes(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        logged_user = User.objects.get(id=request.session['userid'])
        

        all_quotes = Quote.objects.all().order_by('created_at')
        
        context ={
            #'my_wishes': Wish.objects.filter(wished_by= logged_user),
            'all_quotes': all_quotes,
            'user': logged_user
        }
        return render(request, 'quotes.html', context)

def create(request):
    if 'userid' not in request.session:
        return redirect('/')
    errors = Quote.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    logged_user = User.objects.get(id=request.session['userid'])   
    Quote.objects.create(
        author = request.POST['author'],
        content = request.POST['content'],
        posted_by = logged_user

    )
    
    return redirect('/quotes')

def editmyaccount(request, userid):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        logged_user = User.objects.get(id=request.session['userid'])   
    context = {
        'user': logged_user
    }
    return render(request, 'edit.html', context)
        
def update(request, userid):
    if 'userid' not in request.session:
        return redirect('/')
    errors = User.objects.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/editmyaccount/{}".format(userid))
    # update wish!
    to_update = User.objects.get(id=userid)
    # updates each field
    to_update.first_name = request.POST['first_name']
    to_update.last_name = request.POST['last_name']
    to_update.email = request.POST['email']
    to_update.save()
    return redirect('/quotes')
    
def profile(request,userid):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=userid)
        user_quotes = Quote.objects.filter(posted_by=userid).order_by('created_at')
        
        context ={
            #'my_wishes': Wish.objects.filter(wished_by= logged_user),
            'user_quotes': user_quotes,
            'user': user
        }
        return render(request, 'profile.html', context)

    
def like(request,quoteid):
    if 'userid' not in request.session:
        return redirect('/')
    if request.method == "POST":
        logged_user = User.objects.get(id=request.session['userid'])   
        quote = Quote.objects.get(id=quoteid)
        liked_users = quote.user_that_like_quote
        liked_users.add(logged_user)
    return redirect('/quotes')


def delete(request,quoteid):
    to_delete = Quote.objects.get(id=quoteid)
    to_delete.delete()
    return redirect('/quotes')



