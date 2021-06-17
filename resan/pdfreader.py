import pdfplumber
import glob


class PDFReader():
	def __init__(self, filename):
		self.fulltext = ""
		with pdfplumber.open(filename) as pdf:
			for page in pdf.pages:
				self.fulltext += page.extract_text()
		pdf.close()
	def getText(self):
		return self.fulltext
