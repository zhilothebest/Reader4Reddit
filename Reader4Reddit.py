import time
import requests
import requests.auth
import asciimatics
import asciimatics.event as event
import asciimatics.screen as screen
import logging
import sys
import ctypes


logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)



token =""


def get_token():
	client_auth = requests.auth.HTTPBasicAuth("Your dev ID","Your Silent")
	post_data = {"grant_type":"password", "username":"your_user","password":"your_pass"}
	headers = {"User-Agent": "Reader for Reddit by zhilothebest"}
	response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
	token_array = response.json()
	token = token_array["access_token"]
	return token

def get_JSON(url, token):
	headers = {"Authorization" : "bearer "+ token ,"User-Agent": "Reader for Reddit by zhilothebest"}
	response = requests.get(url, headers = headers)
	json = response.json()
	return json


# Reader for not reddit reader because im following copyright laws
print('''
####################################
#                                  #
#              READER              #                   
#                4                 #
#              REDDIT              #
#                                  #
####################################
''')


''' Getting original token'''
token= get_token()
'''Getting JSON code for links'''
sub_reddit = input("\nWhich subreddit would you like to read? Type out what the URL would be after /r/________. \n")
sub_url = str("https://oauth.reddit.com/r/"+ sub_reddit + ".json?limit=25")
json = get_JSON(sub_url,token)

'''Get Info from links, made global for easy access '''
global content_array
content_array = []
global id_array 
id_array = []
global score_array 
score_array= []
global author_array 
author_array=[]
global title_array
title_array = []


for link_num in range(0,len(json["data"]["children"])):
	id_array.append(json["data"]["children"][link_num]["data"]["id"])
	score_array.append(json["data"]["children"][link_num]["data"]["score"])
	author_array.append(json["data"]["children"][link_num]["data"]["author"])
	title_array.append(json["data"]["children"][link_num]["data"]["title"])

	if "selftext" in json["data"]["children"][link_num]["data"]:
		content_array.append(json["data"]["children"][link_num]["data"]["selftext"])

	if "preview" in json["data"]["children"][link_num]["data"]:
		content_array.append(json["data"]["children"][link_num]["data"]["preview"]["images"][0]["source"]["url"])

global read_dict 
read_dict= {id_array[iteration] : False for iteration in range(0, len(id_array))}
global location
location = [4,0]



'''List of input keys'''
global key_q
key_q= str(event.KeyboardEvent(ord("q")))
global key_up
key_up = str(event.KeyboardEvent(-204))
global key_down
key_down = str(event.KeyboardEvent(-206))
global key_left
key_left = str(event.KeyboardEvent(-203))
global key_right
key_right = str(event.KeyboardEvent(-205))


''' figure out a way to combine self text and picture url array, so it displays the same'''
''' writing this definition hear so I can easily read my parsing function.'''

def link_color(id):
	if(read_dict[id] == False):
		white = 7
		return white
	else:
		blue = 4
		return blue

def loc_num(location):
	number = location/2 - 2
	number = int(number)
	return number

def demo(screen):
	i = 0
	screen.set_title("Reader4Reddit")
	logging.debug("Title placed")
	page = 0
	

	while( i== 0):
		if (screen.has_resized() == True ):
			screen.refresh()
	
		''' OUTPUTS'''
		if(location[1]==0):
			screen.print_at("Use the Up and Down arrow keys to choose links.", 0,0)
			screen.print_at("Use the Right arrow key to view a link, and Left to exit the link.",0,1)
			screen.print_at("Use the Q key to exit the application, and ___ to change subreddits.",0,2)
			screen.print_at("-->", 0,location[0])

			if (page == 0):
				for link in range(0,9):
					screen.print_at(title_array[link], 6 , 2*link + 4,link_color(id_array[link])) 
				screen.print_at("Keep scrolling down for more links.", 0, 24)
			elif(page == 1):
				for link in range(0,9):
					screen.print_at(title_array[link+10], 6 , 2*link + 4,link_color(id_array[link]))
				screen.print_at("Keep scrolling down for more links.", 0, 24)
			else:
				for link in range(0,len(title_array)-20):
					screen.print_at(title_array[link+20], 6 , 2*link + 4,link_color(id_array[link]))


			screen.refresh()
		else:
			num = loc_num(location[0])
			ctypes.windll.user32.MessageBoxW(0,content_array[num],title_array[num],0)
			screen.refresh()


		'''INPUTS'''	

		user_input = screen.get_event()
		str_input = str(user_input)

		if(str_input == key_down):
			if(location[0]== 24):
				pass
			else:
				location[0] = location[0] + 2
				if (location[0]>20 and page <2):
					page += 1
					location[0] = 4
				screen.clear()
				

		if(str_input == key_up):
			if(location[0]== 4):
				if (page != 0):
					page -= 1
					location[0]=20
					screen.clear()
				else:
					pass
			else:
					
				location[0] = location[0] - 2

				screen.clear()


		if(str_input == key_left):
			if(location[1]==0):
				pass
			else:
				location[1] = location[1] - 1
				screen.clear()
				

		if(str_input == key_right):
			if(location[1]== 1):
				pass
			else:
				location[1] = location[1] + 1
				id_num = int(loc_num(location[0]))
				if(read_dict[id_array[id_num]]== False):   # This is a really messy code, couldnt figure out what to name everything
					read_dict[id_array[id_num]] = True

				screen.clear()


		if(str_input == key_q): 
			logging.debug("THEY MATCHED")
			i += 1
			sys.exit()
		

		time.sleep(.0001)


screen.Screen.wrapper(demo)
