from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class JoinGroupTest(FunctionalTest):

	def test_can_join_group(self):

		# Philip loga na sua conta no site
		## Como ele já possui conta, adicionamos ele diretamente ao banco de dados para o teste.
		id_ = self.create_sample_user_db("Philip", "Ancora", "T17")
		self.create_sample_group_db("Carniceria", "bateria", "barulho", "Muito barulho")

		self.browser.get(self.server_url)

		username_input = self.browser.find_element_by_id('id_username_input')
		username_input.send_keys("Philip")	

		sign_in_button = self.browser.find_element_by_id('id_sign_in_button')
		self.assertEqual(
			sign_in_button.get_attribute('type'),
			'submit'			
			)
		sign_in_button.click()

		# Como ele gosta muito de batucar, ele procura o grupo da bateria(Carniceria)

		search_input = self.browser.find_element_by_id('id_search_group')
		search_button = self.browser.find_element_by_id('id_search_button')

		search_input.send_keys("Carniceria")
		search_button.click()

		table 	= self.browser.find_element_by_id('id_search_list')
		rows = table.find_elements_by_tag_name('tr')
		columns = []
		for r in rows:
			columns += r.find_elements_by_id('table_alias')
			columns += r.find_elements_by_id('table_view_button')
		for col in columns:
			if col.text == 'bateria':
				view_group_button = columns[columns.index(col) + 1]
		
		view_group_button.click()

		# Ele entra na página do grupo e clica no botão de participar do grupo

		join_group_button = self.browser.find_element_by_id('id_join_group')
		join_group_button.click()

		# Ele nota que seu nota foi adicionado na lista de membros

		members_table = self.browser.find_element_by_id('id_members_list')
		rows = members_table.find_elements_by_tag_name('tr')
		columns = []
		for r in rows:
			columns += r.find_elements_by_tag_name('td')

		self.assertIn('Philip', [col.text for col in columns])
		self.assertIn('Ancora', [col.text for col in columns])
		self.assertIn('T17', [col.text for col in columns])

		# Ele entra na sua página de usuário e verifica que Carniceria está presente nos seus grupos

		self.browser.get(self.server_url + '/users/'+ str(id_) + '/')

		groups_table = self.browser.find_element_by_id('id_groups_list')
		rows = groups_table.find_elements_by_tag_name('tr')
		columns = []
		for r in rows:
			columns += r.find_elements_by_tag_name('td')

		self.assertIn('Carniceria', [col.text for col in columns])

		