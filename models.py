from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from registration.signals import user_registered

# Create your models here.

class Account(models.Model):
	owner = models.OneToOneField(User)
	publisherBalance = models.DecimalField(max_digits=10, decimal_places=2)
	advertiserBalance = models.DecimalField(max_digits=10, decimal_places=2)

class Poll(models.Model):
	owner = models.ForeignKey(User)
	question = models.CharField(max_length=200)
	def __unicode__(self):
		return self.question

class Choice(models.Model):
	poll = models.ForeignKey(Poll)
	choiceText = models.CharField(max_length=100)
	choiceUrl = models.URLField(blank=True)
	def __unicode__(self):
		return self.choice_text

class Publisher(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=1000)
	mainUrl = models.URLField()
	basePrice = models.DecimalField(max_digits=10, decimal_places=2)
	allowNSFW = models.BooleanField()
	active = models.BooleanField()
	def __unicode__(self):
		return self.name

class Campaign(models.Model):
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=100)
	poll = models.ForeignKey(Poll)
	active = models.BooleanField()
	budget = models.DecimalField(max_digits=10, decimal_places=2)
	def __unicode__(self):
		return self.name

class PublisherCampaign(models.Model):
	publisher = models.ForeignKey(Publisher)
	campaign = models.ForeignKey(Campaign)
	pricePerAction = models.DecimalField(max_digits=10, decimal_places=2)

class AdView(models.Model):
	campaign = models.ForeignKey(Campaign)
	session = models.ForeignKey(Session)
	datetime = models.DateTimeField()

class ResultView(models.Model):
	campaign = models.ForeignKey(Campaign)
	session = models.ForeignKey(Session)
	datetime = models.DateTimeField()

class AdVote(models.Model):
	campaign = models.ForeignKey(Campaign)
	session = models.ForeignKey(Session)
	choice = models.ForeignKey(Choice)
	datetime = models.DateTimeField()

class AdClick(models.Model):
	campaign = models.ForeignKey(Campaign)
	session = models.ForeignKey(Session)
	choice = models.ForeignKey(Choice)
	datetime = models.DateTimeField()

def user_registered_callback(sender, user, request, **kwargs):
	profile = Account(owner = user)
	profile.publisherBalance = 0
	profile.advertiserBalance = 0
	profile.save()

user_registered.connect(user_registered_callback)
