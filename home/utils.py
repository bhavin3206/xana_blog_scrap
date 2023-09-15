from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import time,re, random
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class Bot():
    def __init__(self,task_id) -> None:
        self.links = []
        self.article = []
        self.choice = task_id
        self.today = datetime.now()
        self.date_format = '%Y/%m/%d'
        try:
            self.data = pd.read_csv('scraped_data.csv')
        except FileNotFoundError:
            self.data = pd.DataFrame(columns=['URL', 'Text'])
            self.data.to_csv('scraped_data.csv', index=False)
            
        try:
            self.article_data = pd.read_csv('article_data.csv')
        except FileNotFoundError:
            self.article_data = pd.DataFrame(columns=['Text'])
            self.article_data.to_csv('article_data.csv', index=False)

        if self.choice == '1':
            self.end_date  = self.today
            self.start_date = self.end_date  - timedelta(days=7)

        elif str(self.choice).startswith("2") :
            start_date_str, end_date_str = self.choice.split('-')[1:]
            self.start_date = datetime.strptime(start_date_str.strip(), self.date_format)
            self.end_date  = datetime.strptime(end_date_str.strip(), self.date_format)
            
        elif self.choice == '3':
            start_of_previous_week = self.today - timedelta(days=self.today.weekday() + 7)
            end_of_previous_week = start_of_previous_week + timedelta(days=6)
            start_date_str = start_of_previous_week.strftime('%Y/%m/%d')
            end_date_str = end_of_previous_week.strftime('%Y/%m/%d')
            self.start_date = datetime.strptime(start_date_str, self.date_format)
            self.end_date  = datetime.strptime(end_date_str, self.date_format)    

    def find_element(self,xpath,locator=By.XPATH,timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        try:
            ele = wait.until(EC.presence_of_element_located((locator, xpath)))
            return ele
        except NoSuchElementException:
            pass
        except Exception as e:
            pass

    def find_elements(self, xpath, locator=By.XPATH, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        try:
            elements = wait.until(EC.presence_of_all_elements_located((locator, xpath)))
            return elements
        except NoSuchElementException:
            pass
        except Exception as e:
            pass
        
    def click_popup(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoViewIfNeeded();", element)
        time.sleep(1)
        element.click()
        

    def filter_blog_posts(self):
        url = 'https://web.xana.net/blog/'
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=service,options=options)
        self.driver.maximize_window()
        self.driver.get(url)
        print('start driver .....')
        time.sleep(10)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        load_more = self.find_element('//button[text()="Load More"]')
        while not load_more:
            load_more = self.find_element('//button[text()="Load More"]')
            print('not find load more ...')
        for i in range(3):
            self.click_popup(load_more)
            time.sleep(2)
        time.sleep(5)
        blog_posts = self.find_elements('cs-entry__outer',By.CLASS_NAME)
        for post in blog_posts:
            try:
                date_element = post.find_element(By.CLASS_NAME, 'cs-meta-date')
                date_str = date_element.text.strip()
                match = re.search(r'\d{4}/\d{2}/\d{2}', date_str)
                if match:
                    post_date = datetime.strptime(match.group(), self.date_format)
                    
                    # Check the user's self.choice and filter accordingly
                    if self.choice == '1' and (self.today - post_date).days <= 7:
                        link_element = post.find_element(By.CLASS_NAME, 'cs-overlay-link')
                        blog_link = link_element.get_attribute('href')
                        print("Blog Date:", post_date)
                        print("Blog Link:", blog_link)
                        print("Days Since Publication:", (self.today - post_date).days, "days")
                        print("-" * 50)
                        self.links.append(blog_link)

                    elif self.choice == '2' and self.start_date <= post_date <= self.end_date:
                        link_element = post.find_element(By.CLASS_NAME, 'cs-overlay-link')
                        blog_link = link_element.get_attribute('href')
                        print("Blog Date:", post_date)
                        print("Blog Link:", blog_link)
                        print("Days Since Publication:", (self.today - post_date).days, "days")
                        print("-" * 50)
                        self.links.append(blog_link)

                    elif self.choice == '3' and self.start_date <= post_date <= self.end_date:
                        link_element = post.find_element(By.CLASS_NAME, 'cs-overlay-link')
                        blog_link = link_element.get_attribute('href')
                        print("Blog Date:", post_date)
                        print("Blog Link:", blog_link)
                        print("Days Since Publication:", (self.today - post_date).days, "days")
                        print("-" * 50)
                        self.links.append(blog_link)

            except Exception as e:
                print("Error:", e)
                continue
        new_data = pd.DataFrame({'URL': self.links})
        self.data = pd.concat([self.data, new_data], ignore_index=True).drop_duplicates(subset=['URL'])
        self.data.to_csv('scraped_data.csv', index=False)
    
    def scrape_blog_text(self):
        data = pd.read_csv('scraped_data.csv')
        df2_li = []
        for i in data.index:
            data = pd.read_csv('scraped_data.csv')
            url = data.at[i,'URL']
            print(url,data.at[i,'Text'])
            if pd.notnull(data.at[i,'Text']):
                self.article.append(data.at[i,'Text'])
                print("URL already scraped, skipping...")
                df2_li.append({
                    "Text" : data.at[i,'Text'],
                    "Url" : url
                })
            else:
                self.driver.get(url)
                time.sleep(random.randint(4,6))
                entry_content = self.driver.find_element(By.CLASS_NAME, 'entry-content')
                text = entry_content.text
                text = re.sub(r'[^\w\s.]', '', text)
                myarticle = text.replace('\t', ' ').replace('\n', ' ')
                self.article.append(myarticle)
                data.at[i,'Text'] = myarticle
                data.to_csv('scraped_data.csv', index=False)
                df2_li.append({
                    "Text" : myarticle,
                    "Url" : url
                })
                
        new_data = pd.DataFrame({'Text': self.article})
        self.article_data = pd.concat([self.article_data, new_data], ignore_index=True).drop_duplicates(subset=['Text'])
        self.article_data.to_csv('article_data.csv', index=False)
        print('-'*20+ ' Scrape Complete ' + '-'*20)
        self.driver.quit()
        return df2_li

if __name__ == '__main__':
    bot = Bot()
    bot.filter_blog_posts()
    bot.scrape_blog_text()