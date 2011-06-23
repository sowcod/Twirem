#-*- coding: utf-8 -*-

from models import Report
from twirem.main.models import UserProfile, q_inner
from twirem.arrayutil import Marge

def create_report(user_id, start, end):
	user = UserProfile.objects.get_or_create(user_id = user_id)

	report = Report.objects.get_or_create(
			user = user,
			start_date = start,
			end_date = end)
	
	followers_old = user.followers.filter(q_inner(start))
	followers_new = user.followers.filter(q_inner(end))

	friends_old = user.friends.filter(q_inner(start))
	friends_new = user.friends.filter(q_inner(end))

class Reporting(object):
	def __init__(self):
		pass

	
