from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime,timedelta


#print(data)
def get_Data():
    setJson()
    get_webpageData()
    get_nextcall()

    print("Get Data done")

def setJson():
    now = datetime.now()
    current_date = now.strftime("%m/%d")
    current_date = now.strftime("%m/%d")
    tomorrow_0= now+ timedelta(1)
    tomorrow= tomorrow_0.strftime("%m/%d")
    data={ "today":current_date,"tomorrow":tomorrow}
    with open('time.json', 'w') as fp:
        json.dump(data, fp, indent=4, sort_keys=True)

def get_webpageData():

    url='https://tithen-firion.github.io/warframe/poe.html'
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)  # ensure the page is fully loaded

    # Render the dynamic content to static HTML
    html = driver.page_source
    #print(html)

    # Parse the static HTML
    soup = BeautifulSoup(html, "html.parser")
    divs = soup.findAll("div", {"class": "night"})
    divs.pop(0) #useless data
    setJson()
    format(divs)

def format(divs):
    with open('time.json','r',encoding='utf8') as s:
        datax = json.load(s)
    tom=0
    n=0
    current_date=datax['today']
    tomorrow=datax['tomorrow']
    data={current_date:{},tomorrow:{}}
    for i in range(len(divs)-2): 
        xtime=str(divs[i].text[0])+str(divs[i].text[1]) #hours
        ytime=str(divs[i+1].text[0])+str(divs[i+1].text[1]) #hours

        xtime=int(xtime)
        ytime=int(ytime)
        
        if xtime<ytime and tom==0:
            z=divs[i].text
            z0=z[:5]
            z1=z[11:16]
            data[current_date][n]=z0 +' - '+ z1
            n+=1
        elif xtime>ytime and tom==0: #next_day
            z=divs[i].text
            z0=z[:5]
            z1=z[11:16]
            data[current_date][n]=z0 +' - '+ z1
            n=0
            tom=1
        elif xtime<ytime and tom==1:
            z=divs[i].text
            z0=z[:5]
            z1=z[11:16]
            data[tomorrow][n]=z0 +' - '+ z1
            n+=1
        elif xtime>ytime and tom==1:
            z=divs[i].text
            z0=z[:5]
            z1=z[11:16]
            data[tomorrow][n]=z0 +' - '+ z1
            tom=2
    
    with open('time.json','r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.update(data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
            
def get_nextcall():
    print('-----get_nextcall() called at:',datetime.now().strftime("%H:%M"),'-----')
    with open('time.json','r',encoding='utf8') as s:
        datax = json.load(s)
    current_date=datax['today']
    tomorrow=datax['tomorrow']
    if current_date != datetime.now().strftime("%m/%d"):
        get_webpageData()
        with open('time.json','r',encoding='utf8') as a:
            datax = json.load(a)
        current_date=datax['today']
        tomorrow=datax['tomorrow']
        
    data={'nextcall':0}
    current_hour = int(datetime.now().strftime("%H"))#%H:%M
    current_min = int(datetime.now().strftime("%M"))
    #print('current hour,min',current_hour,':',current_min)
    se=0
    for i in datax[current_date]:#i=0 1 2 ....type=str
        # print('today[i+1]',datax[current_date][i])
        th=int(datax[current_date][i][0]+datax[current_date][i][1])  #next calltime:hour
        tm=int(datax[current_date][i][3]+datax[current_date][i][4])  #next calltime:minute
        if  th>current_hour and not se:
            se=1
            print('th:tm=',th,':',tm)
            # print('th>current_hour:')
            # print(datax[current_date][i])
            data['nextcall']=datax[current_date][i]
        elif  th==current_hour and not se:
            print('th:tm=',th,':',tm)
            if tm>current_min: 
                se=1
                # try:
                print('th=ch,tm>current_min:')
                print('today[i]',datax[current_date][i])  
                data['nextcall']=datax[current_date][i]
                # except:
                #     print('th=ch,tm>=current_min:')
                #     print('tomorrow[0]',datax[tomorrow]['0'])
                #     data['nextcall']=datax[tomorrow]['0']
            else:
                try:
                    print('th=ch,tm<current_min:')
                    ip=str(int(i)+1)
                    print('today[i+1]',datax[current_date][ip])
                    data['nextcall']=datax[current_date][ip]
                except:
                    print('th=ch,tm<current_min:')
                    print(datax[tomorrow]['0'])
                    data['nextcall']=datax[tomorrow]['0']
        # else:
        #     print('th<ch',th,current_hour,'  i=',i)
        
    if data['nextcall']== 0: #ex:05/16 23:34 nextcall 05/17 00:38
        data['nextcall']=datax[tomorrow]['0']
        
    #print(data['nextcall'])
    data['nextcall']=data['nextcall'][0:5]
    print('from getData-data[nextcall]:',data['nextcall'])
    with open('time.json','r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.update(data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
    
    print('------------------------------')
    
get_Data()
