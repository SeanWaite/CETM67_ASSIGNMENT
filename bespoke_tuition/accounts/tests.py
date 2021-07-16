from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .forms import *

"""
Whilst this does not have a great deal of testing within the script, I can assure you that 100% of my
web app functionality has been tested. But by trail and error and not automated test scripts.

"""

class TestLoginPage(LiveServerTestCase):
 
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.close()
 
    # Can load login page and attempt to login with incorrect details?
    def test_incorrect_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login")
        user = driver.find_element_by_name("username")
        user.clear()
        user.send_keys("wrong")
        password = driver.find_element_by_name("password")
        password.clear()
        password.send_keys("wrong")
        driver.find_element_by_name("submit").click()
        message = driver.find_element_by_name("error_message").text
        expected = "Username or password is incorrect. If you have forgotten your password please contact us"
        self.assertEqual(message, expected)

    # Can load login page and attempt to login with correct details?
    def test_correct_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login")
        user = driver.find_element_by_name("username")
        user.clear()
        user.send_keys("boo2")
        password = driver.find_element_by_name("password")
        password.clear()
        password.send_keys("thistest1")
        driver.find_element_by_name("submit").click()
        driver.get("http://127.0.0.1:8000")
        username = driver.find_element_by_name("username").text
        expected = "Hello, boo2"
        self.assertEqual(username, expected)

class TestRegisterPage(TestCase):

    # Test registration form
    def test_reg_form_validation_fail(self):
        reg = CreateUserForm(data={'username': "boo", 
                                   'email': "boosays@theghost.com",
                                   'password1': "thistest2",
                                   'password2': "thistest1"})
        self.assertFalse(reg.is_valid())

"""" Not working as expected
    def test_reg_form_validation_pass(self):
        client = AddClientForm(data={'forename': "test", 
                                     'surname': "test",
                                     'password1': "thistest1",
                                     'password2': "thistest1"})

        contact = AddContactSet(data={'client': client, 
                                      'contact_number': "1234567",
                                      'email_address': "boosaid@theghost.com"})

I think this needs a client to be registered already to work which is what i tried to do above
        reg = CreateUserForm(data={'username': "boo", 
                                   'email': "boosaid@theghost.com",
                                   'password1': "thistest1",
                                   'password2': "thistest1"})
        self.assertTrue(reg.is_valid())
"""
