from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError,\
    MultipleObjectsReturned, NON_FIELD_ERRORS
from taggit.managers import TaggableManager
from djangospam.cookie import moderator as cookie
from ckeditor.fields import RichTextField
from edito313.tools.choices import Choices, unique
from edito313.tools import options

class Content(models.Model):
    @unique
    class TYPES(Choices):
        """Types of content.

These types determine the ways of showing specific content. Other types may be
added at runtime."""
        BLOGPOST = 'blog post'
        PAGE = 'page'
        QUOTE = 'quote'
        IMAGE = 'image'
        CATEGORY = 'category'
        
    allowed_parents = {  TYPES.BLOGPOST: (TYPES.CATEGORY,),
                         TYPES.PAGE: (TYPES.PAGE,
                                      TYPES.CATEGORY),
                         TYPES.CATEGORY: (TYPES.CATEGORY,),
                         TYPES.QUOTE: (TYPES.CATEGORY,),
                         TYPES.IMAGE: (TYPES.CATEGORY,),}

    type = models.CharField(max_length=50, choices=TYPES.choices())
    parent = models.ManyToManyField('self', blank=True, null=True)
    title = models.CharField(max_length=200)
    text = RichTextField(blank=False)
    tags = TaggableManager(blank=True) 
    slug = models.SlugField(max_length=200, blank=True)
    author = models.ForeignKey(User, blank=True, null=True)
    creation = models.DateTimeField(auto_now_add=True)
    publishing = models.DateTimeField(blank=True)
    editing = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['publishing', 'title', 'author__name']
        
    def __str__(self):
        return '{type}: {title}'.format(type=self.get_type_display(),
                                        title=self.title)
    
    # TODO: content excerpt
    def excerpt(self):
        return self.text
    
    def validate_unique(self, *args, **kwargs):
        """Validates for slulg uniqueness."""
        valid = True
        try:
            options = Options.objects.get(type=self.type)
            try:
                if options.unique == Options.UNIQUE.TOTALLY_UNIQUE.name:
                    obj = Content.objects.get(type=self.type, slug=self.slug)
                    if obj.pk != self.pk:
                        valid = False
                elif options.unique == Options.UNIQUE.DATE.name:
                    obj = Content.objects.get(type=self.type, slug=self.slug,
                            publishing__day=self.publishing.day,
                            publishing__month=self.publishing.month,
                            publishing__year=self.publishing.year)
                    if obj.pk != self.pk:
                        valid = False
                elif options.unique == Options.UNIQUE.MONTH.name:
                    obj = Content.objects.get(type=self.type, slug=self.slug,
                            publishing__month=self.publishing.month,
                            publishing__year=self.publishing.year)
                    if obj.pk != self.pk:
                        valid = False
                elif options.unique == Options.UNIQUE.YEAR.name:
                    obj = Content.objects.get(type=self.type, slug=self.slug, \
                            publishing__year=self.publishing.year)
                    if obj.pk != self.pk:
                        valid = False
                if not valid:
                    raise ValidationError({
                                           NON_FIELD_ERRORS: (\
                                          '"{slug}" is not a unique {type} slug.'\
                                          .format(slug=self.slug, type=self.get_type_display()))
                                             })
            except MultipleObjectsReturned:
                raise ValidationError({
                                           NON_FIELD_ERRORS: (\
                                          '"{slug}" is not a unique {type} slug.'\
                                          .format(slug=self.slug, type=self.get_type_display()),
                                          'There is already more than one {type} with slug "{slug}". Correct this urgently.'\
                                          .format(slug=self.slug, type=self.get_type_display()))
                                             })
            except ObjectDoesNotExist:
                # No conflicting slug found.
                pass
        except ObjectDoesNotExist:
            # No uniqueness defined.
            pass
        if not valid:
            raise (ValidationError, 'Unknown validation error.')
        super(Content, self).validate_unique(*args, **kwargs)

class Options(models.Model):
    """Administrative options for each content type.""" 
    
    @unique
    class UNIQUE(Choices):
        NONE = 'none'
        TOTALLY_UNIQUE = 'totally unique'
        DATE = 'date'
        MONTH = 'month'
        YEAR = 'year'
        
    type = models.CharField(max_length=50, choices=Content.TYPES.choices(), unique=True)
    unique = models.CharField(max_length=50, choices=UNIQUE.choices(),
                              default=UNIQUE.NONE.name)
    
    class Meta:
        verbose_name_plural = 'options'
    
    def __str__(self):
        return '{type} options'.format(type=self.get_type_display()).capitalize()

options.register(Options, Content)

try:
    cookie.register(Content)
except cookie.AlreadyModerated:
    pass