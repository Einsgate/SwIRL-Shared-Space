from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from behave import *
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# from test.factories.user import UserFactory
# import selenium as se
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By

count1 = 0
count2 = 0


@given('Open reservation history')
def step_impl(context):
    br = context.browser
    br.get(context.base_url + '/reservation/history')
    assert br.current_url.endswith('/reservation/history')
    t_body = br.find_element_by_xpath('//*[@id="reserveList"]')
    rows = t_body.find_elements(By.TAG_NAME, "tr")
    count1 = rows

@when('I click on the delete on specific reservation')
def step_impl(context):
    br = context.browser
    # # br.get(br.current_url + '/reservation/create/')
    br.get(context.base_url + '/reservation/history')
    br.find_element_by_xpath('//*[@id="deleteSubmit"]').click() # click on delete
    t_body = br.find_element_by_xpath('//*[@id="reserveList"]')
    rows = t_body.find_elements(By.TAG_NAME, "tr")
    count2 = rows
    
@then('The reservation list changed')
def step_impl(context):
    br = context.browser
    assert count1 == count2