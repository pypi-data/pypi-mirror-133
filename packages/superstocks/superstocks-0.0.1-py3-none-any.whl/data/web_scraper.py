# Import packages
import json
import requests
from bs4 import BeautifulSoup


class WebScraper:

	def __init__(self, config_path: str, marker: str) -> None:
		self.config_path = config_path
		self.marker = marker

	def load_config(self) -> None:
		try:
			with open(self.config_path) as fh:
				self.config = json.load(fh)[self.marker]
		except FileNotFoundError as exp:
			raise exp

	def build_soup(self, content):
		return BeautifulSoup(content, "html.parser")

	def get_response(self, url: str):
		page = requests.get(url)

		if page.status_code != 200:
			raise Exception("Response: 200")

		return self.build_soup(page.content)
