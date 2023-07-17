from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from egorsConventer.settings import MEDIA_ROOT, MEDIA_URL

from mainpage.forms import *

# Create your views here.
from mainpage.utils  import *

def index(request):
    if request.method == "POST":
        form = UploadPic(request.POST, request.FILES)
        if form.is_valid():
            instance =  form.save()
            urk = instance.photo.url
            urr = urk.rsplit('/', 1)[-1]
            process_picture(urr)
            return redirect("/gallery/"+urr)
    else:
        form = UploadPic()
    return render(request, 'mainpage/mainpage.html', {'form':form,'menu':menu})

def log(request):
    return render(request, 'mainpage/LoginPage.html', {'menu':menu})

def reg(request):
    return render(request, 'mainpage/RegisterPage.html', {'menu':menu})

def gal(request,image_name):

    im = image_name
    return render(request, 'mainpage/gall.html', {'menu': menu, 'im':im, 'media_url': MEDIA_URL} )

def inf(request):
    return render(request, 'mainpage/infopage.html', {'menu':menu})


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'mainpage/RegisterPage.html'
    success_url = reverse_lazy('log')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Registration")
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'mainpage/LoginPage.html'
    success_url = reverse_lazy('log')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Authentication")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('log')