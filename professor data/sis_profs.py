from bs4 import BeautifulSoup

with open('arch4050.html', 'r') as html_file: 
    content = html_file.read()
    
    soup = BeautifulSoup(content, 'lxml')
    table = soup.find('td', class_='dddefault').find('table', class_='datadisplaytable')
    email = table.find_next('a').get("href")[7:]

    id = email[:email.find('@')]
    print(id)
