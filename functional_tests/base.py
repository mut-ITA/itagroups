import sys
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from groups.models import Group, User

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

	def get_group_name_input_box(self):
		return self.browser.find_element_by_id('id_name')

	def get_group_alias_input_box(self):
		return self.browser.find_element_by_id('id_alias')

	def get_group_tags_input_box(self):
		return self.browser.find_element_by_id('id_tags')

	def get_group_description_input_box(self):
		return self.browser.find_element_by_id('id_description')

	def createGroupManually(self, name, alias, tags, description):
		create_group_button = self.browser.find_element_by_id('id_create_group')
		self.assertEqual(
			create_group_button.get_attribute('type'),
			'button'
			)

		create_group_button.click()

		group_name_input = self.get_group_name_input_box()
		group_name_input.send_keys(name)

		group_alias_input = self.get_group_alias_input_box()
		group_alias_input.send_keys(alias)

		group_tags_input = self.get_group_tags_input_box()
		group_tags_input.send_keys(tags)

		group_description_input = self.get_group_description_input_box()
		group_description_input.send_keys(description)

		create_group_button = self.browser.find_element_by_id('id_create_new_group')
		self.assertEqual(
			create_group_button.get_attribute('type'),
			'submit'
			)
		create_group_button.click()
		self.browser.implicitly_wait(5)


	def create_sample_group_db(self, name, alias, tags, description):
		sample_group = Group()
		sample_group.name = name
		sample_group.alias = alias
		sample_group.tags = tags
		sample_group.description = description
		sample_group.save()

	def create_sample_user_db(self, access_token, apelido, turma):
		sample_user = User()
		sample_user.access_token = access_token
		sample_user.apelido = apelido
		sample_user.turma = turma
		sample_user.save()

		return sample_user.id
