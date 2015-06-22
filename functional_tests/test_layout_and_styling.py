from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):

	def test_layout_and_styling(self):
		# Philip vai para a pagina inicial
		self.browser.get(self.server_url)
		self.browser.set_window_size(1024, 768)

		# Ele percebe a barra de pesquisas centralizada
		search_input = self.browser.find_element_by_id('id_search_form')
		self.assertAlmostEqual(
			search_input.location['x'] + search_input.size['width'] / 2,
			512,
			delta = 50
		)