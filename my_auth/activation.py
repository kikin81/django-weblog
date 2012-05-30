from django.core.mail import send_mail
from hashlib import md5
from django.contrib.auth.models import User
from django.template import loader, Context
import time

def send_activation(user):
    time.sleep(10)
    code = md5(user.username).hexdigest()
    url = "http://127.0.0.1:8000/accounts/activate/?user=%s&code=%s" % (user.username,  code)
    print(url)
    template = loader.get_template('registration/activation.html')
    context = Context({
        'username': user.username, 
        'url': url, 
    })
 
    send_mail('Activate account at super site', template.render(context), 'no-reply@example.com', [user.email])

def activate_user(username, code):
    if code == md5(username).hexdigest():
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        return True
    else:
        return False