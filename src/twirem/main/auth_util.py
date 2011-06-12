#-*- coding: utf-8 -*-

import twoauth
from . import models

class NotLogonError(Exception):
	u"""
	ログオンされていない状態を示す
	"""
	pass

_ckey = r'Uc3NTwnHkJyO4RagQSbjWg'
_csecret = r'qFeMN20eKHk6JDqGjgNffuWXvRDhmsjKBJy21Z9lksY'

def create_oauth(atoken = '', asecret = ''):
	u"""
	oauthオブジェクトを作る
	"""
	return twoauth.oauth(_ckey, _csecret, atoken, asecret)

def create_api(atoken = '', asecret = '', auth = None):
	u"""
	APIオブジェクトを作る
	"""
	if isinstance(auth, models.Authorization):
		return twoauth.api(_ckey, _csecret, auth.token, auth.token_secret)
	else:
		return twoauth.api(_ckey, _csecret, atoken, asecret)

def save_auth(req_token, oauth_verifier):
	from models import Authorization

	acc_token = create_oauth().access_token(req_token, oauth_verifier)

	try:
		user = Authorization.objects.get(user_id = acc_token['user_id'])
	except Authorization.DoesNotExist:
		user = models.Authorization(user_id = acc_token['user_id'])

	user.screen_name = acc_token['screen_name']
	user.token = acc_token['oauth_token']
	user.token_secret = acc_token['oauth_token_secret']
	user.save()

	return user

def get_auth(request):
	from models import Authorization
	try:
		return Authorization.objects.get(user_id = request.session['user_id'])
	except (Authorization.DoesNotExist, KeyError):
		raise NotLogonError()


