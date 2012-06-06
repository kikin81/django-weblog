from my_comment_app.models import CommentWithTitle
from my_comment_app.forms import CommentFormWithTitle

def get_model():
    return CommentWithTitle

def get_form():
    return CommentFormWithTitle