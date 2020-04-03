from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv
import time
import logging
import sys
chrome_options = Options()
chrome_options.add_argument('--headless')

# Setup logging
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

logger = setup_custom_logger('log.txt')

class CMSBot:
	def __init__(self):
		self.bot = webdriver.Chrome(options=chrome_options, executable_path=r"C:\Users\arondavidson\AppData\Local\Programs\Python\Python37\chromedriver.exe")

	def edit_id(self, ID):
		bot = self.bot
		bot.maximize_window()
		url = 'http://newcms.warc.com/content/edit'
		bot.get(url) # log
		logger.info(f"requested url: '{url}'")
		bot.implicitly_wait(5)
		legid = bot.find_element_by_name('LegacyId')
		legid.clear()
		legid.send_keys(ID)
		logger.info(f'edit {ID}')
		legid.send_keys(Keys.RETURN)
		# bot.execute_script("document.body.style.zoom='67%'") # this seems to mess with clicks
		time.sleep(1)

	def save_changes(self):
		bot = self.bot
		bot.find_element_by_xpath('//span[@onclick="onSaveClicked()"]').click()
		logger.info('Saved changes')

	def generate_bullets(self):
		bot = self.bot
		bot.find_element_by_link_text('Summary').click()
		logger.info("clicked [Summary] (Expand)")
		bot.find_element_by_id('GenerateBullets').click()
		logger.info("clicked [Generate Bullets]")

	def additional_info(self, award):
		bot = self.bot
		info = bot.find_element_by_id('AdditionalInformation')
		value = info.get_attribute('value')
		logger.info('additional info - ' + value.replace('Shortlisted, ',''))
		info.clear()
		info.send_keys(award + ', ' + value.replace('Shortlisted, ',''))
		logger.info('appending - ' + award)
		new_info = bot.find_element_by_id('AdditionalInformation').get_attribute('value')
		logger.info('additional info - ' + new_info)
		
	def add_video(self, vnum, vlink, vtype):
		bot = self.bot

		# setup scroll functionality
		def scroll():
			bot.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
			logger.info('scroll')

		# setup function to click the 'Add video' button
		def add_button():
			bot.find_element_by_id('add-video-button').click()
			logger.info('clicked [Add]')
		
		# get article title to reuse for video names
		article_title = bot.find_element_by_id('Title').get_attribute('value')
		logger.info('article title - ' + article_title)
		scroll()
		time.sleep(1)

		if 'v01' in vnum:
			bot.find_element_by_link_text('Videos').click() 
			logger.info('clicked [Videos] (Expand)')
			scroll()
			time.sleep(1)
			add_button() # changes to Add another, but id stays the same
			link = bot.find_element_by_id('AddedVideo0_VideoLink').send_keys(vlink)
			logger.info('link - ' + vlink)
			title = bot.find_element_by_id('AddedVideo0_VideoTitle').send_keys(article_title)
			logger.info('vid title - ' + article_title)
			
			if 'Creative' in vtype:
				vid_type = bot.find_element_by_id('AddedVideo0_VideoType').click()
				logger.info('clicked Type')
				time.sleep(1)
				select_type = bot.find_element_by_xpath(
					'//select[@id="AddedVideo0_VideoType"]//option[@value="Creative"]').click()
				logger.info('selected Creative')
				time.sleep(1)
			else:
				pass

		if 'v02' in vnum:
			scroll()
			time.sleep(1)
			add_button()
			link = bot.find_element_by_id('AddedVideo1_VideoLink').send_keys(vlink)
			logger.info('link - ' + vlink)
			title = bot.find_element_by_id('AddedVideo1_VideoTitle').send_keys(article_title)
			logger.info('vid title - ' + article_title)

			if 'Creative' in vtype:
				vid_type = bot.find_element_by_id('AddedVideo1_VideoType').click()
				logger.info('clicked Type')
				time.sleep(1)
				select_type = bot.find_element_by_xpath(
					'//select[@id="AddedVideo1_VideoType"]//option[@value="Creative"]').click()
				logger.info('selected Creative')
				time.sleep(1)
			else:
				pass

		if 'v03' in vnum:
			scroll()
			time.sleep(1)
			add_button()
			link = bot.find_element_by_id('AddedVideo2_VideoLink').send_keys(vlink)
			logger.info('link - ' + vlink)
			title = bot.find_element_by_id('AddedVideo2_VideoTitle').send_keys(article_title)
			logger.info('vid title - ' + article_title)

			if 'Creative' in vtype:
				vid_type = bot.find_element_by_id('AddedVideo2_VideoType').click()
				logger.info('clicked Type') # log
				time.sleep(1)
				select_type = bot.find_element_by_xpath(
					'//select[@id="AddedVideo2_VideoType"]//option[@value="Creative"]').click()
				logger.info('selected Creative') # log
			else:
				pass

def select1(cms):
	"""
	- Goes into each ID by splitting ID from v0 number in row['Vid']
	- adds relevant video (v01, v02 or v03)
	- adds Vimeo review link code from csv row['Link']
	- copies article title to video title
	- selects creative or remains campaign from row['Type']
	- saves changes

	#####################################################

	Pass in a csv file with the following column headers:
	
			[ID,	Vid,	Award,	Link,	Type]

	the order doesn't matter.
	"""

	fn = 'cms-input.csv'

	try:
		with open(fn, newline='') as csvfile:
			r = csv.DictReader(csvfile)
			for row in r:
				ID = row['ID']
				Award = row['Award'] # to update additional_info
				vnum = row['Vid']
				vlink = row['Link']
				vtype = row['Type']
				# vtitle = row['Title'] # not necessary, except for production video spreadsheet

				logger.info(f'-> csv row [{ID} - {vnum} - {vlink} - {vtype}]')

				try:
					# the 'x' here could be an issue. Length is probably better
					if len(vnum) >= 2:
						if 'v01' in vnum:
							cms.edit_id(ID)
							time.sleep(1)
							cms.add_video(vnum, vlink, vtype)

						if not 'v01' in vnum:
							cms.add_video(vnum, vlink, vtype)

						time.sleep(1)
						cms.save_changes()
						time.sleep(1)
					else:
						logger.info("- 'x' ID had no valid video")
				
				except Exception as e:
					logger.error(e)

	except Exception as e:
		logger.error(e)
		logger.info('not a valid csv file')

def select2(cms):

	"""
	Takes award from csv row['Award'] and appends it to 
	'Additional info' field in metadata. 
	'Entrant', 'Gold', 'Special Award', etc.

	Pass in a csv file with the following column headers:
	
			[ID, Award]

	the order doesn't matter.
	"""
	fn = 'cms-input.csv'

	try:
		with open(fn, newline='') as csvfile:
			r = csv.DictReader(csvfile)
			for row in r:
				ID = row['ID']
				Award = row['Award'] # to update additional_info

				logger.info(f'-> csv row [{ID}, {Award}]')

				try:
					if len(ID) >= 5:
						if len(Award) >= 2:
						
							cms.edit_id(ID)
							time.sleep(1)
							cms.additional_info(Award)
							time.sleep(1)
							cms.save_changes()
						else:		
							logger.info("- Incorrect IDs or Awards in csv. Check columns.")

				except Exception as e:
							logger.error(e)
	except Exception as e:
		logger.error(e)
		logger.info('not a valid csv file')

def select3(cms):
	'''Just needs a list of IDs in the CSV column ID'''
	
	fn = 'cms-input.csv'
	try:
		with open(fn, newline='') as csvfile:
			r = csv.DictReader(csvfile)
			for row in r:
				ID = row['ID']
				logger.info(f'-> csv row [{ID}]')

				try:
					if len(ID) >= 5:
						cms.edit_id(ID)
						time.sleep(1)
						cms.generate_bullets()
						time.sleep(1)
						cms.save_changes()
					else:
						logger.info("- No valid IDs in csv. Check 'ID' column.")

				except Exception as e:
						logger.error(e)
	except Exception as e:
		logger.error(e)
		logger.info('not a valid csv file')

def main():

	cms = CMSBot()

	selector = int(input(f'''FUNCTIONS
	'1' - Add videos
	'2' - Edit additional info ('Entrant', 'Gold', 'Special Award', etc.)
	'3' - Generate bullet summaries
	Select: '''))

	if selector == 1:
		select1(cms)
	if selector == 2:
		select2(cms)
	if selector == 3:
		select3(cms)
	if selector not in range(1,4):
		print(f'{selector} was not a valid selection')

	# so the driver quits properly 
	cms.bot.quit()

	print('\n\n# ~~~ SCRIPT ENDED ~~~ #')

	print('''#	
# 	  Improvements
#	  ============
#	
#  -> check whether Video links exists before trying to add it
#			
#	+ would stop duplication
#
#	- might screw up if trying to add a v02 or v03 if v01 exists 
#	  due to link numbering. The link would become AddedVideo0 for v02
#	  rather than AddedVideo1.
#
#  -> use pandas to read directly from the videos tab of the EDIT spreadsheet
#		  
# 	+ would be easier than pasting stuff into the csv...
#
#	- might run wild, so having more control might be better, 
#	  maybe should just use input for specifying a csv file

''')

if __name__ == '__main__':
	main()
