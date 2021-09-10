from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time
import pandas as pd



#For windows run this
'''
PATH = "YOUR OWN CHROMEDRIVER PATH"
driver = webdriver.Chrome(PATH)
'''
#For mac run this

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://ca.indeed.com/jobs?q=computer%20science%20internship&l=Toronto,%20ON&radius=25&ts=1630423938843&pts=1630353837882&rq=1&rsIdx=0")



companies = []
job_list = []
job_desc_list = []


def create_df(*args):
    df = pd.DataFrame({
        "company":args[0],
        "job_header":args[1],
        "job_description":args[2]
    })
    return df

def get_page():
    try:

        main = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID,"resultsBodyContent"))
        )

        # Get company names and job titles
        job_titles = main.find_elements_by_tag_name("h2")
        company_names = main.find_elements_by_class_name("companyName")

        #Add the data to each lists
        for i in range(len(job_titles)):

            job_titles[i].click()
            title = job_titles[i].text.replace('new\n','')
            company = company_names[i].text
            time.sleep(1)
            vjs_desc = main.find_element_by_id("vjs-desc")



            job_desc_list.append(vjs_desc.text)
            job_list.append(title)
            companies.append(company)

    finally:
        pass


def main():
    main = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.ID,"resultsBodyContent"))
        )


    try:
        for i in range(6):
            time.sleep(1)
            ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)

            get_page()


            #Click the forward button
            if i == 0:
                button = WebDriverWait(driver,10,ignored_exceptions=ignored_exceptions)\
                .until(EC.presence_of_element_located((By.XPATH,'//*[@id="resultsCol"]/nav/div/ul/li[6]/a/span'))) 
            else:
                button = WebDriverWait(driver,10,ignored_exceptions=ignored_exceptions)\
                    .until(EC.presence_of_element_located((By.XPATH,'//*[@id="resultsCol"]/nav/div/ul/li[7]/a/span')))
            
            button.click()
            driver.refresh()
    
    except:
        pass

    finally:
        '''
        print("Companies",len(companies))
        print("Job_list",len(job_list))
        print(len(job_desc_list))
        '''
        #Create the dataset
        df = create_df(companies,job_list,job_desc_list)
        df.to_csv("data_new.csv")

        driver.quit()


main()
