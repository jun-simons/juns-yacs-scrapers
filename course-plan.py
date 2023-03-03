from bs4 import BeautifulSoup
import requests
import json

base_url = "http://catalog.rpi.edu/"

html_text = requests.get('http://catalog.rpi.edu/content.php?catoid=24&navoid=604', headers={'Accept-Encoding': 'utf-8'}).content
soup = BeautifulSoup(html_text,'lxml')

#Find all programs on the page
program_list = soup.find('ul', class_='program-list')
programs = program_list.find_all('li')


#dictionary for output data
output = {}
#loop through each program
for program in programs:
    #find <a> element, get name
    data = program.find('a')
    name = data.text
    
    #open each link to gather more data
    html = requests.get(base_url + data['href']).text
    program_soup = BeautifulSoup(html,'lxml')
    #get relavent section 
    section = program_soup.find('td', class_ = 'block_content_outer').find_next('div', class_="custom_leftpad_20")

    #if section does not contain any course information
    #ex: "Program for Graduates of Naval Nuclear Power" as of 2/2/23
    if section == None:
        continue

    #get array of program years
    program_years = section.find_all('div')
    #we only want data under these years:
    valid_years = ["first","secon","third","fourt","fifth"]

    #loop through each year of courses
    for year_data in program_years:
        if 'acalog-core' not in year_data.get('class'):
            continue
        title = year_data.find_next('h2').text
        
        print(title)
        #check if this element is data we want
        #if not, we check the next thing
        if title[:5] not in valid_years:
            continue




    
    # print(data)


    output[name] = {}

# .find_all('li')
# for p in program_list:
#     print(p)




