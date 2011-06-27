#-*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'../..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'twirem.settings'

from twirem.main.models import UserFriend, UserScreenName, UserIcon

def processUserFriend():
	friends = UserFriend.objects.all().values('user_id', 'friend_id').distinct()
	for friend in friends:
		setUserFriendStart(friends['user_id'], friends['friend_id'])

def setUserFriendStart(user_id, friend_id):
	friend = UserFriend.objects.filter(user_id = user_id, friend_id = friend_id).order_by('start_date')[0]
	print(friend.user_id, friend._friend_id, friend.start_date)


def processUserScreenName():
	users = UserScreenName.objects.all().values('user_id').distinct()
	for user in users:
		setUserScreenNameStart(user['user_id'])

def setUserScreenNameStart(user_id):
	name = UserScreenName.objects.filter(user_id = user_id).order_by('start_date')[0]
	print(name.screen_name, name.start_date)


def processUserIcon():
	users = UserIcon.objects.all().values('user_id').distinct()
	for user in users:
		setUserIconStart(user['user_id'])

def setUserIconStart(user_id):
	icon = UserIcon.objects.filter(user_id = user_id).order_by('start_date')[0]
	print(icon.digest, icon.start_date)

processUserFriend()
processUserScreenName()
processUserIcon()
