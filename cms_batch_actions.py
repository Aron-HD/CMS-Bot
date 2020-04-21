from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import logging
import sys
import csv
import time
from glob import glob

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument("--start-maximized")

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

l = setup_custom_logger('logs/cms_batch_actions.log')

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
		l.info('Requested url: ' + url)
		bot.implicitly_wait(10)

		l.info(f'editing {code}, {id_from}-{id_to}')
		# first id
		IdFrom = bot.find_element_by_id('IdFrom')
		IdFrom.clear()
		IdFrom.send_keys(id_from)
		l.info(id_from)
		# last id
		IdTo = bot.find_element_by_id('IdTo')
		IdTo.clear()
		IdTo.send_keys(id_to)
		l.info(id_to)
		# selects correct award source, though this isn't strictly necessary
		bot.find_element_by_id('Source').click()
		bot.find_element_by_xpath(f'//option[@value="{code}"]').click()
		l.info(f'selected {code}')
		
		input('press key to continue: ')
		# clicks view
		bot.find_element_by_xpath('//input[@type="submit"]').click()
		l.info('clicked [View]')


	def select_ids(self, ids, remainder_IDs):
		
		bot = self.bot
		confirmed_IDs = []

		l.info('checking IDs are listed')
		# match IDs to see if they exist before ticking
		for i in ids:
			try:
				bot.find_element_by_xpath(f"//tbody/tr/td[contains(text(), '{i}')]")
				confirmed_IDs.append(i)
			except NoSuchElementException:
				remainder_IDs.append(int(i))
				l.error(
					'no such element: Unable to locate element: {"method":"xpath","selector":"//tbody/tr/td[contains(text(), '
																	+ f"'{i}'" + '}' + f'appended {i} to remaining_IDs list')

		for i in confirmed_IDs:
			try:
				tickbox = bot.find_elements_by_xpath(f"//tbody/tr/td[contains(text(), '{i}')]/../td")[0].click()
				l.info(f'{i} ticked')
			except Exception as e:
				l.info(e)

	def set_live(self):
		bot = self.bot
		bot.implicitly_wait(10)
		bot.find_element_by_id("handle-metadata-options").click()
		l.info('clicked bottom dropdown')
		bot.find_element_by_xpath('//option[@value="metadata"]').click()
		l.info("selected 'Change metadata'")
		bot.find_element_by_xpath('//button[@onclick="onManageMetadataClicked()"]').click()
		l.info('clicked [Go]')
		bot.find_element_by_xpath('//button[@onclick="onPublishAllClicked()"]').text #.click()
		l.info("clicked 'Make all items live'")
		time.sleep(5)
		bot.find_element_by_xpath('//input[@value="Save changes for all items"]').get_attribute('value') #.click()
		l.info("clicked 'Save changes for all items'")
		time.sleep(5)

def read_category(csv_file, cms, code):

	# reset IDs
	IDs = []
	remainder_IDs = []

	with open(csv_file, newline='') as f:
		r = csv.DictReader(f)
		# switch from str to int so can list low and high + append each ID to list of IDs
		[IDs.append(int(row['ID'])) for row in r]

	# FIRST LOOP
	if len(remainder_IDs) < 1:
		# get lowest and highest ID numbers
		id_from = min(IDs)
		id_to = max(IDs)
		cms.edit_ids(code, id_from, id_to)
		l.info(str(len(IDs)) + f' IDs: {IDs}')
		cms.select_ids(IDs, remainder_IDs)
		cms.set_live()

		input('press key to continue: ')

	# SECOND LOOP
	if len(remainder_IDs) > 0:
		l.info(str(len(remainder_IDs)) + f' IDs remaining: {remainder_IDs}')
		id_from = min(remainder_IDs)
		id_to = max(remainder_IDs)
		cms.edit_ids(code, id_from, id_to)
		l.info(f'editing {code}, {id_from}-{id_to}')
		cms.select_ids(remainder_IDs, [])
		cms.set_live()
		
	# input('press key to continue: ')


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
		l.info(code)
	except Exception as e:
		l.error(e)
		l.info('running main() again')
		main()

	categories = ['Social'] # tie to category

	try:
		# read shortlist / metadata csv for IDs to interact with (this will need category / award interaction)
		for cat in categories:
			csv_file = glob(fr'..\Metadata\csv\*{cat}_metadata.csv')[0]
			read_category(csv_file, cms, code)

	except Exception as e:
		l.error(e)

	# pause before exit
	time.sleep(2)
	cms.bot.quit()
	l.info('exited script correctly')

if __name__ == '__main__':
	main()