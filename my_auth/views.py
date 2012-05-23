from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from forms import RegisterForm

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = RegisterForm()

    return render_to_response("registration/register.html",
                              {"form": form,},)

def activate(request):
    user = request.GET.get('user')
    code = request.GET.get('code')

    if active_user(user, code):
        return HttpResponseRedirect("/")
    else:
        raise Http404

def activate_user(username, code):
    if code == md5(username).hexdigest():
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        return True
    else:
        return False