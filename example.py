import unidecode
import WebFunctions
import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def ConnectDB():
        ReturnObject = dict()
        #Changing of path may be required
        #Also install sqlite db browser @ https://sqlitebrowser.org/dl/
        connection = sqlite3.connect("E:\\Users\\Mike\\Python\\pythonfuntime\\pythonfuntime\\subjob.db")
        connection.row_factory = dict_factory
        cursor     = connection.cursor()
        ReturnObject['connection'] = connection
        ReturnObject['cursor']     = cursor
        return ReturnObject

url = "https://www.aesopcanada.com/login2.asp"
username = '3065298525'
password = '1971'
DW = ConnectDB()

driver = WebFunctions.open_url(url, 120)
WebFunctions.fill_text_box("//input[@id='txtLoginID']", username, driver)
WebFunctions.fill_text_box("//input[@id='txtPassword']", password, driver)
WebFunctions.click_button("//a[@id='loginLink']",driver)
WebFunctions.click_button("//*[@id='ui-id-2']", driver)
table_location = WebFunctions.find_all_elements_xpath("//div[@id='scheduledJobs']",driver)[0]
soup = WebFunctions.BeautifulSoup(table_location.get_attribute('innerHTML'), "html.parser")
Table = soup.find('table')
job_list = []
for row in Table.findAll('tr',{"class": "detail"}):
    data = {}
    columns = row.findAll('td')
    data['Date'] = columns[0].get_text()
    data['Time'] = columns[1].get_text()
    data['School'] = unidecode.unidecode(columns[3].get_text())
    job_list.append(data)
index = 0
for row in Table.findAll('tr',{"class": "summary"}):
    columns = row.findAll('span')
    job_list[0]['Teacher'] = columns[0].get_text()
    job_list[0]['Role'] = columns[1].get_text()
    index += 1
for job in job_list:
    print(job)
    input_data = (job['Date'],job['Time'],job['School'],job['Teacher'],job['Role'])
    DW['cursor'].execute('INSERT INTO job (Date,Time,School,Teacher,Role) Values (?,?,?,?,?)', input_data)
    DW['connection'].commit()
