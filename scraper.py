#cd Documents/personal/programming\ projects/RAReviewsData/

from bs4 import BeautifulSoup
import requests
import re

latest_review_id = "0"
link_base = "https://www.residentadvisor.net/reviews/"

#Single
# r = requests.get("https://www.residentadvisor.net/reviews/21855")
#album
r = requests.get("https://www.residentadvisor.net/reviews/21906")
data = r.text
soup = BeautifulSoup(data,'lxml')

#check release type -- if event, bail
try:
	release_type = re.findall('format=.*"',str(soup.header.find_all("li")[-1].contents[1]))[0][7:-1]
	if release_type == 'event' or release_type = 'tech':
		#CHANGE TO LOOP BAIL
		pass
except:
	release_type = "NaN"


#get artist and title from hyphenated title
artist_title = str(soup.body.header.find_all("h1")[0])[4:-5]

#split artist from title. store both.
try:
	artist_title = artist_title.split("-")
except:
	#might want to break loop here -- go on to next entry
	pass

try:
	artist = artist_title[0]
except:
	artist = "NaN"

try:
	release_title = artist_title[1]
except:
	release_title = "NaN"

#get chunk of data containing release info and rating
try:
	release_data = soup.main.aside.find_all("li")
except:
	#might want to break loop here -- go on to next entry
	pass

# 0 = label
# 1 = release month/year
# 2 = style
# 3 = comments
# 4 = rating

#handle label
try:
	label = re.findall(">.*<",str(release_data[0].contents[3]))[0][1:-1]
except:
	label = "NaN"

#handle release month
try:
	release_month = release_data[1].contents[-1][1:-1]
except:
	release_month = "NaN"

#handle style NOTE: COMMA SEPARATED LIST - HANDLE BEFORE CREATING CSV
try:
	style = release_data[2].contents[-1][1:-1]
except:
	style = "NaN"

#handle comments
try:
	num_comments = release_data[3].contents[2][1:-3]
except:
	num_comments = "NaN"

#handle rating
try:
	rating = re.findall('g">.*<s',str(release_data[4].contents[3]))[0][3:-2]
except:
	rating = "NaN"

#
# gather chunk containing review body, tracklist, date published and author
#
try:
	body_span = soup.main.find_all('span')
except:
	#might want to break loop here -- go on to next entry
	pass

#chop out review body
try:
	review_body = str(body_span[3])[58:-8]
except:
	review_body = "NaN"

#chop out date review published
try:
	review_published = body_span[5]['datetime']
except:
	review_published = "NaN"

#chop out author
try:
	author = re.findall('reviewer">.*<',str(body_span[7]))[0][10:-8]
except:
	author = "NaN"

#chop out tracklist
try:
	tracklist = str(body_span[13]).replace("\r<br/>",',')[6:-7]
except:
	tracklist = "NaN"




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


