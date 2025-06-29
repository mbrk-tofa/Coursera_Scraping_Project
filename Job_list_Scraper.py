import requests
import pandas as pd
import time, schedule
from datetime import datetime
import os

# Creating a folder to save multiple runs
os.makedirs("remoteok_data", exist_ok=True)

def fetch_and_save_remoteok():
    url = 'https://remoteok.com/api'
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # raise error for bad response

        jobs = response.json()[1:]  # skip metadata

        data = []
        for job in jobs:
            data.append({
                'Company': job.get('company'),
                'Position': job.get('position'),
                'Tags': ', '.join(job.get('tags', [])),
                'Location': job.get('location'),
                'Date Posted': job.get('date'),
                'URL': f"https://remoteok.com{job.get('url')}"
            })

        df = pd.DataFrame(data)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
        filename = f"remoteok_data/jobs_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"Saved: {filename}")
        
    except Exception as e:
        print(f"Error fetching data: {e}")

# Running the scheduler every hour
schedule.every(1).hour.do(fetch_and_save_remoteok)
print("Fetching start every one hour")

#looping to keep the scheduler running
while True:
    schedule.run_pending()
    time.sleep(60)  # check every 1 minute
