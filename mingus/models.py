from django.db import models

class Tag(models.Model):
    title = models.CharField(max_length=250,
                             help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True,
                            help_text='Suggested valu automatically generated from title. Must be uniqe.')
    description = models.TextField()

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

    def get_absoulte_url(self):
        return "/tags/%s/" % self.slug