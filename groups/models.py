from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Group(models.Model):
	name = models.TextField(default = '')
	alias = models.TextField(default = '', unique = True)
	tags = models.TextField(default = '')
	description = models.TextField(default = '')

	def get_absolute_url(self):
		return reverse('view_group', args=[self.alias])

class User(models.Model):
	access_token = models.TextField(default = '')
	apelido = models.TextField(default = '')
	turma = models.TextField(default = '')
	groups = models.ManyToManyField(Group)

	def get_absolute_url(self):
		return reverse('view_user', args=[self.id])

	
