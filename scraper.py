import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time

import csv

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=options)
driver.get("https://cpu.userbenchmark.com/")

def start():
    print("start")
    with open("cpu_data.csv", mode = "w", newline = "") as file:
        writer = csv.writer(file)
        columnTitles = ["Brand", "Name", "User Rating", "Value", "Average Benchmark", "Market Share", "Price"]
        writer.writerow(columnTitles)

        nextPageExists = True

        page = 1

        numCPUs = int(''.join(filter(str.isdigit, driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/form/div[1]/span/div[1]").text)))

        
        while(nextPageExists):
            print("search")
            lastCPU = page * 50
            leftCPUs = numCPUs - 50 * (page - 1)
            print(leftCPUs)
            if leftCPUs > 50:
                lastCPUString = "/html/body/div[2]/div/div[6]/form/div[2]/table/tbody/tr[50]/td[1]/div"
            else:
                lastCPUString = "/html/body/div[2]/div/div[6]/form/div[2]/table/tbody/tr[" + str(leftCPUs) + "]/td[1]/div"

            print(lastCPU)
            print(lastCPUString)
            while True:
                try:
                    currentLastCPU = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, lastCPUString))).text
                    print(currentLastCPU)
                    if(int(currentLastCPU) == lastCPU or int(currentLastCPU) == numCPUs):
                        break
                except StaleElementReferenceException:
                    time.sleep(.01)

            table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[6]/form/div[2]/table/tbody")))

            cpus = table.find_elements(By.CLASS_NAME, "hovertarget")
            

            for cpu in cpus:
                rowData = []

                #Finding Brand and Name
                nameInfo = cpu.find_element(By.CLASS_NAME, "semi-strongs.lighterblacktexts")

                nameInfoText = nameInfo.text
                brand = "Intel"
                if nameInfoText.find("AMD") != -1:
                    brand = "AMD"

                cpuName = nameInfo.find_element(By.CLASS_NAME, "nodec").text

                #Check if element exists, assigns it if so, assigns to N/A if not
                try:
                    userRating = cpu.find_element(By.XPATH, "./td[3]/div[1]").text
                except NoSuchElementException:
                    userRating = "N/A"

                try:
                    value = cpu.find_element(By.XPATH, "./td[4]/div[1]").text
                except NoSuchElementException:
                    value = "N/A"

                try:
                    averageBenchmark = cpu.find_element(By.XPATH, "./td[5]/div[1]").text
                except NoSuchElementException:
                    averageBenchmark = "N/A"

                try:
                    marketShare = cpu.find_element(By.XPATH, "./td[8]/div[1]").text
                except NoSuchElementException:
                    marketShare = "N/A"

                try:
                    price = cpu.find_element(By.XPATH, "./td[10]/div[1]").text
                except NoSuchElementException:
                    price = "N/A"

                # Adds data to row list
                rowData.append(brand)
                rowData.append(cpuName)
                rowData.append(userRating [1:-1].replace("\n", ""))
                rowData.append(value)
                rowData.append(averageBenchmark)
                rowData.append(marketShare)
                rowData.append(price)
                writer.writerow(rowData)

            print("End CPU Search")

            try:
                if page == 1:
                    nextPage = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/form/div[2]/nav/ul/li[2]/a")
                else:
                    nextPage = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[6]/form/div[2]/nav/ul/li[3]/a")

                nextPage.click()
                print("****************************")
            except NoSuchElementException:
                nextPageExists = False
                print("end")
                driver.quit()

            page += 1
    
start()