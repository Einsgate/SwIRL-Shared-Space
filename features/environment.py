# examples
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

def before_all(context):
	options = webdriver.ChromeOptions()
	options.add_argument('--headless')
	context.browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
	# context.browser = webdriver.Chrome(chrome_options=options)
	# context.browser = webdriver.Firefox()
	# context.broswer = webdriver.Chrome(ChromeDriverManager().install())
	# context.broswer = webdriver.Firefox(executable_path=GeckoDriverManager().install())

	# context.browser = webdriver.PhantomJS()
	# context.browser.implicitly_wait(1)
	# context.server_url = 'http://localhost:8000'

def after_all(context):
	# Explicitly quits the browser, otherwise it won't once tests are done
	context.browser.quit()

def before_feature(context, feature):
	# Code to be executed each time a feature is going to be tested
	pass