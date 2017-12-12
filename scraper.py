from bs4 import BeautifulSoup
import requests
import re

# r = requests.get("https://www.residentadvisor.net/reviews/21703")
r = requests.get("https://www.residentadvisor.net/reviews/21849")
data = r.text
soup = BeautifulSoup(data,'lxml')


release_data = soup.main.aside.find_all("li")

# 0 = label
# 1 = release month/year
# 2 = style
# 3 = comments
# 4 = rating

#handle label
label = re.findall(">.*<",str(release_data[0].contents[3]))[0][1:-1]

#handle style
release_month = release_data[1].contents[-1][1:-1]

#handle style
style = release_data[2].contents[-1][1:-1]

#handle comments
num_comments = release_data[3].contents[2][1:-3]

#handle rating
rating = re.findall('g">.*<s',str(release_data[4].contents[3]))[0][3:-2]
