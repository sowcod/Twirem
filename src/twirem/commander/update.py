#-*- coding:utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
#from django.http import HttpResponseRedirect
from twirem.main import auth_util
from twirem.main.models import UserFriend,UserScreenName

def reset(request):
	UserFriend.objects.all().delete()
	UserScreenName.objects.all().delete()
	return render_to_response('main/member.html')

def friend(request):
	from twirem.crawler import UserInfoRequester
	from twirem.crawler.update import update_friends, users_noactivity, update_screen_names
	u"""
	フレンド更新
	"""
	try :
		auth = auth_util.get_auth(request)
		api = auth_util.create_api(auth = auth)
		requester = UserInfoRequester(api)

		new_friends = requester.request_friend_ids(auth.user_id)
		update_friends(auth.user_id, new_friends)

		users = [str(user.user_id) for user 
				in users_noactivity(auth.user_id) if user.activity == 0]
		update_users = sorted(requester.lookup(users),
				cmp = lambda a,b:cmp(a['id'], b['id']))
		update_screen_names(update_users)

		friends = UserFriend.objects.filter()

		#ids = FollowerIds(api, user_id = auth.user_id)
		#users = FollowerUsers(api, user_id = auth.user_id)
		#values = {'user' : auth, 'ids' : ids, 'users' : users}
		values = {'user' : auth, 'friends' : friends}
		return render_to_response(
				'main/member.html',
				values,
				RequestContext(request))
	except auth_util.NotLogonError :
		return render_to_response('main/top.html')
