import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

# URL to collect results data from
url = 'https://vote.freeandequal.org/ranking'

# Define the sleep interval in seconds (3600 seconds = 1 hour)
sleep_interval = 3600

while True:
    # Send a GET request to the website and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all instances of the first span tag
    name_spans = soup.find_all('span', class_='text-[17px] font-bold text-darkBlue')

    # Find all instances of the second span tag
    vote_spans = soup.find_all('span', class_='whitespace-nowrap')

    # Create a list to store the extracted information
    data = []

    # Generate a timestamp for the CSV file name in the specified format (YY-MM-DD-HH-MM)
    timestamp = datetime.now().strftime('%y-%m-%d-%H-%M')

    # Iterate through each pair of span tags and extract the desired information
    for name_span, vote_span in zip(name_spans, vote_spans):
        # Extract the text content from the name span (removing " -" and any extra whitespace)
        name = ' '.join(name_span.stripped_strings).replace(" -", "")

        # Extract the text content from the vote span (assuming it's always in the format "Number Votes")
        vote_text = vote_span.get_text(strip=True)
        votes = vote_text.split()[0].replace("Votes", "")  # Extract the number part and remove "Votes"

        # Append the extracted information to the data list
        data.append([name, votes])

    # Create a CSV file with the timestamp in the filename
    csv_filename = f'scraped_data_{timestamp}.csv'

    # Write the data to the CSV file
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write header
        csv_writer.writerow(['Name', 'Votes'])
        
        # Write data rows
        csv_writer.writerows(data)

    print(f"Data has been saved to {csv_filename}")

    # Sleep for the specified interval before the next iteration
    time.sleep(sleep_interval)
