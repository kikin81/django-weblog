from django.http import Http404
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from forms import RegisterForm


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return render_to_response("registration/registration_complete.html")
    else:
        form = RegisterForm()

    return render_to_response("registration/register.html",
                              {"form": form, },)


def activate(request):
    user = request.GET.get('user')
    code = request.GET.get('code')

    if activate_user(user, code):
        return render_to_response("registration/activation_complete.html")
    else:
        raise Http404
