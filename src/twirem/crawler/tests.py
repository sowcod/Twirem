#-*- coding: utf-8 -*-

from django.test import TestCase
from twirem.main.models import UserProfile
#from twirem.main.models import UserFriend
#from django.core import serializers
import db_update
import time
from django.db.models import Q

class UpdateTest(TestCase):
	fixtures = ['followers.json']
	def setup(self):
		pass

	def test_users_related_all(self):
		users = db_update.users_related(2, contains_unfollow = True)

		# 2 <- 4(unfollow)
		# 1 <- 2

		users.sort(cmp = lambda a,b: cmp(a.user_id, b.user_id))
		self.assertEquals(len(users), 2)
		self.assertEquals(users[0].user_id, 1)
		self.assertEquals(users[1].user_id, 4)

	def test_users_related(self):
		users = db_update.users_related(2) # unfollowは対象外

		# 2 <- 4(unfollow)
		# 1 <- 2

		users.sort(cmp = lambda a,b: cmp(a.user_id, b.user_id))
		self.assertEquals(len(users), 1)
		self.assertEquals(users[0].user_id, 1)

	def test_update_bios(self):
		bios = ([
			{"id":1, "screen_name":"test1", "profile_image_url":"url1"},
			{"id":2, "screen_name":"test2", "profile_image_url":"url2"},
			{"id":3, "screen_name":"test3", "profile_image_url":"url3"},
			{"id":9, "screen_name":"test9", "profile_image_url":"url9"},
			])
		db_update.update_bios(bios)

		self.assertEquals(
				UserProfile.objects.get(pk = 1).latest_bio.screen_name, 'test1')
		self.assertEquals(
				UserProfile.objects.get(pk = 1).latest_bio.icon_url, 'url1')
		self.assertEquals(
				UserProfile.objects.get(pk = 2).latest_bio.screen_name, 'test2')
		self.assertEquals(
				UserProfile.objects.get(pk = 2).latest_bio.icon_url, 'url2')
		self.assertEquals(
				UserProfile.objects.get(pk = 3).latest_bio.screen_name, 'test3')
		self.assertEquals(
				UserProfile.objects.get(pk = 3).latest_bio.icon_url, 'url3')
		self.assertEquals(
				UserProfile.objects.get(pk = 9).latest_bio.screen_name, 'test9')
		self.assertEquals(
				UserProfile.objects.get(pk = 9).latest_bio.icon_url, 'url9')
	
	def test_update_screen_names(self):
		from twirem.main.models import UserScreenName, q_inner
		names = ([
			{"id":1, "screen_name":"test1"},
			{"id":2, "screen_name":"test2"},
			{"id":3, "screen_name":"test3mod"},
			])
		db_update.update_screen_names(names)

		inner = q_inner()
		
		self.assertEquals(
				UserScreenName.objects.get(inner, user__user_id = 1).screen_name, 'test1')
		self.assertEquals(
				UserScreenName.objects.get(inner, user__user_id = 2).screen_name, 'test2')
		self.assertEquals(
				UserScreenName.objects.get(inner, user__user_id = 3).screen_name, 'test3mod')

	def test_follower_change_new_user(self):
		followers = [2,3,5]
		
		db_update.update_followers(
				user_id = u'6',
				followers = followers
				)
		try:
			user = UserProfile.objects.get(user_id = 6)
		except:
			self.fail('user not created')

		now = time.time()
		inner = Q(start_date__lte = now, end_date__gt = now)

		ufollowers = user.followers

		self.assertNotEquals(ufollowers.get(inner, user = 2).unfollow, True)
		self.assertNotEquals(ufollowers.get(inner, user = 3).unfollow, True)
		self.assertNotEquals(ufollowers.get(inner, user = 5).unfollow, True)

	def test_follower_change(self):
		# user1 was followed by 2 users.
		# user1 <- user2
		# user1 <- user3 (unfollow)
		# user1 <- user4

		# new follower is
		followers = [2,3,5]
		
		db_update.update_followers(
				user_id = 1,
				followers = followers
				)

		# Now, user1 is followed by 3 users.
		# user1 <- user2
		# user1 <- user3 (followed)
		# user1 <- user4 (unfollow)
		# user1 <- user5

		#data = serializers.serialize("json", UserFriend.objects.all())
		#print(data)

		now = time.time()
		inner = Q(start_date__lte = now, end_date__gt = now)

		ufollowers = UserProfile.objects.get(user_id = 1).followers

		self.assertNotEquals(ufollowers.get(       user = 2).unfollow, True)
		self.assertNotEquals(ufollowers.get(inner, user = 3).unfollow, True)
		self.assertEquals   (ufollowers.get(inner, user = 4).unfollow, True)
		self.assertNotEquals(ufollowers.get(inner, user = 5).unfollow, True)

	def test_follow_change(self):
		# user1 <- user4
		# user2 <- user4 (unfollow)
		# user3 <- user4

		# new friends is
		friends = [1,2,5]
		
		db_update.update_friends(
				user_id = 4,
				friends = friends
				)

		# Now, user1 is followed by 3 users.
		# user1 <- user4
		# user2 <- user4 (follow)
		# user3 <- user4 (unfollow)
		# user5 <- user4

		now = time.time()
		inner = Q(start_date__lte = now, end_date__gt = now)

		ufriends = UserProfile.objects.get(user_id = 4).friends
		self.assertNotEquals(ufriends.get(       friend = 1).unfollow, True)
		self.assertNotEquals(ufriends.get(inner, friend = 2).unfollow, True)
		self.assertEquals   (ufriends.get(inner, friend = 3).unfollow, True)
		self.assertNotEquals(ufriends.get(inner, friend = 5).unfollow, True)
