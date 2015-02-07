from django.db import models

# Create your models here.

# This is the user-model for Skifer. The user is identified by a unique pair of 
# email id and reference id.
# The ref id is meant for the user to share the page using his/her id, however that
# feature is currently not being employed by us.
class Join(models.Model):
	email = models.EmailField()
	friend = models.ForeignKey("self", related_name = "referral",\
								null = True, blank = True)
	ref_id = models.CharField(max_length = 120, default = '123', unique = True)
	ip_address = models.CharField(max_length=120, default='ABC')
	timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
	updated = models.DateTimeField(auto_now_add = False, auto_now = True)

	def __unicode__(self):
		return self.email

	class Meta:
		unique_together = ('email', 'ref_id',)