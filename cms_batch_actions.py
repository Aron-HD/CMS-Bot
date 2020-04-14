from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
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
		url = 'http://newcms.warc.com/content/batch-actions'
		bot.get(url)
		logger.info('Requested url: ' + url)
		bot.implicitly_wait(5)

		logger.info(f'editing {code}, {id_from}-{id_to}')
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


	def select_ids(self, ids, remainder_IDs):
		
		bot = self.bot
		confirmed_IDs = []

		logger.info('checking IDs are listed')
		# match IDs to see if they exist before ticking
		for i in ids:
			try:
				bot.find_element_by_xpath(f"//tbody/tr/td[contains(text(), '{i}')]")
				confirmed_IDs.append(i)
			except NoSuchElementException:
				remainder_IDs.append(int(i))
				logger.error(
					'no such element: Unable to locate element: {"method":"xpath","selector":"//tbody/tr/td[contains(text(), '
																	+ f"'{i}'" + '}' + f'appended {i} to remaining_IDs list')

		for i in confirmed_IDs:
			try:
				tickbox = bot.find_elements_by_xpath(f"//tbody/tr/td[contains(text(), '{i}')]/../td")[0].click()
				logger.info(f'{i} ticked')
			except Exception as e:
				logger.info('')

	def set_live(self):
		pass

def main():

	cms = CMSBot()

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
		logger.error(e)
		logger.info('running main() again')
		main()

	# split into function
	try:
		# read shortlist / metadata csv for IDs to interact with (this will need category / award interaction)
		csv_file = r'..\Metadata\csv\Content_metadata.csv'

		with open(csv_file, newline='') as f:
			r = csv.DictReader(f)
			IDs = []
			# switch from str to int so can list low and high + append each ID to list of IDs
			[IDs.append(int(row['ID'])) for row in r]
	
		remainder_IDs = []

		# FIRST LOOP
		if len(remainder_IDs) < 1:
			# get lowest and highest ID numbers
			id_from = min(IDs)
			id_to = max(IDs)
			cms.edit_ids(code, id_from, id_to)
			logger.info(str(len(IDs)) + f' IDs: {IDs}')
			cms.select_ids(IDs, remainder_IDs)

		# SECOND LOOP
		if len(remainder_IDs) > 0:
			logger.info(str(len(remainder_IDs)) + f' IDs remaining: {remainder_IDs}')
			id_from = min(remainder_IDs)
			id_to = max(remainder_IDs)
			cms.edit_ids(code, id_from, id_to)
			logger.info(f'editing {code}, {id_from}-{id_to}')
			cms.select_ids(remainder_IDs, [])
			# reset IDs
			remainder_IDs = []

	except Exception as e:
		logger.error(e)

	# pause before exit
	time.sleep(3)
	cms.bot.quit()
	logger.info('exited script correctly')

if __name__ == '__main__':
	main()