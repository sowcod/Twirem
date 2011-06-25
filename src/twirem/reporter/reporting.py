#-*- coding: utf-8 -*-

from models import Report, DiffScreenName, DiffIcon
from twirem.main.models import UserProfile, q_inner
from twirem.main.models import UserScreenName, UserIcon
from twirem.arrayutil import Marge
import time

def create_new_report(user_id, end = None):
	if end is None: end = time.time()

	try:
		last_date  = Report.objects.select_related('user').latest('start_date').end_date
	except Report.DoesNotExist:
		last_date = end
	
	return create_report(user_id, last_date, end)

def create_report(user_id, start, end):
	user = UserProfile.objects.get_or_create(user_id = user_id)[0]

	report = Report.objects.select_related('user').get_or_create(
			user = user,
			start_date = start,
			end_date = end)[0]

	attach_followers(report)
	attach_friends(report)
	attach_screen_name(report)
	attach_icon(report)

	report.save()

	return report

def attach_followers(report):
	followers = report.followers
	user = report.user
	oldf = user.followers.filter(q_inner(report.start_date), unfollow = False).order_by('user')
	newf = user.followers.filter(q_inner(report.end_date), unfollow = False).order_by('user')

	m = Marge(oldf, newf, lambda a,b: cmp(a.user_id, b.user_id))

	m.full(left = lambda l: followers.create(user = l.user, remove = True),
			right = lambda r: followers.create(user = r.user, remove = False))

	return followers

def attach_friends(report):
	friends = report.friends
	user = report.user
	oldf = user.friends.filter(q_inner(report.start_date), unfollow = False).order_by('friend')
	newf = user.friends.filter(q_inner(report.end_date), unfollow = False).order_by('friend')

	m = Marge(oldf, newf, lambda a,b: cmp(a.friend_id, b.friend_id))

	m.full(left = lambda l: friends.create(user = l.friend, remove = True),
			right = lambda r: friends.create(user = r.friend, remove = False))

	return friends

def attach_screen_name(report):
	user = report.user
	try:
		new = user.screen_names.get(q_inner(report.end_date))
	except UserScreenName.DoesNotExist:
		new = None

	try:
		old = user.screen_names.get(q_inner(report.start_date))
	except UserScreenName.DoesNotExist:
		old = None

	if new == None: names = DiffScreenName(report = report, diff_type = 'N')
	elif old == None: names = DiffScreenName(report = report, new = new, diff_type = 'E')
	elif old.screen_name == new.screen_name:
		names = DiffScreenName(report = report, old = old, new = new, diff_type = 'E')
	else:
		names = DiffScreenName(report = report, old = old, new = new, diff_type = 'C')

	names.save()
	report.screen_names = names

	return names

def attach_icon(report):
	user = report.user
	try:
		newi = user.icons.get(q_inner(report.end_date))
	except UserIcon.DoesNotExist:
		newi = None
		 
	try:
		oldi = user.icons.get(q_inner(report.start_date))
	except UserIcon.DoesNotExist:
		oldi = None

	if newi == None: icons = DiffIcon(report = report, diff_type = 'N')
	elif oldi == None: icons = DiffIcon(report = report, new = newi, diff_type = 'E')
	elif oldi.digest == newi.digest:
		icons = DiffIcon(report = report, old = oldi, new = newi, diff_type = 'E')
	else:
		icons = DiffIcon(report = report, old = oldi, new = newi, diff_type = 'C')
	
	icons.save()
	report.icons = icons

	return icons

