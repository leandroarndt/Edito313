from django.views.generic import ListView, DetailView
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from edito313.content.models import Content, Options
from edito313.tools.views import BaseView

class ContentListView(BaseView, ListView):
    model = Content
    context_object_name = 'content_list'
    
    def get_queryset(self):
        queryset = super(ContentListView, self).get_queryset()
        
        # Exclude types not shown in archives:
        excluded = Options.objects.filter(exclude_from_archive=True)
        queryset = queryset.exclude(type__in=[opt.type for opt in excluded])
        args = []
        if 'uri' in self.kwargs:
            args = self.kwargs['uri'].split('/')
            if not args[0].isdigit(): # We have a prefix:
                queryset = queryset.filter(type=Options.objects.get(uri_prefix=args[0]+'/').type)
                args = args[1:]
            if len(args) > 3: # We don't have anything more detailed than daily archive
                queryset = queryset.none()
            if args: # Get archive year
                queryset = queryset.filter(publishing__year=args[0])
                args = args[1:]
            if args: # Get archive month
                queryset = queryset.filter(publishing__month=args[0])
                args = args[1:]
            if args: # Get archive day
                queryset = queryset.filter(publishing__day=args[0])
            
        return queryset
    
class ContentDetailView(BaseView, DetailView):
    model = Content
    model_object_name = 'content'
    
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        args = self.kwargs['uri'].split('/')

        # Step 1: filter prefixes.
        if not (args[0].startswith('pk-') or args[0].isdigit()): # First part is a prefix
            opt = Options.objects.get(uri_prefix=args[0]+'/') # Prefixes end with "/"
            queryset.filter(type=opt.type)
            args = args[1:] # Drops prefix.
        else: # No prefix.
            # Exclude types which use non-blank value:
            opts = Options.objects.exclude(uri_prefix='')
            queryset = queryset.exclude(type__in=[opt.type for opt in opts])
            # Exclude types which use default (not blank) value:
            if Options.objects.get(type='').uri_prefix != '':
                excludes = []
                for t in Content.TYPES.choices():
                    try:
                        Options.objects.get(type=t[0])
                    except ObjectDoesNotExist:
                        excludes.append(t[0])
                queryset = queryset.exclude(type__in=excludes)
        
        # Step 2: get the object according to the prefix.
        if args[0].startswith('pk-'): # Has no uniqueness
            return queryset.get(pk=int(args[0][3:]))
        if len(args) == 1: # Is totally unique without prefix
            return self.queryset.get(slug=args[0])
        if len(args) == 2:
            return queryset.get(publishing__year=args[0], slug=args[1])
        elif len(args) == 3:
            return queryset.get(publishing__year=args[0], publishing__month=args[1],
                                slug=args[2])
        elif len(args) == 4:
            return queryset.get(publishing__year=args[0], publishing__month=args[1],
                                publishing__day=args[2], slug=args[3])