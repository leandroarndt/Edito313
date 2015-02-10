from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError,\
    MultipleObjectsReturned, NON_FIELD_ERRORS, FieldError
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

    type = models.CharField(max_length=50, choices=TYPES.choices(), blank=True)
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
        ordering = ['publishing', 'title']
        
    def __str__(self):
        return '{type}: {title}'.format(type=self.get_type_display(),
                                        title=self.title)
    
    # TODO: content excerpt
    def excerpt(self):
        return self.text
    
    def uri(self):
        """Return content URI according to options."""
        opt = Options.get(self)
        uri = opt.uri_prefix # TODO: change site model to allow a per-site prefix.
        if opt.unique == Options.UNIQUE.TOTALLY_UNIQUE.name:
            return uri + self.slug
        elif opt.unique == Options.UNIQUE.DATE.name:
            return uri + '/'.join((str(self.publishing.year), str(self.publishing.month),
                                  str(self.publishing.day), self.slug))
        elif opt.unique == Options.UNIQUE.MONTH.name:
            return uri + '/'.join((str(self.publishing.year), str(self.publishing.month),
                                  self.slug))
        elif opt.unique == Options.UNIQUE.YEAR.name:
            return uri + '/'.join((str(self.publishing.year), self.slug))
        else:
            return uri + '/'.join(('pk-'+str(self.pk) ,self.slug))
    
    def validate_unique(self, *args, **kwargs):
        """Validates for slug uniqueness."""
        valid = True
        options = Options.get(self)
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
        if not valid:
            raise ValidationError({NON_FIELD_ERRORS: ('Unknown validation error.',)})
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
        
    type = models.CharField(max_length=50, choices=Content.TYPES.choices()+(('','default'),),
                            unique=True, blank=True)
    unique = models.CharField(max_length=50, choices=UNIQUE.choices(),
                              default=UNIQUE.NONE.name)
    uri_prefix = models.CharField(max_length=50, blank=True, verbose_name='URI prefix')
    exclude_from_archive = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'options'
    
    def __str__(self):
            return '{type} options'.format(type=self.get_type_display()).capitalize()
    
    def clean_fields(self, *args, **kwargs):
        if self.uri_prefix != '' and not self.uri_prefix.endswith('/'):
            raise ValidationError({'uri_prefix': 'URI prefix should be blank or end with "/".'})
        if self.uri_prefix == '/':
            raise ValidationError({'uri_prefix': 'Keep URI prefix blank if you don\'t want any prefix'})
        super(Options, self).clean_fields(*args, **kwargs) 
    
    def validate_unique(self, *args, **kwargs):
        # Validate the uniqueness of the prefix
        if self.uri_prefix != '':
            try:
                obj = Options.objects.get(uri_prefix=self.uri_prefix)
                if obj.pk != self.pk:
                    raise MultipleObjectsReturned
            except MultipleObjectsReturned:
                raise ValidationError({NON_FIELD_ERRORS: ('URI prefix must be blank or unique.')})
            except ObjectDoesNotExist:
                pass
        return super(Options, self).validate_unique(*args, **kwargs)
    
    @classmethod
    def get(cls, model):
        try:
            return cls.objects.get(type=model.type)
        except ObjectDoesNotExist:
            return cls.objects.get(type='')

options.register(Options, Content)

try:
    cookie.register(Content)
except cookie.AlreadyModerated:
    pass