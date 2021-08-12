import requests, re, json
from bs4 import BeautifulSoup

original_link = "https://www.zillow.com/homes/97222_rb/"  # gets the URL for the bs4 link to parse through for the zip code

headers = {"accept": "*/*",
       "accept-encoding": "gzip, deflate, br",
       "accept-language": "en-US, en;q=0.9",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'} #this is the header for the website so it will allow to scrape the site.
House_Info = {}
class zillow: #this allows for information of the above link to be stored in a class format.
    def __init__(self, link, headers):
        self.link = link
        self.headers = headers
    def request(self):
        with requests.Session() as self.s:
            self.r = self.s.get(self.link, headers = self.headers)
            return self.r
       
class_link = zillow(original_link, headers)
urls = class_link.request()


soup = BeautifulSoup(urls.text, "html.parser") #Sends the BS4 request.

prices = [i.text for i in soup.find_all("div", {"class": "list-card-price"})] #Gets the prices of the house

for i in soup.find_all("ul", {"class":"photo-cards photo-cards_wow photo-cards_short photo-cards_extra-attribution"}): #from here, this part of the script parses through the data and gets the relivent information looking at the HTML format.
    for j in i.find_all("div", {"class": "list-card-top"}):
        house_links = ''.join(re.findall(r'https://www.zillow.com/homedetails.*zpid/', str(j)))
        individual_houses = zillow(house_links, headers)
        each_houses = individual_houses.request()
        house_soup = BeautifulSoup(each_houses.text, "html.parser")
        house_list = []
        address_list = []
        [house_list.append(i.text) for i in house_soup.find("ul", {"class": "sc-pspzH hhcidC"})]
        new_house_list = " ".join(house_list)
        House_Info[house_links] = [new_house_list] #Uses the class to input this information as a list
        for house in house_soup.find("h1", {"class": "Text-c11n-8-18-0__aiai24-0 StyledHeading-c11n-8-18-0__ktujwe-0 efSAZl"}):
            address_list.append(house.text) #appends the text to another list as this was a unicode format.
        address_list2 = [i.replace("\xa0", "") for i in address_list] #gets rid of anything with the character in order to better organize the data
        House_Info[house_links].append("".join(address_list2))
x = House_Info.popitem() #gets rid of the last line.
y = prices.pop()#gets rid of the first line in the list.
json_object = json.dumps(House_Info, indent = 2) #imports this object into a json format.

