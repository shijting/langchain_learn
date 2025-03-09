# 默认 只取上海  代码以后再改
import logging
from typing import Dict, List
from urllib.parse import urlencode

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ai_job.utils.httputil import init_driver
import logging

listurl = "https://www.zhipin.com/web/geek/job?{}"


def get_list_by_keyword(keyword: str, page: int = 1, size: int = 30) -> str:
    url = listurl.format(urlencode({
        "query": keyword,
        "city": "101020100"
    }))

    driver = init_driver()
    if driver is None:
        raise Exception("创建无头浏览器失败")
    logging.info("创建无头浏览器成功")
    driver.maximize_window()

    driver.get(url)

    WebDriverWait(driver, 1000, 0.8). \
        until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                              '.job-list-box')))  # 等待页面加载到出现job-list-box 为止

    li_list = driver.find_elements(By.CSS_SELECTOR,
                                   ".job-list-box li.job-card-wrapper")
    jobs = []
    for li in li_list:
        job_name_list = li.find_elements(By.CSS_SELECTOR, ".job-name")
        if len(job_name_list) == 0:
            continue
        job = {}
        job["job_name"] = job_name_list[0].text
        job_salary_list = li.find_elements(By.CSS_SELECTOR, ".job-info .salary")
        if job_salary_list and len(job_salary_list) > 0:
            job["job_salary"] = job_salary_list[0].text
        else:
            job["job_salary"] = "暂无"
        job_tags_list = li.find_elements(By.CSS_SELECTOR, ".job-info .tag-list li")
        if job_tags_list and len(job_tags_list) > 0:
            job["job_tags"] = [tag.text for tag in job_tags_list]
        else:
            job["job_tags"] = []
        com_name = li.find_element(By.CSS_SELECTOR, ".company-name")
        if com_name:
            job["com_name"] = com_name.text
        else:
            continue  # 公司名称都没有，搞个毛
        com_tags_list = li.find_elements(By.CSS_SELECTOR, ".company-tag-list li")
        if com_tags_list and len(com_tags_list) > 0:
            job["com_tags"] = [tag.text for tag in com_tags_list]
        else:
            job["com_tags"] = []
        job_tags_list_footer = li.find_elements(By.CSS_SELECTOR, ".job-card-footer  li")
        if job_tags_list_footer and len(job_tags_list_footer) > 0:
            job["job_tags_footer"] = [tag.text for tag in job_tags_list_footer]
        else:
            job["job_tags_footer"] = []
        jobs.append(job)
    driver.close()
    job_tpl = """
{}. 岗位名称: {}
公司名称: {}
岗位要求: {}
技能要求: {}
薪资待遇: {}
     """
    ret = ""
    if len(jobs) > 0:
        for i, job in enumerate(jobs):
            job_desc = job_tpl.format(str(i + 1), job["job_name"],
                                      job["com_name"],
                                      ",".join(job["job_tags"]),
                                      ",".join(job["job_tags_footer"]),
                                      job["job_salary"])
            ret += job_desc + "\n"
        logging.info("完成直聘网分析")
        return ret
    else:
        raise Exception("没有找到任何岗位列表")
