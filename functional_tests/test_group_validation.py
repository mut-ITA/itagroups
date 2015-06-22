from .base import FunctionalTest
from unittest import skip

class ValidationTest(FunctionalTest):	
	@skip
	def test_wrong_user_input(self):
		# Chico entra no site e tenta entrar com um grupo com tudo errado
		# Nome > 27 caracteres
		# Alias nao alfanumerico
		# Uma tag com uma letra

		# A pagina recarrega com as mensagens de erro para cada uma
		self.fail("Finish writing!")
