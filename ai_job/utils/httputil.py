from selenium import webdriver
import requests
# 这里包含了 抓取 相关的函数
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

chromedriver_path = "/opt/homebrew/bin/chromedriver"


# 写死

def init_driver() -> webdriver:
    # '--verbose',  log_output=sys.stdout,
    service = Service(executable_path=chromedriver_path,
                      service_args=[
                          '--headless',
                          '--no-sandbox',
                          '--disable-dev-shm-usage',
                          '--disable-gpu',
                          '--ignore-certificate-errors',
                          '--ignore-ssl-errors',
                          '--user-data-dir=/Users/jinting/Library/Application\ Support/Google/Chrome'
                      ])

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_experimental_option('detach', True)
    options.add_argument('--user-data-dir==/Users/jinting/Library/Application\ Support/Google/Chrome')
    options.add_experimental_option("useAutomationExtension", False)  # 关闭插件
    return webdriver.Chrome(options=options, service=service)
