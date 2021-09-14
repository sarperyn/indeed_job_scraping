from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import os



#For windows run below
'''
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
'''


#For mac run below
driver = webdriver.Chrome(ChromeDriverManager().install())
#driver.get("https://ca.indeed.com/jobs?q=computer%20science%20internship&l=Toronto,%20ON&radius=25&ts=1630423938843&pts=1630353837882&rq=1&rsIdx=0")

job = "computer science internship"
location = "ontario"

companies = []
job_list = []
job_desc_list = []

def go_indeed(job,location):
    driver.get("https://ca.indeed.com/")

    main = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID,"ssrRoot"))
        )
    try:
        text_input = main.find_element_by_id("text-input-what")
        text_input.send_keys(job)
        if len(location) != 0:
                location_input = main.find_element_by_id('text-input-where')
                location_input.send_keys(location)
        find_jobs = main.find_element_by_xpath('//*[@id="whatWhereFormId"]/div[3]/button')
        find_jobs.click()

    except:
        pass


def create_df(*args):
    df = pd.DataFrame({
        "company":args[0],
        "job_header":args[1],
        "job_description":args[2]
    })
    return df

def get_page():
    main = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID,"resultsBodyContent"))
        )
    try:

        # Get company names and job titles
        job_titles = main.find_elements_by_tag_name("h2")
        company_names = main.find_elements_by_class_name("companyName")

        #Add the data to each lists
        for i in range(len(job_titles)):

            job_titles[i].click()
            title = job_titles[i].text.replace('new\n','')
            company = company_names[i].text
            time.sleep(1.5)
            vjs_desc = main.find_element_by_id("vjs-desc")
            job_desc_list.append(vjs_desc.text)
            job_list.append(title)
            companies.append(company)

    finally:
        pass


def get_data():

    try:
        for i in range(20):
            time.sleep(1)
            #ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)

            get_page()

            #Click the forward button
            if i == 0:
                button = WebDriverWait(driver,10,)\
                .until(EC.presence_of_element_located((By.XPATH,'//*[@id="resultsCol"]/nav/div/ul/li[6]/a/span'))) 
            else:
                try:
                    button = WebDriverWait(driver,10,)\
                        .until(EC.presence_of_element_located((By.XPATH,'//*[@id="resultsCol"]/nav/div/ul/li[7]/a/span')))
                except:
                    break

            button.click()
            driver.refresh()

    finally:
        #Create the dataset
        df = create_df(companies,job_list,job_desc_list)
        job_str = ''.join(x for x in job.title() if not x.isspace())

        if len(location) != 0:
            location_str = ''.join(x for x in location.title() if not x.isspace())
            df.to_csv((f"{job_str}_{location_str}.csv"))
        
        else:
            df.to_csv((f"{job_str}_.csv"))



        driver.quit()

    
go_indeed(job,location)
get_data()
