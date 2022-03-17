from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword="+keyword+"&sc.keyword="+keyword+"&locT=&locId=&jobType="
    #url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(15)
        try:
            driver.find_element(By.CLASS_NAME, "d-flex flex-column pl-sm css-1buaf54 job-search-key-1mn3dn8 e1rrn5ka0").click()
        except ElementClickInterceptedException:
            pass
        time.sleep(slp_time)
        try:
            driver.find_element(By.CSS_SELECTOR, '[alt="Close"]').click() #clicking to the X.
            print(' x out worked')
        except NoSuchElementException:
            print(' x out failed ')
            pass
        

        #Going through each job in this page
        
        job_buttons = driver.find_elements(By.CSS_SELECTOR, "li.react-job-listing")  #jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons: 
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                
                break

            job_button.click()  #You might 
            
            time.sleep(1)
            
            collected_successfully = False
            
            while not collected_successfully:
                try:
                    
                    company_name = driver.find_element(By.XPATH, './/div[@class="css-xuk5ye e1tk4kwz5"]').text
                    location = driver.find_element(By.XPATH, './/div[@class="css-56kyx5 e1tk4kwz1"]').text
                    job_title = driver.find_element(By.XPATH, './/div[@class = "css-1j389vi e1tk4kwz2"]').text
                    job_description = driver.find_element(By.XPATH, './/div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                
                salary_estimate = driver.find_element(By.XPATH, './/div[@class="css-y2jiyn e2u4hf18"]').text
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
            
            try:
                rating = driver.find_element(By.XPATH, './/div[@class="mr-sm css-ey2fjr e1pr2f4f3"]').text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                driver.find_element(By.XPATH, './/div[@data-item="tab" and @data-tab-type="overview"]').click()
                
                try:
                    size = driver.find_element(By.XPATH, './/div[@id="EmpBasicInfo"]//span[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1

                try:
                    founded = driver.find_element(By.XPATH, './/div[@id="EmpBasicInfo"]//span[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1

                try:
                    type_of_ownership = driver.find_element(By.XPATH, './/div[@id="EmpBasicInfo"]//span[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1

                try:
                    industry = driver.find_element(By.XPATH, './/div[@id="EmpBasicInfo"]//span[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element(By.XPATH, './/div[@id="EmpBasicInfo"]//span[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element(By.XPATH, './/div[@id="EmpBasicInfo"]//span[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

                try:
                    competitors = driver.find_element(By.XPATH, './/div[@id="EmpBasicInfo"]//span[text()="Competitors"]//following-sibling::*').text
                except NoSuchElementException:
                    competitors = -1

            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1

                
            if verbose:
                
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue,
            "Competitors" : competitors})
            #add job to jobs
            
            
        #Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH,'//button[@class="nextButton css-1hq9k8 e13qs2071"]').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.

