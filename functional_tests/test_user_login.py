from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class LoginTests (FunctionalTest):
	
	def test_can_sign_in(self):
		# Moller entra no site e decide se cadastrar.
		self.browser.get(self.server_url)

		# Ele acha o lugar de colocar seu username e o preenche

		username_input = self.browser.find_element_by_id('id_username_input')
		username_input.send_keys("Moller")	

		# Após preencher o username, ele clica no botão de login
		sign_in_button = self.browser.find_element_by_id('id_sign_in_button')
		self.assertEqual(
			sign_in_button.get_attribute('type'),
			'submit'			
			)
		sign_in_button.click()

		# Como era sua primeira vez logando no site, um formulário surgiu para que completasse
		# com suas informações ITA

		apelido_input = self.browser.find_element_by_id('id_apelido_input')

		turma_input = self.browser.find_element_by_id('id_turma_input')

		submit_button = self.browser.find_element_by_id('id_submit_information')		
		self.assertEqual(
			submit_button.get_attribute('type'),
			'submit'			
			)


		# Ele preenche suas informações e as envia

		apelido_input.send_keys("Padabixo")
		
		turma_input.send_keys("T17")

		submit_button.click()
		self.browser.implicitly_wait(10)

		# Satisfeito com o cadastro, ele verifica se já se encontra logado na página
		
		greeting_text = self.browser.find_element_by_id('id_greeting_text')

		self.assertIn('Bem vindo, Moller', greeting_text.text)