from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import pre_save
from taggit.managers import TaggableManager
from .utils import get_read_time
from django.utils.safestring import mark_safe
class PublishedManager(models.Manager): 
    def get_queryset(self): 
        return super(PublishedManager, self).get_queryset().filter(status='published')


def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

class Post(models.Model): 
    STATUS_CHOICES = ( 
        ('draft', 'Draft'), 
        ('published', 'Published'), 
    ) 
    title   = models.CharField(max_length=250) 
    slug    = models.SlugField(max_length=250, unique_for_date='publish') 
    author  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    image   = models.ImageField(upload_to=upload_location, null=True, blank=True)
    body    = RichTextUploadingField()
    publish = models.DateTimeField(default=timezone.now)
    read_time =  models.IntegerField(default=0) # models.TimeField(null=True, blank=True) #as sume minutes 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    status  = models.CharField(max_length=10,  choices=STATUS_CHOICES, default='draft') 
    ovation = models.ManyToManyField(User, blank=True, related_name="ovation")
    objects = models.Manager() # The default manager. 
    published = PublishedManager() # Our custom manager.
    tags = TaggableManager()

    class Meta: 
        ordering = ('-publish',) 

    def __str__(self): 
        return self.title


    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    def get_markdown(self):
        body = self.body
        return mark_safe(body)

    def total_ovations(self):
        return self.ovation.count()

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if instance.body:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var

pre_save.connect(pre_save_post_receiver, sender=Post)

class Comment(models.Model): 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', null=True, on_delete=models.CASCADE, related_name='replies')
    body = RichTextUploadingField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True) 
 
    class Meta: 
        ordering = ('created',) 
 
    def __str__(self): 
        return 'Comment by {} on {}'.format(self.author.username, self.post.title)

    def get_markdown(self):
        body = self.body
        return mark_safe(body)
