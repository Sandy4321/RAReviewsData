#cd Documents/personal/programming projects/RAReviewsData

from bs4 import BeautifulSoup
import requests
import re

#Single
# r = requests.get("https://www.residentadvisor.net/reviews/21855")
#album
r = requests.get("https://www.residentadvisor.net/reviews/4948")
data = r.text
soup = BeautifulSoup(data,'lxml')

#get artist and title from hyphenated title
artist_title = str(soup.body.header.find_all("h1")[0])[4:-5]

#split artist from title. store both.
artist_title = artist_title.split("-")
artist = artist_title[0]
release_title = artist_title[1]

#get chunk of data containing release info and rating
release_data = soup.main.aside.find_all("li")

# 0 = label
# 1 = release month/year
# 2 = style
# 3 = comments
# 4 = rating

#handle label
label = re.findall(">.*<",str(release_data[0].contents[3]))[0][1:-1]

#handle release month
release_month = release_data[1].contents[-1][1:-1]

#handle style NOTE: COMMA SEPARATED LIST - HANDLE BEFORE CREATING CSV
style = release_data[2].contents[-1][1:-1]

#handle comments
num_comments = release_data[3].contents[2][1:-3]

#handle rating
rating = re.findall('g">.*<s',str(release_data[4].contents[3]))[0][3:-2]

#
# gather chunk containing review body, tracklist, date published and author
#
body_span = soup.main.find_all('span')

#chop out review body
review_body = str(body_span[3])[58:-8]

#chop out date review published
review_published = body_span[5]['datetime']

#chop out author
author = re.findall('reviewer">.*<',str(body_span[7]))[0][10:-8]

#chop out tracklist
tracklist = str(body_span[13]).replace("\r<br/>",',')[6:-7]


release_type = re.findall('format=.*"',str(soup.header.find_all("li")[-1].contents[1]))[0][7:-1]


# print(soup.prettify())

print("artist= " + artist)
print("release_title= " + release_title)
print("label= " + label)
print("release_month= " + release_month)
print("style= " + style)
print("num_comments= " + num_comments)
print("rating= " + rating)
print("review_body= " + review_body)
print("review_published= " + review_published)
print("author= " + author)
print("tracklist= " + tracklist)
print("release_type= " + release_type)


