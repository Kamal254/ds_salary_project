import pandas as pd
import Glassdoor_scrapping_code as gs

path = "C:/Users/SONU/Data_science_project/chromedriver"
df = gs.get_jobs("Data Scientist", 700, False, path, 20)
df.to_csv('Glassdoor_Scrapped_jobs.csv', index=False)


