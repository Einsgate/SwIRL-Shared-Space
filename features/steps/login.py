# for example
# follow the pattern to change the testing code
from behave import given, when, then
from test.factories.user import UserFactory

@given('an anonymous user')
def step_impl(context):
	from django.contrib.auth.models import User

	# Creates a dummy user for our tests (user is not authenticated at this point)
	u = UserFactory(username='foo', email='foo@example.com')
	u.set_password('bar')

	# Don't omit to call save() to insert object in database
	u.save()

@when('I submit a valid login page')
def step_impl(context):
	br = context.browser
	br.get(context.base_url + '/login/')

	# Checks for Cross-Site Request Forgery protection input
	assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()

	# Fill login form and submit it (valid version)
	br.find_element_by_name('username').send_keys('foo')
	br.find_element_by_name('password').send_keys('bar')
	br.find_element_by_name('submit').click()

@then('I am redirected to the login success page')
def step_impl(context):
	br = context.browser

	# Checks success status
	assert br.current_url.endswith('/login/success/')
	assert br.find_element_by_id('main_title').text == "Login success"

@when('I submit an invalid login page')
def step_impl(context):
	br = context.browser

	br.get(context.base_url + '/login/')

	# Checks for Cross-Site Request Forgery protection input (once again)
	assert br.find_element_by_name('csrfmiddlewaretoken').is_enabled()

	# Fill login form and submit it (invalid version)
	br.find_element_by_name('username').send_keys('foo')
	br.find_element_by_name('password').send_keys('bar-is-invalid')
	br.find_element_by_name('submit').click()

@then('I am redirected to the login fail page')
def step_impl(context):
	br = context.browser

	# Checks redirection URL
	assert br.current_url.endswith('/login/fail/')
	assert br.find_element_by_id('main_title').text == "Login failure"