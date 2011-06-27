#-*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'../..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'twirem.settings'

from twirem.main.models import UserFriend, UserScreenName, UserIcon

def processUserFriend():
	friends = UserFriend.objects.all().values('user', 'friend').distinct()
	for friend in friends:
		setUserFriendStart(friend['user'], friend['friend'])

def setUserFriendStart(user_id, friend_id):
	friend = UserFriend.objects.filter(user = user_id, friend = friend_id).order_by('start_date')[0]
	friend.start_date = 0
	friend.save()

def processUserScreenName():
	users = UserScreenName.objects.all().values('user').distinct()
	for user in users:
		setUserScreenNameStart(user['user'])

def setUserScreenNameStart(user_id):
	name = UserScreenName.objects.filter(user = user_id).order_by('start_date')[0]
	name.start_date = 0
	name.save()


def processUserIcon():
	users = UserIcon.objects.all().values('user').distinct()
	for user in users:
		setUserIconStart(user['user'])

def setUserIconStart(user_id):
	icon = UserIcon.objects.filter(user = user_id).order_by('start_date')[0]
	icon.start_date = 0
	icon.save()

processUserFriend()
processUserScreenName()
processUserIcon()
