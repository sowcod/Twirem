#-*- coding: utf-8 -*-

from django.db import models

class Authorization(models.Model):
	user_id = models.CharField(max_length = 20, primary_key = True)
	screen_name = models.CharField(max_length = 20)
	token = models.CharField(max_length = 100, blank = True)
	token_secret = models.CharField(max_length = 100, blank = True)

