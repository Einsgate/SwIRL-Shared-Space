# for example
# follow the pattern to change the testing code
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

@given('Create zone one open reservation')
def step_impl(context):
    br = context.browser
    # Go to the Panel
    # print("L17: ", context.base_url)
    # br.get(context.base_url + "reservation/create/")
    # br.get(context.base_url + "reservation/")
    br.get(context.base_url)
    sleep(2)
    # br = context.browser
    # br.get(context.base_url + "reservation/create/")
    # 	assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()
    br.find_element_by_xpath("//*[@id='calendar']/div[1]/div[2]/div/button[1]").click() # click on month
    br.find_element_by_xpath('//*[@id="calendar"]/div[1]/div[1]/div/button[2]').click() # next
    reset = br.find_element_by_xpath('//*[@id="reservation-reset-button"]')
    zone_select = br.find_element_by_xpath('/html/body/div[2]/div/div[3]/div[2]/div[1]/div[1]/div[2]/div/div[1]')
    date = br.find_element_by_xpath('/html/body/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/div/div[2]/div/table/tbody/tr/td/div/div/div[1]/div[1]/table/tbody/tr/td[4]')
    # zone_select = br.find_elements(By.XPATH, '/html/body/div[2]/div/div[3]/div[2]/div[1]/div[1]/div[2]/div/div[1]')
    # date = br.find_elements(By.XPATH, '//*[@id="calendar"]/div[2]/div/table/tbody/tr/td/div/div/div[2]/div[1]/table/tbody/tr/td[2]')
    # target_x_offset = date.location.get("x")
    # target_y_offset = date.location.get("y")
    # x = zone_select.location.get("x")
    # y = zone_select.location.get("y")
    # x1 = zone_select2.location.get("x")
    # y2 = zone_select2.location.get("y")
    # print("L1: ", x)
    # print("L2: ", y)
    # print("L3: ", x1)
    # print("L4: ", y2)
    actions = ActionChains(br)
    
    # fill in valid form and submit, title"test1, open option, zone 1, switch to month calander view
    actions.move_to_element(zone_select).click_and_hold().pause(2).move_to_element(date).release().perform()
    # actions.move_to_element(date).pause(2).perform()
    # actions.drag_and_drop(zone_select, date).perform()
    # actions.drag_and_drop_by_offset(zone_select, 1000, 91).perform()
    # assert br.find_element_by_xpath('//*[@id="calendar"]/div[2]/div/table/tbody/tr/td/div/div/div[1]/div[2]/table/tbody/tr/td[4]/a/div[1]').is_enabled()
    # sleep(2)
    br.find_element_by_xpath('//*[@id="reservation-title"]').send_keys('test1') # title
    # br.find_element_by_xpath('//*[@id="reservation-type"]').click()
    # br.find_element_by_xpath('//*[@id="reservation-type"]/option[3]').click() # option open
    submit = br.find_element_by_xpath('//*[@id="reservation-button"]') # submit
    actions.move_to_element(submit).click().perform()
    # print("L38: ", br.current_url) # http://localhost:35831/?a=option2
    alert = Alert(br)
    print("L43:", alert.text)
    alert.accept()
    # alert2 = Alert(br)
    # print("L44:", alert2.text)
    # alert2.accept()
    br.get(context.base_url + '/reservation/history')
    assert br.current_url.endswith('/reservation/history')
    t_body = br.find_element_by_xpath('//*[@id="reserveList"]')
    rows = t_body.find_elements(By.TAG_NAME, "tr")
    print("L51:", len(rows))
    assert len(rows) >= 1

@when('I submit a zone one reservation')
def step_impl(context):
    br = context.browser
    # # br.get(br.current_url + '/reservation/create/')
    br.get(context.base_url)
    # # assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()
    # actions = ActionChains(br)
    # br.find_element_by_xpath('//*[@id="calendar"]/div[1]/div[2]/div/button[1]').click() # click on month
    # date = br.find_element_by_xpath('//*[@id="calendar"]/div[2]/div/table/tbody/tr/td/div/div/div[1]/div[1]/table/tbody/tr/td[3]')
    # zone_select = br.find_element_by_xpath('//*[@id="external-events"]/div[1]')
    # # fill in valid form and submit, title"test1, open option, zone 1, switch to month calander view
    # actions.click_and_hold(zone_select)
    # actions.move_to_element(date).perform()
	
    # sleep(2)
    # br.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div[2]/div[1]/div[2]/div[2]/form/div[1]/input').send_keys('test2')
    # br.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div[2]/div[1]/div[2]/div[2]/form/div[3]/div[2]/label/div').click()
    # br.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div[2]/div[1]/div[2]/div[2]/form/div[7]/button[1]').click()
    br.find_element_by_xpath("//*[@id='calendar']/div[1]/div[2]/div/button[1]").click() # click on month
    br.find_element_by_xpath('//*[@id="calendar"]/div[1]/div[1]/div/button[2]').click() # next
    reset = br.find_element_by_xpath('//*[@id="reservation-reset-button"]')
    zone_select = br.find_element_by_xpath('/html/body/div[2]/div/div[3]/div[2]/div[1]/div[1]/div[2]/div/div[1]')
    date = br.find_element_by_xpath('//*[@id="calendar"]/div[2]/div/table/tbody/tr/td/div/div/div[2]/div[1]/table/tbody/tr/td[2]')
    actions = ActionChains(br)
    
    # fill in valid form and submit, title"test1, open option, zone 1, switch to month calander view
    # actions.click_and_hold(zone_select).pause(5).move_to_element(date).release().perform()
    # actions.move_to_element(date).pause(2).perform()
    actions.drag_and_drop(zone_select, date).perform()
    # actions.drag_and_drop_by_offset(zone_select, 1000, 91).perform()
    # assert br.find_element_by_xpath('//*[@id="calendar"]/div[2]/div/table/tbody/tr/td/div/div/div[1]/div[2]/table/tbody/tr/td[4]/a/div[1]').is_enabled()
    # sleep(2)
    br.find_element_by_xpath('//*[@id="reservation-title"]').send_keys('test2') # title
    # br.find_element_by_xpath('//*[@id="reservation-type"]').click()
    # br.find_element_by_xpath('//*[@id="reservation-type"]/option[3]').click() # option open
    submit = br.find_element_by_xpath('//*[@id="reservation-button"]') # submit
    actions.move_to_element(submit).click().perform()
    
    assert True
	
	
@then('I am received error message')
def step_impl(context):
    br = context.browser
    alert = Alert(br)
    assert alert.text == "Conflit with existing reservations"
    alert.accept()
    assert True