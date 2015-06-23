import sys
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class FunctionalTest(StaticLiveServerTestCase):
	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url = 'http://' + arg.split('=')[1]
				return
		super().setUpClass()
		cls.server_url = cls.live_server_url

	@classmethod
	def tearDownClass(cls):
		if cls.server_url == cls.server_url:
			super().tearDownClass()

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def createGroupManually(self, name, alias, tags, description):
		create_group_button = self.browser.find_element_by_id('id_create_group')
		if create_group_button:
			self.assertEqual(
				create_group_button.get_attribute('type'),
				'button'			
				)

			create_group_button.click()

		group_name_input = self.browser.find_element_by_id('id_group_name')
		group_name_input.send_keys(name)

		group_alias_input = self.browser.find_element_by_id('id_group_alias')
		group_alias_input.send_keys(alias)

		group_tags_input = self.browser.find_element_by_id('id_group_tags')
		group_tags_input.send_keys(tags)

		group_description_input = self.browser.find_element_by_id('id_group_description')
		group_description_input.send_keys(description)

		create_group_button = self.browser.find_element_by_id('id_create_new_group')		
		self.assertEqual(
			create_group_button.get_attribute('type'),
			'submit'			
			)
		create_group_button.click()
		self.browser.implicitly_wait(5)
