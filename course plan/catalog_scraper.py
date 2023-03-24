from bs4 import BeautifulSoup
import unicodedata
import requests
import json

base_url = "http://catalog.rpi.edu/"

html_text = requests.get('http://catalog.rpi.edu/content.php?catoid=24&navoid=604', headers={'Accept-Encoding': 'utf-8'}).content
soup = BeautifulSoup(html_text,'lxml')

#Find all programs on the page
program_list = soup.find('ul', class_='program-list')
programs = program_list.find_all('li')\

#dictionary for output data
output_list = []

#loop through each program
for program in programs:
    #find <a> element, get name
    data = program.find('a')
    name = data.text

    program_dict = {"Major": name}
    
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
    program_years = section.find_all('div', recursive=False)
    #we only want data under these years:
    valid_years = ["First","Secon","Third","Fourt","Fifth"]

    #loop through each year of courses
    prev_year = None
    year = 0
    for year_data in program_years:
        # if we have an 'acalog-core' div, we get the year
        if 'acalog-core' in year_data.get('class'):
            title = year_data.find_next('h2').text
            #check if this element is data we want
            #if not, we check the next thing    
            if title[:5] not in valid_years:
                prev_year = "n/a"
                continue
            year+=1
            prev_year = title
        # if other div, get information
        else:
            if prev_year == "n/a":
                continue

            #set "Year" portion
            year_sl = prev_year[:5]
            if year_sl=="First":
                program_dict.update({"Y1":"First Year"})
            elif year_sl=="Secon":
                program_dict.update({"Y2":"Second Year"})
            elif year_sl=="Third":
                program_dict.update({"Y3":"Third Year"})
            elif year_sl=="Fourt":
                program_dict.update({"Y4":"Fourth Year"})
            elif year_sl=="Fifth":
                program_dict.update({"Y5":"Fifth Year"})

            # get array of each semester
            semester_data = year_data.find_all('div', class_ = 'acalog-core')
            sem_counter = 0
            # for each semester:
            for semester in semester_data:
                sem_counter += 1
                header = semester.find_next('h3')
                if header == None:
                    sem_key = "Error"
                    program_dict.update({sem_key:"text"})
                    continue
                text = header.text
                #concatenate year and semester num (ex: Y2S1 = year 2, semester 1)
                sem_key = "Y" + str(year) + "S" + str(sem_counter)
                
                course_list = []
                course_list.append(text)

                course_blocks = semester.find_all('ul')
                for block in course_blocks:
                    courses = block.find_all('li')
                    for course in courses:
                        #here, we get the actual course information
                        course_info = course.text

                        # course_info.replace("\n", ' ').replace("\t", " ")

                        # Remove "(see footnote: etc...)"
                        # note: if in the future these footnote indications are desired,
                        # this portion of code may be modified
                        note_ind = course_info.find('(See')
                        if note_ind == -1:  ##check alternate forms
                            note_ind = course_info.find('( See')
                        if note_ind == -1:
                            note_ind = course_info.find('(see')
                        if note_ind == -1:
                            note_ind = course_info.find('[See')

                        # Remove this any following text from the code
                        if note_ind != -1:
                            course_info = course_info[:note_ind]

                        # remove any \n
                        x= course_info.find('\n')
                        if (x != -1):
                            course_info = course_info[0:x] + course_info[x+1:]
                        # remove any \t
                        x= course_info.find('\t')
                        if (x != -1):
                            course_info = course_info[0:x] + course_info[x+1:]

                        if len(course_info) > 2:
                            course_list.append(course_info)

                program_dict.update({sem_key:course_list})

    output_list.append(program_dict)


with open('degree_template.json', 'w', encoding='UTF-8') as f:
    json.dump(output_list, f, ensure_ascii=False, indent=4)






