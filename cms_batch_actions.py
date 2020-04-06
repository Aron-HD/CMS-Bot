from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import logging
import sys
import csv
import time

chrome_options = Options()
# chrome_options.add_argument('--headless')

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%d-%m-%Y %H:%M:%S')
    handler = logging.FileHandler(name, mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger

logger = setup_custom_logger('logs/cms_batch_actions.log')

codes = {
'warc': 'WARC-AWARDS',
'mena': 'Warc-Prize-Mena',
'asia': 'Warc-Prize-Asia',
'media': 'Warc-Awards-Media'
}

class CMSBot:
	def __init__(self):
		self.bot = webdriver.Chrome(options=chrome_options, executable_path=r"C:\Users\arondavidson\AppData\Local\Programs\Python\Python37\chromedriver.exe")
		

	def edit_ids(self, code, id_from, id_to):
		bot = self.bot
		# bot.maximize_window()
		url = 'http://newcms.warc.com/content/batch-actions'
		bot.get(url) # log
		logger.info('Requested: ' + url)
		bot.implicitly_wait(5)
		# first id
		IdFrom = bot.find_element_by_id('IdFrom')
		IdFrom.clear()
		IdFrom.send_keys(id_from)
		logger.info(id_from)
		# last id
		IdTo = bot.find_element_by_id('IdTo')
		IdTo.clear()
		IdTo.send_keys(id_to)
		logger.info(id_to)
		# selects correct award source, though this isn't strictly necessary
		source = bot.find_element_by_id('Source').click()
		option = bot.find_element_by_xpath(f'//option[@value="{code}"]').click()
		logger.info(f'selected {code}')
		# clicks view
		bot.find_element_by_xpath('//input[@type="submit"]').click() # //div[@class="col-md-10 col-lg-9 col-xl-12 form-buttons mt-medium-space mt-xl-0"]
		logger.info('clicked [View]')


	def select_ids(self, id_from, id_to):

		def ids():
			ids = [id_from, id_to]
			return ids

		bot = self.bot
		
		for i in ids():
		# table = bot.find_element_by_id("content-metadata-table")
			data = bot.find_elements_by_xpath('//table/tbody/tr/td[text()]')
			[print(d) for d in data]

		# logger.info('ticked id')

def main():

	cms = CMSBot()

	id_from = 131385 # int(input('\n\tID RANGE\n- from: '))
	id_to = 131607 # int(input('- to: '))

	selector = 1 # int(input(f'''
	# FUNCTIONS
	# '1' - warc awards
	# '2' - mena prize
	# '3' - asia prize
	# '4' - media awards

	# Select: '''))

	if selector == 1:
		award = 'warc'
	if selector == 2:
		award = 'mena'
	if selector == 3:
		award = 'asia'
	if selector == 4:
		award = 'media'
	if selector not in range(1,5):
		print(f'\n{selector} was not a valid selection\n')

	try:
		code = codes[f'{award}']
		logger.info(code)
	except Exception as e:
		logger.error(e, '\nrunning main() again')
		main()

	try:
		cms.edit_ids(code, id_from, id_to)
		logger.info(f'editing {code}, {id_from}-{id_to}')
		cms.select_ids(id_from, id_to)
	except Exception as e:
		logger.error(e)

	# pause before exit
	time.sleep(5)
	cms.bot.quit()
	logger.info('exited script correctly')

if __name__ == '__main__':
	main()