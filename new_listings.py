import os, requests, time
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
from discord_webhook import DiscordWebhook

# Webhook settings
url_wb = os.environ.get('DISCORD_WH')

# Data for the scrap
url = "https://www.coingecko.com/en/coins/recently_added"

# Open old database file
#path = "/home/pi/OpenAlpha/coingecko_listings.xlsx"
path = "coingecko_listings.xlsx"
df = pd.read_excel(path)

# Check url
response = get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Check the class before running the code. It might change from blog to blog
news_list = soup.find_all(class_ = 'd-lg-none font-bold')

# Empty list
updated_list = []

for news in news_list:
	token_text = news.text
	token_link = news.get('href')

	# Remove line break from token_text
	token_text = token_text.replace('\n', '')

	# Check if the main domain is missing in the href
	if ("http" not in token_link):
		token_link = "https://www.coingecko.com" + token_link

	if (token_link not in df.values):
		msg = f":lizard: **Coingecko listing** | **{token_text}**\n{token_link}"
		updated_list.append([token_text, token_link])
		try:
			print(msg)
		except:
			print(msg.encode('utf-8'))
		
		# Send message to Discord server
		webhook = DiscordWebhook(url=url_wb, content=msg)
		response = webhook.execute()

		# Sleep to not get rated
		time.sleep(1)

# Export updated news to Excel
cols = ['Token', 'Link']
df = df.append(pd.DataFrame(updated_list, columns=cols), ignore_index = True)
df.to_excel(path, index = False)