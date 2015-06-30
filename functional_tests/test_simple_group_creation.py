from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):

	def test_can_create_a_group_and_other_join_it_later(self):
		# Um aluno do ita quer criar um grupo novo usando
		# o site recomendado pelos veteranoes. Ele vai para a pagina inicial
		self.browser.get(self.server_url)

		# Ele percebe que tanto o titulo quanto o header se referem ao ITA
		self.assertIn('ITA', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('ITA', header_text)

		# Ele observa a pagina encontra o botao de criar um novo grupos		
		# Ele pressiona o botao e surge um formulario para a criacao de grupo
		# Ele observa o formulario e o preenche conforme o desejado:
		# nome: Testadores do H8
		# alias: h8testers
		# tags: TDD, test
		# description: Um grupo maneiro de aprender a testar
		# Apos escrever o que desejava, conferiu e pressionou o botao de criar novo grupo.

		self.createGroupManually(	name = "Testadores no H8",
									alias = "h8testers",
									tags =  "TDD; test",
									description = "Um grupo maneiro de aprender a testar")


		# Agora ele deseja saber se o grupo foi criado corretamente
		# Ele olha para o site e visualiza uma caixa de texto com um botao de pesquisa do lado

		search_input = self.browser.find_element_by_id('id_search_group')
		search_button = self.browser.find_element_by_id('id_search_button')

		# Como possuia a tag TDD ele pesquisa por essa tag
		search_input.send_keys("TDD")
		search_button.click()

		# A pagina atualiza, agora mostrando uma lista de grupos com apenas um elemento        
		# Tal elemento é o grupo criado recentemente por ele
		table 	= self.browser.find_element_by_id('id_search_list')
		rows = table.find_elements_by_tag_name('tr')
		columns = []
		for r in rows:
			columns += r.find_elements_by_tag_name('td')
		self.assertIn('Testadores no H8', [col.text for col in columns])

		# Ele observa a pagina e clica no link para ver mais detalhes sobre o grupo 

		table 	= self.browser.find_element_by_id('id_search_list')
		rows = table.find_elements_by_tag_name('tr')
		columns = []
		for r in rows:
			columns += r.find_elements_by_id('table_alias')
			columns += r.find_elements_by_id('table_view_button')
		for col in columns:
			if col.text == 'h8testers':
				view_group_button = columns[columns.index(col) + 1]
		
		view_group_button.click()

		self.assertIn(self.browser.current_url, self.server_url + '/groups/h8testers/')

		# Apos ser redirecionado para a pagina do grupo
		# ele observa que o titulo contem o nome do grupo e fica satisfeito
		
		self.assertIn('ITA', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Testadores no H8', header_text)

