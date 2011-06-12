#-*- coding:utf-8 -*-

class PageListingApi(object):
	listKey = ''

	def __init__(self, api, user_id = '', user = None):
		if user is not None:
			self.user_id = user.user_id
		else:
			self.user_id = user_id
		self.api = api

	def __iter__(self):
		next_cursor = -1
		while True :
			resultList = self.apiFunc(next_cursor)
			for user in resultList[self.__class__.listKey]:
				yield user
			next_cursor = resultList['next_cursor']
			if resultList['next_cursor'] <= 0:
				break

	def apiFunc(self, cursor = -1):
		pass

class FollowerIds(PageListingApi):
	listKey = 'ids'

	def apiFunc(self, cursor = -1):
		u"""
		{
			previous_cursor:0,
			ids:[1,2,3,...],
			previous_cursor:
			next_cursor:0
		}
		"""
		return self.api.followers_ids(self.user_id, auth = True, cursor = cursor)

class FollowerUsers(PageListingApi):
	listKey = 'users'

	def apiFunc(self, cursor = -1):
		u"""
		{
			...
		}
		"""
		return self.api.followers(self.user_id, auth = True, cursor = cursor)

class FriendIds(PageListingApi):
	listKey = 'ids'

	def apiFunc(self, cursor = -1):
		u"""
		{
			previous_cursor:0,
			ids:[1,2,3,...],
			previous_cursor:
			next_cursor:0
		}
		"""
		return self.api.friends_ids(self.user_id, auth = True, cursor = cursor)
