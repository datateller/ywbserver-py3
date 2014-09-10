from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.measure import D
import dbarray
import datetime
from django.utils.timezone import utc
# Create your models here.


class TopicBase(models.Model):
    from_user = models.ForeignKey(User)
    content = models.TextField()
    comments = dbarray.IntegerArrayField(null=True)
    create_time = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))
    update_time = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))
    class Meta:
        abstract = True


class CommentBase(models.Model):
    from_user = models.ForeignKey(User)
    content = models.TextField()
    create_time = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))
    class Meta:
        abstract = True
    
class PraiseBase(models.Model):
    from_user = models.ForeignKey(User)
    create_time = models.DateTimeField(default=datetime.datetime.utcnow().replace(tzinfo=utc))
    class Meta:
        abstract = True
    
