# 开发时间 ：  11:28 PM
from selenium import webdriver
from time import sleep
import json
from selenium.webdriver.common.by import By


class TestCase(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.bilibili.com/index.html')
        self.driver.maximize_window()
        sleep(2)

        # 进入番剧页面
        self.driver.find_element(By.LINK_TEXT, '番剧').click()
        sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        _type = self.driver.find_element(By.XPATH, '//*[@id="home_v3_mod_index"]/div/div[2]/a/span').text
        print(_type)

        # 进入类型风格 页面
        self.driver.find_element(By.LINK_TEXT, '类型风格').click()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        sleep(5)

        self.driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div[5]/ul/li[2]').click()
        sleep(5)
        # self.driver.find_element(By.LINK_TEXT, '33').click()
        # 点击类型中的正片（输出所有正片标题、追番量、共多少话、标签、扩展：输出到数据库，excel

        # 总数量
        num_total = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[1]/div/a[6]').text
        print('总页数', num_total)

        #  标签
        tap_list = self.driver.find_element(By.CSS_SELECTOR, '#app > div.bangumi-index-body.clearfix > div.filter-body > ul.bangumi-list.clearfix > li:nth-child(1) > a.cover-wrapper > span').text
        print('这是什么？', tap_list)
        # 获取整页的数据
        tap_num_list = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[1]/ul[2]').text
        print('未分类的数据', tap_num_list)


    def sum_anime(self):
        sleep(10)
        all1_list = []
        tap_list = self.driver.find_elements(By.XPATH, '//ul[@class="bangumi-list clearfix"]/li')
        for tap in tap_list:
            item = {}
            item['番剧名称'] = tap.find_element(By.CLASS_NAME, 'bangumi-title').text
            item['版权'] = tap.find_element(By.TAG_NAME, 'span').text
            item['追番量'] = tap.find_element(By.CLASS_NAME, 'shadow').text
            item['封面'] = tap.find_element(By.TAG_NAME, 'img').get_attribute('src')
            item['共多少话'] = tap.find_element(By.XPATH, './/p[@class="pub-info"]').text
            all1_list.append(item)

        print('分类后，第一页的数据', all1_list)
        page_one = self.driver.find_element(By.CLASS_NAME, 'p.active').text
        page_end = self.driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[1]/div/div/span[1]').text
        page = page_end[2:4]

        if page_one == page:
            return all1_list, None
        else:
            next_data = self.driver.find_element(By.LINK_TEXT, '下一页')
            next_url = next_data.text

            if len(next_url) > 0:
                return all1_list, next_data
            else:
                next_data = None
            return all1_list, next_data



    # 存到数据库
    def save_data(self, content_list):
        with open("douyu.txt", "a", encoding='utf-8') as f:
            for content in content_list:
                json.dump(content, f, ensure_ascii=False, indent=2)
                f.write("\n")
                print("保存数据成功")
            f.close()
            # self.driver.quit()

if __name__ == '__main__':
    test = TestCase()
    all_list, next_list = test.sum_anime()
    test.save_data(all_list)
    while next_list is not None:
        next_list.click()
        all_list, next_list = test.sum_anime()
        test.save_data(all_list)
