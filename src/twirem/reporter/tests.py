#-*- coding: utf-8 -*-

from django.test import TestCase
import reporting

class ReportingTest(TestCase):
	"""
	100 - 200
	2 -> 1
	3 -> 1
	     1 -> 2
	     1 -> 4

	200 - 300
	name: "user200"
	url: "http://example.com/icon200"
	digest: "digest200"
	3 -x 1
	     1 -x 2

	300 - 400
	name: "user300"
	url: "http://example.com/icon200"
	digest: "digest300"
	4 -> 1
	     1 -> 3

	"""

	fixtures = ['reporting.json']

	def test_report_nochange1(self):
		report = reporting.create_report(user_id = 1, start = 110, end = 130)
		self.assertEquals(report.followers.count(), 0)
		self.assertEquals(report.friends.count(), 0)
		self.assertEquals(report.screen_names.diff_type, 'N')
		self.assertEquals(report.icons.diff_type, 'N')

	def test_report_nochange2(self):
		report = reporting.create_report(user_id = 1, start = 210, end = 230)
		self.assertEquals(report.followers.count(), 0)
		self.assertEquals(report.friends.count(), 0)
		self.assertEquals(report.screen_names.diff_type, 'E')
		self.assertEquals(report.icons.diff_type, 'E')
		
	def test_report_change1_2(self):
		report = reporting.create_report(user_id = 1, start = 100, end = 230)
		self.assertEquals(report.followers.count(), 1)
		self.assertEquals(report.followers.all()[0].user_id, 3)
		self.assertEquals(report.followers.all()[0].remove, True)
		self.assertEquals(report.friends.count(), 1)
		self.assertEquals(report.friends.all()[0].user_id, 2)
		self.assertEquals(report.friends.all()[0].remove, True)
		self.assertEquals(report.screen_names.diff_type, 'E')
		self.assertEquals(report.screen_names.new.screen_name, 'user200')
		self.assertEquals(report.icons.diff_type, 'E')
		self.assertEquals(report.icons.new.digest, 'digest200')

	def test_report_change2_3(self):
		report = reporting.create_report(user_id = 1, start = 200, end = 330)
		self.assertEquals(report.followers.count(), 1)
		self.assertEquals(report.followers.all()[0].user_id, 4)
		self.assertNotEquals(report.followers.all()[0].remove, True)
		self.assertEquals(report.friends.count(), 1)
		self.assertEquals(report.friends.all()[0].user_id, 3)
		self.assertNotEquals(report.friends.all()[0].remove, True)
		self.assertEquals(report.screen_names.diff_type, 'C')
		self.assertEquals(report.screen_names.old.screen_name, 'user200')
		self.assertEquals(report.screen_names.new.screen_name, 'user300')
		self.assertEquals(report.icons.diff_type, 'C')
		self.assertEquals(report.icons.old.digest, 'digest200')
		self.assertEquals(report.icons.new.digest, 'digest300')
		
	def test_report_change1_3(self):
		report = reporting.create_report(user_id = 1, start = 100, end = 330)
		self.check1_3(report)
		"""
		followers = report.followers.all().order_by('user')
		self.assertEquals(followers.count(), 2)
		self.assertEquals(followers[0].user_id, 3)
		self.assertEquals(followers[0].remove, True)
		self.assertEquals(followers[1].user_id, 4)
		self.assertNotEquals(followers[1].remove, True)

		friends = report.friends.all().order_by('user')
		self.assertEquals(friends.count(), 2)
		self.assertEquals(friends[0].user_id, 2)
		self.assertEquals(friends[0].remove, True)
		self.assertEquals(friends[1].user_id, 3)
		self.assertNotEquals(friends[1].remove, True)

		self.assertEquals(report.screen_names.diff_type, 'E')
		self.assertEquals(report.screen_names.new.screen_name, 'user300')

		self.assertEquals(report.icons.diff_type, 'E')
		self.assertEquals(report.icons.new.digest, 'digest300')
		"""
	
	def check1_3(self, report):
		followers = report.followers.all().order_by('user')
		self.assertEquals(followers.count(), 2)
		self.assertEquals(followers[0].user_id, 3)
		self.assertEquals(followers[0].remove, True)
		self.assertEquals(followers[1].user_id, 4)
		self.assertNotEquals(followers[1].remove, True)

		friends = report.friends.all().order_by('user')
		self.assertEquals(friends.count(), 2)
		self.assertEquals(friends[0].user_id, 2)
		self.assertEquals(friends[0].remove, True)
		self.assertEquals(friends[1].user_id, 3)
		self.assertNotEquals(friends[1].remove, True)

		self.assertEquals(report.screen_names.diff_type, 'E')
		self.assertEquals(report.screen_names.new.screen_name, 'user300')

		self.assertEquals(report.icons.diff_type, 'E')
		self.assertEquals(report.icons.new.digest, 'digest300')

	def test_report_start(self):
		report = reporting.create_new_report(user_id = 1, end = 100)
		followers = report.followers.all().order_by('user')
		self.assertEquals(followers.count(), 0)
		friends = report.friends.all().order_by('user')
		self.assertEquals(friends.count(), 0)

		self.assertEquals(report.screen_names.diff_type, 'N')
		self.assertEquals(report.icons.diff_type, 'N')

		self.check1_3(reporting.create_new_report(user_id = 1, end = 320))
