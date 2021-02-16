import requests, re, json
from bs4 import BeautifulSoup

if __name__=="__main":
    print("Executing Script Now")
else:
    print("Executing Script")


original_link = "https://www.zillow.com/homes/97222_rb/"

headers = {"accept": "*/*",
       "accept-encoding": "gzip, deflate, br",
       "accept-language": "en-US, en;q=0.9",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
House_Info = {}
class zillow:
    def __init__(self, link, headers):
        self.link = link
        self.headers = headers
    def request(self):
        with requests.Session() as self.s:
            self.r = self.s.get(self.link, headers = self.headers)
            return self.r
       
class_link = zillow(original_link, headers)
urls = class_link.request()


soup = BeautifulSoup(urls.text, "html.parser")

prices = [i.text for i in soup.find_all("div", {"class": "list-card-price"})]

for i in soup.find_all("ul", {"class":"photo-cards photo-cards_wow photo-cards_short photo-cards_extra-attribution"}):
    for j in i.find_all("div", {"class": "list-card-top"}):
        house_links = ''.join(re.findall(r'https://www.zillow.com/homedetails.*zpid/', str(j)))
        individual_houses = zillow(house_links, headers)
        each_houses = individual_houses.request()
        house_soup = BeautifulSoup(each_houses.text, "html.parser")
        house_list = []
        address_list = []
        [house_list.append(i.text) for i in house_soup.find("ul", {"class": "sc-pspzH hhcidC"})]
        new_house_list = " ".join(house_list)
        House_Info[house_links] = [new_house_list]
        for house in house_soup.find("h1", {"class": "Text-c11n-8-18-0__aiai24-0 StyledHeading-c11n-8-18-0__ktujwe-0 efSAZl"}):
            address_list.append(house.text)
        address_list2 = [i.replace("\xa0", "") for i in address_list]
        House_Info[house_links].append("".join(address_list2))
x = House_Info.popitem()
y = prices.pop()
json_object = json.dumps(House_Info, indent = 2)

