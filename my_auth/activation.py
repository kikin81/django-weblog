from django.core.mail import send_mail
from hashlib import md5
from django.template import loader, Context
import time

def send_activation(user):
    time.sleep(10)
    code = md5(user.username).hexdigest()
    url = "http://127.0.0.1:8000/activate/?user=%s&code=%s" % (user.username,  code)
    print(url)
    template = loader.get_template('registration/activation.html')
    context = Context({
        'username': user.username, 
        'url': url, 
    })
 
    send_mail('Activate account at super site', template.render(context), 'no-reply@example.com', [user.email])