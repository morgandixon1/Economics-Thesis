from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

chrome_driver_path = "chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get("https://www.bls.gov/ooh/a-z-index.htm")

# Find all <li> elements
all_li_tags = driver.find_elements(By.TAG_NAME, 'li')

job_titles = []
links = []

for li in all_li_tags:
    # Find the first <a> tag within each <li> element
    a_tags = li.find_elements(By.TAG_NAME, 'a')
    if a_tags:
        first_a_tag = a_tags[0]
        href = first_a_tag.get_attribute("href")
        if href and "/ooh/" in href and href.endswith(".htm"):
            job_title = first_a_tag.text
            job_titles.append(job_title)
            links.append(href)

df = pd.DataFrame({"Job Title": job_titles, "Link": links})
print(df)
df.to_csv("Jobs_and_urls.csv", index=False)
driver.quit()
