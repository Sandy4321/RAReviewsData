#cd Documents/personal/programming\ projects/RAReviewsData/

from bs4 import BeautifulSoup
import requests
import re
import csv

############
# CONTROLS #
############
latest_review_id = 21855
#set as either number of pulls to try or "full" 
#pulls 25 in about 32 seconds -- full run will take almost 8 hours(!)
num_pulls = 400
verbose = False
###########

if (num_pulls == "full"):
	num_pulls = latest_review_id - 1


link_base = "https://www.residentadvisor.net/reviews/"

with open('RA.csv', 'wb') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter=';')
	csvwriter.writerow(["ra_review_id","release_type","artist","release_title","label","release_month","style","num_comments","rating","review_published","author","review_body","tracklist"])
	# csvwriter.writerow(["ra_review_id","release_type","artist","release_title","label","release_month","style","num_comments","rating","review_published","author","tracklist"])


	for i in range(latest_review_id,latest_review_id - num_pulls,-1):
		

		url = link_base + str(i)

		# r = requests.get("https://www.residentadvisor.net/reviews/21787")
		r = requests.get(url)
		data = r.text
		soup = BeautifulSoup(data,'lxml')

		#check release type -- if event, bail
		try:
			release_type = re.findall('format=.*"',str(soup.header.find_all("li")[-1].contents[1]))[0][7:-1]
			if release_type == 'event' or release_type == 'tech':
				#CHANGE TO LOOP BAIL
				continue
		except:
			release_type = "NaN"


		#get artist and title from hyphenated title
		artist_title = str(soup.body.header.find_all("h1")[0])[4:-5]

		#split artist from title. store both.
		try:
			artist_title = artist_title.split("-")
		except:
			#if no data here, it's wack - go on to next entry
			pass

		try:
			artist = artist_title[0]
		except:
			artist = "NaN"

		if artist == "Reviews":
			#when we query a link that's not a review, RA takes us to the general review page
			#since we're scrapting the title here, a title as "Review" means we didnt get anything.
			continue

		try:
			release_title = artist_title[1]
		except:
			release_title = "NaN"

		#get chunk of data containing release info and rating
		try:
			release_data = soup.main.aside.find_all("li")
		except:
			#if no data here, it's wack - go on to next entry
			continue

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

		#handle style
		try:
			style = release_data[2].contents[-1][1:-1]
		except:
			style = "NaN"

		#handle comments
		try:
			num_comments = release_data[3].contents[2][1:-3]
		except:
			num_comments = "0"

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
			continue

		#chop out review body
		try:
			review_body = str(body_span[3]).replace("\r","")[58:-8]
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

		csvwriter.writerow([i,release_type,artist,release_title,label,release_month,style,num_comments,rating,review_published,author,review_body,tracklist])
			# csvwriter.writerow([i,release_type,artist,release_title,label,release_month,style,num_comments,rating,review_published,author,tracklist])


		# print(soup.prettify())

		print(i)
		if verbose:
			print("release_type= " + release_type)
			print("artist= " + artist)
			print("release_title= " + release_title)
			print("label= " + label)
			print("release_month= " + release_month)
			print("style= " + style)
			print("num_comments= " + num_comments)
			print("rating= " + rating)
			print("review_published= " + review_published)
			print("author= " + author)
			print("review_body= " + review_body)
			print("tracklist= " + tracklist)
		


