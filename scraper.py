#coding=UTF8

from bs4 import BeautifulSoup
import requests
import re
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

############
# CONTROLS #
############
#get this from residentadvisor.com
latest_review_id = 21921
#set as either number of pulls to try or "full" 
#pulls 25 in about 32 seconds -- full run will take almost 8 hours(!)
num_pulls = "full"
verbose = False
###########

if (num_pulls == "full"):
	num_pulls = latest_review_id - 1


link_base = "https://www.residentadvisor.net/reviews/"

with open('RA.csv', 'wb') as csvfile:
	csvwriter = csv.writer(csvfile, delimiter=';')
	csvwriter.writerow(["ra_review_id","release_type","artist","release_title","label","release_month","release_year","style","num_comments","rating","review_published","author","review_body","tracklist"])
	# csvwriter.writerow(["ra_review_id","release_type","artist","release_title","label","release_month","style","num_comments","rating","review_published","author","tracklist"])


	# for i in range(latest_review_id,latest_review_id - num_pulls,-1):
	for i in repull_author_list:

		url = link_base + str(i)

		# uncomment below to test single row
		# r = requests.get("https://www.residentadvisor.net/reviews/6323")
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
			#handle strange unicode character that sometimes shows up
			if "-" in artist_title:
				artist_title = artist_title.split("-")
			else:
				artist_title = artist_title.split("\xe2\x80\x93 ")
		except:
			#if no data here, it's wack - go on to next entry
			continue

		try:
			artist = artist_title[0].replace("&amp;","&").rstrip()
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

		#
		# A smarter way to deal with release data, as some may be missing
		#

		#initiallize all values to NaN in case they don't get filled
		label = "NaN"
		release_month = "NaN"
		num_comments = "NaN"
		rating = "NaN"
		style = "NaN"

		#get number of attributes in release_data chunk
		release_data_length = len(release_data)

		#loop through each, check the attribute, handle accordingly and assign
		for j in range(0,release_data_length):
			
			field = str(release_data[j].contents[1])[6:-9]

			if field == "Label" or field == "レーベル":
				#handle label
				try:
					label = re.findall(">.*<",str(release_data[j].contents[3]))[0][1:-1].encode("utf-8").replace("&amp;","&")
				except:
					label = "NaN"
			elif field == "Released" or field == "発売":
				#handle release month
				try:
					release_month = release_data[j].contents[-1][1:-1]
					release_year = release_month[-4:]
					release_month = release_month[:-5]
				except:	
					release_month = "NaN"
			elif field == "Comments" or field == "コメント":
				#handle comments
				try:
					if release_data[j].contents[2] == '\n':
						num_comments = "0"
					else:
						num_comments = release_data[j].contents[2][1:-3]
				except:
					num_comments = "0"
			elif field == "Rating" or field == "評価":
				#handle rating
				try:
					rating = re.findall('g">.*<s',str(release_data[j].contents[3]))[0][3:-2]
				except:
					rating = "NaN"
			elif field == "Style" or field == "スタイル":
				#handle style
				try:
					style = release_data[j].contents[-1][1:-1].encode("utf-8")
				except:
					style = "NaN"
			else:
				continue



		#
		# gather chunk containing review body, tracklist, date published and author
		#
		try:
			body_span = soup.main.find_all('span')
		except:
			continue

		#chop out review body
		try:
			review_body = str(body_span[3]).replace("\r","")[58:-8].replace("&amp;","&")
		except:
			review_body = "NaN"

		#chop out date review published
		try:
			review_published = body_span[5]['datetime']
		except:
			review_published = "NaN"

		#handle a case where a reviewer with a profile will create extra entry in review_body
		#this affects where to look for author and tracklist		
		review_profile_flag = 0
		if "profile" in str(body_span[7]):
			review_profile_flag = 1

		#chop out author
		try:
			if review_profile_flag:
				author = re.findall('reviewer">.*<',str(body_span[7]))[0][10:-8].encode("utf-8")
			else:
				author = str(body_span[7])[7:-8]
		except:
			author = "NaN"

		#chop out tracklist
		try:
			if review_profile_flag:
				tracklist = str(body_span[13]).replace("\r<br/>",',')[6:-7]
			else:
				tracklist = str(body_span[12]).replace("\r<br/>",',')[6:-7]
		except:
			tracklist = "NaN"

		csvwriter.writerow([i,release_type,artist,release_title,label,release_month,release_year,style,num_comments,rating,review_published,author,review_body,tracklist])

		# print(soup.prettify())

		print(i)
		if verbose:
			print("release_type= " + release_type)
			print("artist= " + artist)
			print("release_title= " + release_title)
			print("label= " + label)
			print("release_month= " + release_month)
			print('release_year= ' + release_year)
			print("style= " + style)
			print("num_comments= " + num_comments)
			print("rating= " + rating)
			print("review_published= " + review_published)
			print("author= " + author)
			print("review_body= " + review_body)
			print("tracklist= " + tracklist)
		



