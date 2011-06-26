#-*- coding: utf-8 -*-

import os.path
from twirem.crawler import iconmanager
from django.http import HttpResponse

iconmanager.set_base_path(os.path.abspath(os.path.join(
	os.path.dirname(__file__),'../../../icons')))

def digest(request, digest):
	"""
	/icons/<digest>?size=full
	"""
	name = request.GET['size'] if 'size' in request.GET else 'normal'

	icon_paths = iconmanager.icon_paths(digest)

	try:
		with file(icon_paths[name], 'r') as f:
			buf = f.read()
		with file(icon_paths['mimetype'], 'r') as f:
			mimetype = f.read()
		response = HttpResponse(buf, mimetype = mimetype, status = 200)
	except IOError:
		#403
		response = HttpResponse(status = 403)
	
	return response
