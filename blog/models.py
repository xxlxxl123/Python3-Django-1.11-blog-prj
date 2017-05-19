from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from uuslug import slugify
from django.conf import settings

class PostManager(models.Manager):       #筛选，查询器，django内置。来自models.Manager
    def active(self,*args,**kwargs):
        return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())#all()#order_by('-timestamp')


# Create your models here.
def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)   #blank=True, null=True
    title = models.CharField(max_length=100)  # 博客题目
    slug = models.SlugField(unique=True)  # Field.unique如果是 True，该字段在整个表中必须是唯一的。
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field="width",
                              height_field="height")  # 图片文件数据，允许为空
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now_add=False, auto_now=False)
    category = models.CharField(max_length=50, blank=True)  # 博客标签
    updated = models.DateTimeField(auto_now=True, blank=False, null=True)  # 更新日期
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # 博客日期
    content = models.TextField(blank=True, null=True)  # 博客文章正文
    objects = PostManager()
    # class Meta:
    #     db_table='article'
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug':self.slug})

    class Meta:  # 定义数据库
        ordering = ['-timestamp', '-updated']


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title, max_length=15)
    if new_slug is not None:
        slug = new_slug
    qs = Article.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Article)
