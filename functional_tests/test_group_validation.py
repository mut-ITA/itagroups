from .base import FunctionalTest

class ValidationTest(FunctionalTest):

	def test_wrong_user_input(self):
		# Chico entra no site e tenta entrar com um grupo com tudo errado
		self.browser.get(self.server_url)

		id_ = self.create_sample_user_db("Chico", "Chico", "T18")

		username_input = self.browser.find_element_by_id('id_username_input')
		username_input.send_keys("Chico")	

		# Após preencher o username, ele clica no botão de login
		sign_in_button = self.browser.find_element_by_id('id_sign_in_button')
		self.assertEqual(
			sign_in_button.get_attribute('type'),
			'submit'			
			)
		sign_in_button.click()


		# Ele observa a pagina encontra o botao de criar um novo grupos
		# Ele pressiona o botao e surge um formulario para a criacao de grupo
		# Ele observa o formulario e o preenche conforme o desejado:
		## Nome > 27 caracteres
		# nome: Pessoas mais chatas entre todo mundo do universo todo
		## Alias nao alfanumerico
		# alias: nao entendo ingles
		## Uma tag com uma letra
		# tags: b,
		# description: Nao sei
		# Apos escrever o que desejava, conferiu e pressionou o botao de criar novo grupo.

		self.createGroupManually(	name = "Pessoas mais chatas entre todo mundo do universo todo",
									alias = "nao entendo ingles",
									tags =  "b;",
									description = "Nao sei")

		# A pagina atualiza com mensagens de erro
		errors = self.browser.find_elements_by_css_selector('.has-error')
		self.assertEqual(len(errors), 3)
		for e in errors:
			error_text = {
				'id_name_error': 'O nome do grupo deve possuir entre 3 e 27 caracteres',
				'id_alias_error': 'Minusculo, sem simbolos, sem espaço',
				'id_tags_error': 'Todas as tags devem possuir entre 3 e 12 caracteres',
			}
			e_id = e.get_attribute('id')
			if e_id:
				self.assertEqual(e.text, error_text[e_id])

		self.assertEqual(slefget_group_name_input_box().get_attribute('value'), "Pessoas")
		self.assertEqual(self.get_group_alias_input_box().get_attribute('value'), "nao")
		self.assertEqual(self.get_group_tags_input_box().get_attribute('value'), "b;")
		self.assertEqual(self.get_group_description_input_box().text, "Nao sei")

		#Chico atualiza a pagina e tenta novamente , arrumando e modificando as tags:
		self.browser.get(self.server_url)
		self.createGroupManually(	name = "Pessoas mais chatas",
									alias = "chatos",
									tags =  "tag_igual; tag_igual",
									description = "Nao sei")

		# A pagina atualiza com mensagens de erro
		error = self.browser.find_element_by_css_selector('.has-error')
		error_message = "Não podem haver tags iguais"
		self.assertEqual(error.text, error_message)

		self.assertEqual(slefget_group_name_input_box().get_attribute('value'), "Pessoas")
		self.assertEqual(self.get_group_alias_input_box().get_attribute('value'), "chatos")
		self.assertEqual(self.get_group_tags_input_box().get_attribute('value'), "tag_igual;")
		self.assertEqual(self.get_group_description_input_box().text, "Nao sei")

		# Chico agora lembra de um grupo que tinha visto, e achou que o botao de criar servia para entrar em grupos
		# Ele criou um grupo com um nome que ja existia

		self.fail("Finish the test")
