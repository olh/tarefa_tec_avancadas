from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from registration.signals import user_registered

# Create your models here.

class Account(models.Model):
	"""Classe de conta da aplicação"""
	owner = models.OneToOneField(User)
	publisherBalance = models.DecimalField(max_digits=10, decimal_places=2)
	advertiserBalance = models.DecimalField(max_digits=10, decimal_places=2)

class Poll(models.Model):
	"""Classe que descreve uma questão a ser respondida"""
	owner = models.ForeignKey(User)
	question = models.CharField(max_length=200)
	def __unicode__(self):
		return self.question

class Choice(models.Model):
	"""Classe que descreve escolhas de resposta de uma questão"""
	poll = models.ForeignKey(Poll)
	choiceText = models.CharField(max_length=100)
	choiceUrl = models.URLField(blank=True)
	def __unicode__(self):
		return self.choice_text

class Publisher(models.Model):
	"""Classe descrevendo um publisher onde a questão será exposta"""
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
	"""Módulo que define uma campanha de publicidade de questão"""
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=100)
	poll = models.ForeignKey(Poll)
	active = models.BooleanField()
	budget = models.DecimalField(max_digits=10, decimal_places=2)
	def __unicode__(self):
		return self.name

class PublisherCampaign(models.Model):
	"""Módulo de gerênciamento de campanhas por publisher"""
	publisher = models.ForeignKey(Publisher)
	campaign = models.ForeignKey(Campaign)
	pricePerAction = models.DecimalField(max_digits=10, decimal_places=2)

class AdView(models.Model):
	"""Classe para registro de views de questão"""
	campaign = models.ForeignKey(Campaign)
	session = models.ForeignKey(Session)
	datetime = models.DateTimeField()

class ResultView(models.Model):
	"""Classe para registro de views de resultado"""
	campaign = models.ForeignKey(Campaign)
	session = models.ForeignKey(Session)
	datetime = models.DateTimeField()

class AdVote(models.Model):
	"""Classe computação de voto para resposta de questão"""
	campaign = models.ForeignKey(Campaign)
	session = models.ForeignKey(Session)
	choice = models.ForeignKey(Choice)
	datetime = models.DateTimeField()

class AdClick(models.Model):
	"""Classe para registro click em questão"""
	campaign = models.ForeignKey(Campaign)
	session = models.ForeignKey(Session)
	choice = models.ForeignKey(Choice)
	datetime = models.DateTimeField()

def user_registered_callback(sender, user, request, **kwargs):
	"""Método de auxílio para informações iniciais de conta"""
	profile = Account(owner = user)
	profile.publisherBalance = 0
	profile.advertiserBalance = 0
	profile.save()

user_registered.connect(user_registered_callback)
