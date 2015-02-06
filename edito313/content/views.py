from django.views.generic import ListView, DetailView
from edito313.content.models import Content
from edito313.tools.views import BaseView

# TODO: exclude comments from the basic content list
class ContentListView(BaseView, ListView):
    model = Content
    context_object_name = 'content_list'
    
class ContentDetailView(BaseView, DetailView):
    model = Content
    model_object_name = 'content'