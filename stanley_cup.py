import requests
import time
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import datetime
import mplcursors


# Use this info to calculate how many data points there are since the NHL took over
# the Stanley Cup
currentYear = datetime.date.today().year
years_since_beginning = currentYear - 1927

# Request webpage
url = 'https://www.nhl.com/news/nhl-stanley-cup-champions-winners-complete-list/c-287705398'
response = requests.get(url)

# Parse table
soup = BeautifulSoup(response.content, "html.parser")
table = soup.find("div", class_="article-item__body")
winnerList = table.findAll("li")

# Create empty data arrays for plotting
year_list = []
team_list = []

# Parse year and team for each season and add to array
for winner in winnerList[:years_since_beginning]:
	winnerText = winner.text
	year, team_and_coach = winnerText.split(":")
	year = int(year)
	team = team_and_coach.split(",")[0].strip()

	# The Blackhawks used to be the Black Hawks, so we have to deal with that space
	# so that it doesn't behave as two seperate teams when we plot.
	if "chicago" in team.lower():
		team = "Chicago Blackhawks"

	year_list.append(year)
	team_list.append(team)

# Sort lists alphabetically
team_list, year_list = zip(*sorted(zip(team_list, year_list)))


# Plot data
sc = plt.scatter(team_list, year_list)
cursor = mplcursors.cursor(sc, hover=True)

# Show year when point is hovered
@cursor.connect("add")
def on_add(sel):
	sel.annotation.set(text=int(sel.target_[1]))


plt.xticks(rotation=90)
plt.title('Stanley Cup Champions')
plt.ylabel('Year')
plt.tight_layout()
plt.show()
