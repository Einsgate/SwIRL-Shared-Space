# for example
# follow the pattern to change the testing code
from selenium.webdriver import ActionChains
from time import sleep
from behave import *
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# from test.factories.user import UserFactory
# import selenium as se
from selenium.webdriver.common.alert import Alert

@given('Create zone one open reservation')
def step_impl(context):
    br = context.browser

    # Go to the Panel
    # print("L17: ", context.base_url)
    # br.get(context.base_url + "reservation/create/")
    # br.get(context.base_url + "reservation/")
    br.get(context.base_url)
    
    # br = context.browser
    # br.get(context.base_url + "reservation/create/")
    # 	assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()
    actions = ActionChains(br)
    
    br.find_element_by_xpath("//*[@id='calendar']/div[1]/div[2]/div/button[1]").click() # click on month
    date = br.find_element_by_xpath('//*[@id="calendar"]/div[2]/div/table/tbody/tr/td/div/div/div[1]/div[1]/table/tbody/tr/td[3]')
    zone_select = br.find_element_by_xpath('//*[@id="external-events"]/div[1]')
    # fill in valid form and submit, title"test1, open option, zone 1, switch to month calander view
    actions.click_and_hold(zone_select)
    actions.move_to_element(date).perform()
    
    sleep(2)
    br.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div[2]/div[1]/div[2]/div[2]/form/div[1]/input').send_keys('test1') # title
    br.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div[2]/div[1]/div[2]/div[2]/form/div[3]/div[2]/label/div').click() # option open
    br.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div[2]/div[1]/div[2]/div[2]/form/div[7]/button[1]').click() # submit
    print("L38: ", br.current_url) # http://localhost:35831/?a=option2
    assert br.current_url.endswith('/reservation/create/')

@when('I submit a zone one reservation')
def step_impl(context):
    br = context.browser
    # br.get(br.current_url + '/reservation/create/')
    # br.get(context.base_url)
    # assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()
    actions = ActionChains(br)
    br.find_element_by_xpath('//*[@id="calendar"]/div[1]/div[2]/div/button[1]').click() # click on month
    date = br.find_element_by_xpath('//*[@id="calendar"]/div[2]/div/table/tbody/tr/td/div/div/div[1]/div[1]/table/tbody/tr/td[3]')
    zone_select = br.find_element_by_xpath('//*[@id="external-events"]/div[1]')
    # fill in valid form and submit, title"test1, open option, zone 1, switch to month calander view
    actions.click_and_hold(zone_select)
    actions.move_to_element(date).perform()
	
    sleep(2)
    br.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div[2]/div[1]/div[2]/div[2]/form/div[1]/input').send_keys('test2')
    br.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div[2]/div[1]/div[2]/div[2]/form/div[3]/div[2]/label/div').click()
    br.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div[2]/div[1]/div[2]/div[2]/form/div[7]/button[1]').click()
	
	
@then('I am received error message')
def step_impl(context):
    br = context.browser
    alert = Alert(br)
    assert alert.text == "Conflit with existing reservations"
    alert.accept()