from selenium import webdriver
from selenium.webdriver.remote.remote_connection import RemoteConnection
from automation_helpers import AutomationHelpers
from os import environ
from erppeek import Client


def get_browser():
    """
    Get the browser to use
    :return: Selenium driver
    """
    if environ.get('GO_PIPELINE_LABEL'):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        desired_caps = options.to_capabilities()
        selenium_host = environ.get('GATEWAY', 'localhost')
        selenium_endpoint = "http://{}:4444/wd/hub".format(selenium_host)
        executor = RemoteConnection(selenium_endpoint, resolve_ip=False)
        browser = webdriver.Remote(
            command_executor=executor,
            desired_capabilities=desired_caps,
        )
        return browser
    else:
        return webdriver.Chrome()


def before_all(context):
    """
    Before all features and scenarios are run set up environment

    :param context: Behave context
    """
    context.driver = get_browser()
    context.helpers = AutomationHelpers('config.yml')
    context.client = Client(
        context.helpers.config.get('server'),
        context.helpers.config.get('database'),
        user='admin',
        password='admin',
    )


def after_all(context):
    """
    After all features and scenarios are run clean up the environment

    :param context: Behave context
    """
    context.driver.quit()
