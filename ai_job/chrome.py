from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def test():
    chromedriver_path = "/opt/homebrew/bin/chromedriver"
    service = Service(executable_path=chromedriver_path, service_args=["--headless=new",
                                                                       '--no-sandbox',
                                                                       '--disable-dev-shm-usage',
                                                                       '--disable-gpu',
                                                                       '--ignore-certificate-errors',
                                                                       '--ignore-ssl-errors',
                                                                       ])
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")

    # 加载一个网页
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.baidu.com")
    print(driver.title)
    print(driver.find_element(By.CLASS_NAME,"title-content-title").text)
    driver.quit()


if __name__ == '__main__':
    test()
