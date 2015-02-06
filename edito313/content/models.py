from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from djangospam.cookie import moderator as cookie
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
                         TYPES.PAGE: (TYPES.PAGE,),
                         TYPES.CATEGORY: (TYPES.CATEGORY,),
                         TYPES.QUOTE: (TYPES.CATEGORY,),
                         TYPES.IMAGE: (TYPES.CATEGORY,),}

    type = models.CharField(max_length=50, choices=TYPES.choices())
    parent = models.ForeignKey('self', blank=True, null=True)
    # TODO: ensure configurable uniqueness
    slug = models.SlugField(max_length=200, blank=True)
    author = models.ForeignKey(User, blank=True, null=True)
    author_mail = models.EmailField(max_length=254)
    author_ip = models.GenericIPAddressField()
    datetime = models.DateTimeField(auto_now_add=True)
    published_datetime = models.DateTimeField(blank=True)
    approved = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    text = models.TextField(blank=False)
    tags = TaggableManager() 
    
    class Meta:
        ordering = ['published_datetime', 'datetime', 'title']
        
    def __str__(self):
        return '{type}: {title}'.format(type=self.get_type_display(),
                                        title=self.title)
    
    # TODO: content excerpt
    def extract(self):
        return self.text

class Options(models.Model):
    """Administrative options for content.""" 
    class UNIQUE(Choices):
        NONE = 'none'
        TOTALLY_UNIQUE = 'totally unique'
        DATE = 'date'
        MONTH = 'month'
        YEAR = 'year'
        
    type = models.CharField(max_length=50, choices=Content.TYPES.choices(), unique=True)
    unique = models.CharField(max_length=50, choices=UNIQUE.choices(),
                              default=UNIQUE.NONE.name)
    approve_permission = models.CharField(max_length=50, blank=True)
    must_be_reviewed = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'options'
    
    def __str__(self):
        return '{type} options'.format(type=self.get_type_display()).capitalize()

options.register(Options, Content)

try:
    cookie.register(Content)
except cookie.AlreadyModerated:
    pass