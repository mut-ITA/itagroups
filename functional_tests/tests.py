from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase

import unittest

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_create_a_group_and_other_join_it_later(self):
		# Um aluno do ita quer criar um grupo novo usando
		# o site recomendado pelos veteranoes. Ele vai para a pagina inicial
		self.browser.get(self.live_server_url)

		# Ele percebe que tanto o titulo quanto o header se referem ao ITA
		self.assertIn('ITA', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('ITA', header_text)

		# Ele observa a pagina encontra o botao de criar um novo grupo
		create_group_button = self.browser.find_element_by_id('id_create_group')		
		self.assertEqual(
			create_group_button.get_attribute('type'),
			'button'			
			)

		# Ele pressiona o botao e surge um formulario para a criacao de grupo


		# Ele observa o formulario e o preenche conforme o desejado:
		# nome: Testadores do H8
		group_name_input = self.browser.find_element_by_id('id_group_name')
		group_name_input.send_keys("Testadores no H8")

		# alias: h8testers
		group_alias_input = self.browser.find_element_by_id('id_group_alias')
		group_alias_input.send_keys("h8testers")

		# tags: TDD, test
		group_tags_input = self.browser.find_element_by_id('id_group_tags')
		group_tags_input.send_keys("TDD; test;")

		# description: Um grupo maneiro de aprender a testar
		group_description_input = self.browser.find_element_by_id('id_group_description')
		group_description_input.send_keys("Um grupo maneiro de aprender a testar")

		# Apos escrever o que desejava, conferiu e pressionou o botao de criar novo grupo.
		create_group_button = self.browser.find_element_by_id('id_create_new_group')		
		self.assertEqual(
			create_group_button.get_attribute('type'),
			'submit'			
			)
		create_group_button.click()

		# Acreditando que o grupo foi criado corretamente, ele saiu da pagina
		# Outro usuario, Mutante, entra no site querendo entrar num grupo de testadores

		## Abrimos outro browser para simular o fato de ser um novo usuario
		self.browser.quit()
		self.browser = webdriver.Firefox()
		self.browser.get(self.live_server_url)
		self.browser.implicitly_wait(3)

		# Ele entra no site e visualiza uma caixa de texto com um botao de pesquisa do lado
		search_input = self.browser.find_element_by_id('id_search_group')
		search_button = self.browser.find_element_by_id('id_search_button')
		# Interessado em aprender TDD, Gustavo entra com "TDD" na barra de pesquisa e aperta o botao
		search_input.send_keys("TDD")
		search_button.click()

		# A pagina atualiza, agora mostrando uma lista de grupos com apenas um elemento        
		# Tal elemento é o grupo criado recentemente pelo outro aluno
		table 	= self.browser.find_element_by_id('id_search_list')
		rows = table.find_elements_by_tag_name('tr')
		columns = []
		for r in rows:
			columns += r.find_elements_by_tag_name('td')
		self.assertIn('Testadores no H8', [col.text for col in columns])

		# Gustavo observa a pagina e clica no link para ver mais detalhes sobre o grupo 

		# Apos ser redirecionado para a pagina do grupo, Gustavo, satisfeito com a descricao,
		# pressiona o botao de entrar no grupo
        
		# Confiando no funcionamento do site, Gustavo volta às suas atividades


		self.fail("Finish the test! Add Popup!")