#-*- coding: utf-8 -*-

import twoauth
from . import models

class NotLogonError(Exception):
	"""
	ログオンされていない状態を示す
	"""
	pass

_ckey = r'Uc3NTwnHkJyO4RagQSbjWg'
_csecret = r'qFeMN20eKHk6JDqGjgNffuWXvRDhmsjKBJy21Z9lksY'

def create_oauth(token = '', token_secret = ''):
	return twoauth.oauth(_ckey, _csecret, token, token_secret)

def save_auth(req_token, oauth_verifier):
	from models import Authorization

	acc_token = create_oauth().access_token(req_token, oauth_verifier)
	print(acc_token)

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


