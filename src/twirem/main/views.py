#-*- coding:utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from . import auth_util

def access_token(request):
	u"""
	アクセストークンの取得
	"""
	oauth = auth_util.create_oauth()
	req_token = oauth.request_token()
	url = oauth.authorize_url(req_token)
	request.session['req_token'] = req_token

	return HttpResponseRedirect(url)

def auth(request):
	u"""
	OAuth認証からのリダイレクトされたとき
	認証情報を保存して個人ページに飛ぶ
	"""
	auth = auth_util.save_auth(request.session['req_token'],
			request.GET['oauth_verifier'])

	request.session['user_id'] = auth.user_id
	del request.session['req_token']
	
	return HttpResponseRedirect('/')

def logout(request):
	u"""
	ログアウト
	セッションを削除してトップページに移動するだけ。
	DBに保存された認証情報等はそのまま。
	"""
	request.session.clear()

	return HttpResponseRedirect('/')

def toppage(request):
	u"""
	トップページへのアクセス
	ログイン状態であれば個人ページを表示
	そうでなければトップページを表示
	"""
	try :
		user = auth_util.get_auth(request)
		values = {'user' : user}
		return render_to_response(
				'main/member.html',
				values,
				RequestContext(request))
	except auth_util.NotLogonError :
		return render_to_response('main/top.html')
	

