```shell
pip install html2text BeautifulSoup4
```

# 抓取股票数据

## 两个方向

1. 输入股票名称，查看它好不好（目前）
2. 输入行业，行情，消息等关键字，反推股票(需要模型微调或者蒸馏)

## 思路

信息收集和总结，信息处理和过滤

```
用输入关键字，比如茅台 -> 财联社agent tool -> 根据关键字查询股票代码tool ->F10获取概念 -> 
最后结合k线信息，公司信息，经营信息, 财务信息得出这个股票到底好不好
```

1. 财联社电报
   https://www.cls.cn/searchPage?keyword=%E8%8C%85%E5%8F%B0&type=telegram
2. 同花顺F10（题材要点）
   http://basic.10jqka.com.cn/600519/concept.html  (600519 是茅台的股票代码)

   需要把关键字转成股票代码, 可以参考这个项目 https://github.com/yangshun/stock-code-convertor

3. 其他，比如雪球、东方财富、网易股票等

## selenlum

自动化测试和浏览器自动化的开源框架。它允许开发人员编写脚本来模拟用户在浏览器中的行为，自动执行一系列操作，如点击按钮、填写表单、导航到不同页面等

```shell
pip installselenium==4.23.1 
```

### 安装驱动

#### linux

https://googlechromelabs.github.io/chrome-for-testing/#stable

需要先安装chrome浏览器

```
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

如果安装过程中出现依赖问题，输入以下命令修复依赖：

```shell

sudo apt-get install -f
```

安装好后执行

```shell
google-chrome --version
```

注意：版本需要和chrome版本保持一致

#### mac：

```shell
brew install chromedriver
which chromedriver 查看chromedriver path
```

https://googlechromelabs.github.io/chrome-for-testing/#stable

#### 简单抓取百度示例

```python
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
    print(driver.find_element(By.CLASS_NAME, "title-content-title").text)
    driver.quit()


if __name__ == '__main__':
    test()

```

#### 抓取boss直聘

https://www.zhipin.com/web/geek/job?query=golang&city=101281600
基础做法

```
输入关键字如golang -> Ai Agent(暂时不写)->使用无头浏览器在线分析抓取 -> 进行rag匹配
->进一步筛选，输出组最合适的岗位结果
```

进阶做法

```
输入关键字如golang -> Ai Agent(暂时不写)->使用无头浏览器在线分析抓取 -> 进行rag匹配
->进一步筛选 ->输出组最合适的岗位结果 -> 用户反馈 -> 如果用户不满意简历- >Ai Agent-> 自动“修复”简历 ,使得你的简历更加匹配职位需求

也可以这么做， 用户输入岗位职责描述/岗位要求 -> 用户输入简历 -> AI Agent ->自动“修复”简历 ,使得你的简历更加匹配职位需求 -> 自动投简历(可选)
```

#### 读取doc简历

```shell
pip install python-docx
```












