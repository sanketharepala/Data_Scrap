from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import csv
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import params

driver = webdriver.Chrome('/usr/bin/chromedriver')
driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')

user = driver.find_element_by_name('session_key')
user.send_keys(params.linkedin_username)
sleep(1)

password = driver.find_element_by_name('session_password')
password.send_keys(params.linkedin_password)
sleep(1)

login_btn = driver.find_element_by_xpath('//*[@id="app__container"]/main/div/form/div[3]/button')
login_btn.click()
sleep(3)

sleep(1)
i = 0
j = 0

writer = csv.writer(open(params.file_name, 'w'))

writer.writerow(['Job_Title', 'Job_Description', 'company', 'location ', 'Industry', 'Employment_type', 'Job Function',
                 'Experence_Level'])

while (j < 40):

    print("processing")

    present_url = 'https://www.linkedin.com/jobs/search/?f_E=2&f_TPR=r604800&geoId=103644278&keywords=business%20analytics&location=United%20States' + '&start=' + str(
        i)

    driver.get(present_url)
    scroll = driver.find_element_by_class_name('jobs-search-results')
    scroll.send_keys(Keys.PAGE_DOWN)

    sleep(1)

    scroll.send_keys(Keys.PAGE_DOWN)

    sleep(1)

    scroll.send_keys(Keys.PAGE_DOWN)

    sleep(1)

    # ActionChains(driver).move_to_element(
    #     driver.find_element_by_class_name('search-results-pagination-section')).perform()

    jobs = driver.find_elements_by_class_name('job-card-search__title')

    for job in jobs:
        current_url = driver.current_url

        if (present_url == current_url):
            print("sanketha is dumb " + str(j))

        try:
            job.click()
        except:
            pass

        try:
            company_name = driver.find_element_by_class_name('jobs-details-top-card__company-url')
            company_name = company_name.text

            if company_name:
                company_name = company_name.strip()
        except:
            company_name = None

        try:
            job_name = driver.find_element_by_class_name('jobs-details-top-card__job-title')
            job_name = job_name.text

            if job_name:
                job_name = job_name.strip()
        except:
            job_name = None

        try:
            job_description = driver.find_element_by_xpath('//*[@id="job-details"]')
            job_description = job_description.text

            if job_description:
                job_description = job_description.strip()
        except:
            job_description = None

        try:
            employement_type = driver.find_element_by_class_name('js-formatted-employment-status-body')
            employement_type = employement_type.text

            if employement_type:
                employement_type = employement_type.strip()
        except:
            employement_type = None

        try:
            industry = driver.find_element_by_class_name('js-formatted-industries-list')
            industry = industry.find_elements_by_class_name('jobs-box__list-item')
            industry = [ind.text for ind in industry]
            industry = ','.join(industry)

            if industry:
                industry = industry.strip()
        except:
            industry = None

        try:
            location = driver.find_element_by_class_name('jobs-details-top-card__bullet')
            location = location.text

            if location:
                location = location.strip()
        except:
            location = None

        try:
            job_function = driver.find_element_by_class_name('js-formatted-job-functions-list')
            job_function = job_function.text

            if job_function:
                job_function = job_function.strip()
        except:
            job_function = None

        try:
            experence_Level = driver.find_element_by_class_name('js-formatted-exp-body')
            experence_Level = experence_Level.text

            if experence_Level:
                experence_Level = experence_Level.strip()
        except:
            experence_Level = None

        writer.writerow([job_name, job_description, company_name, location, industry, employement_type,
                         job_function, experence_Level])
        sleep(2)

    i = i + 25

    j = j + 1

print("completed" + "driver is closing")
driver.quit()
