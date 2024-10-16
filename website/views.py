from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .forms import AddRecordForm
from .models import Record
# Create your views here.


def home(request):
    records = Record.objects.all

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "You have been logged in")
            return redirect('home')
        
        else:
            messages.success(request, "There was an error logging you in, Please Try again")
            return redirect('home')
    else:
         return render(request, 'home.html', {'records':records})





def logout_user(request):
    logout(request)
    messages.success(request, "You have been Logged Out...")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']  # Should use 'password', not 'password1'
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully signed in")
                return redirect('home')  # Redirect to home page or another page
            else:
                messages.error(request, "Authentication failed. Please try again.")
                return redirect('login')  # You can redirect to the login page
        else:
            # Form is invalid, show the form again with errors
            messages.error(request, "There was an error with your form.")
            return render(request, 'register.html', {'form': form})

    else:
        # GET request, render the empty registration form
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    



def customer_record(request,pk):
    if request.user.is_authenticated:
        #lookup record
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.error(request, "You must be Logged In To View This Page")
        return redirect('home')
    

def delete_record(request,pk):
    if request.user.is_authenticated:

        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully")
        return redirect('home')
    else:
       messages.success(request, "You Must Be Logged In To Delete Record")     

def add_record(request):
            form = AddRecordForm(request.POST or None)
            if request.user.is_authenticated:
                    if request.method == "POST":
                            if form.is_valid():
                                add_record = form.save()
                                messages.success(request, "Record Added....")
                                return redirect('home')
        
                
                    return render(request, 'add_record.html', {'form': form})
            else:
                 messages.success(request, "You Must Be Logged In")
                 return redirect('home')
            

def update_record(request,pk):
    if request.user.is_authenticated:
         current_record = Record.objects.get(id=pk)
         form = AddRecordForm(request.POST or None, instance=current_record)
         if form.is_valid():
              form.save()
              messages.success(request, "Record Has Been Updated!")
              return redirect('home')
         return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In")
        return redirect('home')