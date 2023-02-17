import json
from bs4 import BeautifulSoup
import requests

root ="https://directory.rpi.edu/pplsearch/NULL/NULL/"
f = open('names.json')
data = json.load(f)
output = {}

for prof in data['faculty_ids']:
    # get beautiful soup data
    html = requests.get(root + prof).text
    soup = BeautifulSoup(html,'lxml')
    # divide html into sections
    info = soup.find("div", class_='pplsearch-results-people container')
    name = info.find_next('h3').text
    sections = info.find_all("div", class_="col-12 col-md-4")
    # these are the primary sections:
    # contains email & phone:
    sub1 = sections[0].find_all('p') 
    # contains department & school:
    sub2 = sections[1].find_all('p')

    # create as blank strings
    email = ""
    phone = ""
    department = ""
    school = ""
    # loop through, find email/phone
    for sub_section in sub1:
        if sub_section.text[:5] == "Email":
            email = sub_section.text[7:].strip()
        elif sub_section.text[:5] == "Phone":
            phone = sub_section.text[7:].strip()
    #loop through, find departmnet/school
    for sub_section in sub2:
        if sub_section.text[:5] == "Depar":
            department = sub_section.find_next('a').text.strip()
        elif sub_section.text[:5] == "Portf":
            school = sub_section.find_next('a').text.strip()

    #add information to dictionary
    output[prof] = {"name": name, "email": email, "phone": phone, "department": department, "school":school}

#convert dictionary to json object with indentation
json_data = json.dumps(output, indent = 4)
#write json object to output file
with open("output.json", "w") as outfile:
    outfile.write(json_data) 
#close input file
f.close()
