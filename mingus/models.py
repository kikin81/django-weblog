from django.contrib.auth.models import User
from django.db import models
from markdown import markdown

import datetime

class Tag(models.Model):
    """
    Tag Model with fields: title, slug
    """
    title = models.CharField(max_length=250,
                             help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True,
                            help_text='Suggested value automatically generated from title. Must be uniqe.')

    def live_entry_set(self):
        from mingus.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('mingus_tag_detail', (), { 'slug': self.slug })

class LiveEntryManager(models.Manager):
    """
    A query that returns entries whose status is LIVE
    """
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)


class Entry(models.Model):
    """
    Entry Model with fields: title, excerpt, body, pub_date, excerpt_html,
      body_html, author, enable_comments, featured, slug, status, tags,
      objects, live.
    Tags are associated with a Many-to-Many relationship.
    """
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )
    
    # Entry main fields.
    title = models.CharField(max_length=250,
                             help_text='Maximum 250 characters.')
    excerpt = models.TextField(blank=True,
                               help_text='A short summary of the entry. Optional.')
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)

    # Fields to store generated HTML.
    excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)

    # Metadata.
    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(unique_for_date='pub_date',
                            help_text='Suggested value automatically generated from title. Must be unique.')
    status = models.IntegerField(choices=STATUS_CHOICES,
                                 default=LIVE_STATUS,
                                 help_text='Only entries with live status will be publicly displayed.')
    
    # Categorization.
    tags = models.ManyToManyField(Tag)

    objects = models.Manager()
    live = LiveEntryManager()
    
    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = "Entries"

    def __unicode__(self):
        return self.title
    
    def save(self, force_insert=False, force_update=False):
        self.body_html = markdown(self.body)
        if self.excerpt:
            self.excerpt_html = markdown(self.excerpt)
        super(Entry, self).save(force_insert, force_update)

    @models.permalink
    def get_absolute_url(self):
        return ('mingus_entry_detail', (), {  'year': self.pub_date.strftime("%Y"),
                                                'month': self.pub_date.strftime("%b").lower(),
                                                'day': self.pub_date.strftime("%d"),
                                                'slug': self.slug })


class SearchKeyword(models.Model):
    """
    Keyword Model to speed up searches made on the Entries.
    """
    keyword = models.CharField(max_length=50)
    page = models.ForeignKey(Entry)
    
    def __unicode__(self):
        return self.keyword


from akismet import Akismet
from django.conf import settings
from django.contrib.comments.moderation import CommentModerator, moderator
from django.contrib.sites.models import Site
from django.utils.encoding import smart_str

class EntryModerator(CommentModerator):
    auto_moderate_field = 'pub_date'
    moderate_after = 30
    email_notification = True

    def moderate(self, comment, content_object, request):
        already_moderated = super(EntryModerator, self).moderate(comment, content_object, request)
        if already_moderated:
            return True
        akismet_api = Akismet(key=settings.AKISMET_API_KEY, blog_url="http://%s/" %Site.objects.get_current().domain)
        if akismet_api.verify_key():
            akismet_data = { 'comment_type': 'comment',
                             'referrer': request.META['HTTP_REFERER'],
                             'user_ip': comment.ip_address,
                             'user_agent': request.META['HTTP_USER_AGENT'] }
            return akismet_api.comment_check(smart_str(comment.comment),
                akismet_data,
                build_data=True)
        return False
moderator.register(Entry, EntryModerator)