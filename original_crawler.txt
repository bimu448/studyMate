from selenium import webdriver
from bs4 import BeautifulSoup
import time
import getpass
import unittest

sel = webdriver.PhantomJS(executable_path='phantomjs.exe')

loginurl = 'https://www.student.auckland.ac.nz/psc/ps/EMPL\
OYEE/SA/c/NUI_FRAMEWORK.PT_LANDINGPAGE.GBL?languageCd=ENG'
sel.get(loginurl)
time.sleep(3)

    
#user account entry
try:
    upi = input("please enter ur upi: ")
    print(upi)
    sel.find_element_by_xpath("/html/body/div/main/div/div/div/div[2]/div[2]/fieldset/form/div[1]/input").send_keys(upi )

    print("user success")

except Exception as e:
    print(e)
    print("user error")

#password entry
try:
    pw = input("please enter ur password: ")
    #pw = getpass.getpass("please enter ur password: ")
    sel.find_element_by_xpath("/html/body/div/main/div/div/div/di\
v[2]/div[2]/fieldset/form/div[2]/div/input").send_keys(pw)
    print("pw success")

except:
    print("pw error")
time.sleep(3)

#click login button
try:
    sel.find_element_by_xpath("/html/body/div/ma\
in/div/div/div/div[2]/div[2]/fieldset/form/div[3]/button").click()
    print("login success")

except:
    print("login error")
time.sleep(5)

#go to classtale page
try:
    sel.find_element_by_xpath("/html/body/form/div[2]/div[4]/div[2]/d\
iv/div/div/div/div[3]/section/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/div[4]/div[1]/div").click()
    print("classtable success")

except:
    print("classtable error")

time.sleep(3)

"""
#go to next week
try:
    sel.find_element_by_xpath("/html/body/form/div[2]/div[4]/div[2]/di\
v/div/div/div/div[3]/div[3]/div/div/div[1]/div[3]/span/a").click()
    print("nextweek success")
except:

    print("nextweek error")
"""

#go to previous week
try:
    sel.find_element_by_xpath("/html/body/form/div[2]/div[4]/div[2]/di\
v/div/div/div/div[3]/div[3]/div/div/div[1]/div[1]/span/a").click()
    print("previous success")
except:
    print("previous error")

#waitting for page complete loadded
time.sleep(10)

#get elements
pageSource = sel.page_source
bs = BeautifulSoup(pageSource)


#course_list = bs.findAll("a", {"class":"ps-link"})
course_list = bs.findAll("td")

#close driver
sel.close()


#build a new dict
courses = []
course_dict = {'Monday':[], 'Tuesday':[], 'Wednesday':[], 'Thursday':[], 'Friday':[]}
for x in course_list:
    courses.append(x.get_text())

#simplelfy course_list
courses = courses[1:-2]

for x in range(len(courses)):
    if courses[x] == '\xa0':
        courses[x] = 'None'

#set up dict
for x in ['8:00AM', '9:00AM', '10:00AM', '11:00AM', \
          '12:00PM', '1:00PM', '2:00PM', '3:00PM' ,\
          '4:00PM', '5:00PM', '6:00PM']:
    point = courses.index(x)
    course_dict['Monday'].append(courses[point+1])
    course_dict['Tuesday'].append(courses[point+2])
    course_dict['Wednesday'].append(courses[point+3])
    course_dict['Thursday'].append(courses[point+4])
    course_dict['Friday'].append(courses[point+5])

for x in course_dict:
    for y in range(len(course_dict[x])-1, -1, -1):
        if course_dict[x][y] == 'None':
                   course_dict[x].pop(y)

for x in course_dict:
    new_list = []
    for y in course_dict[x]: 
        y = y.split("  ")
        
        time = ""

        for num in range(len(y)-1):
            if len(y) > 2:
                point = y[num+1].find(":")
                if point != -1:
                    if y[num+1][point-2].isdigit():
                        paper = y[num] + "  " + y[num+1][:point-2]
                    else:
                        paper = y[num] + "  " + y[num+1][:point-1]
                else:
                    point = y[num].rfind(":")
                    paper = y[num][point+5:] + "  " + y[num+1]
            else:
                
                paper = y[num] + "  " + y[num+1]
            
            time_point = paper.rfind(":")
            
            if time_point != -1:
                time = paper[:time_point+5]
                course_point = paper.rfind("  ")
                course = paper[time_point+5:course_point+5]
            else:
                course_point = paper.find("  ")
                course = paper[:course_point+5]
            location = paper[course_point+5:]
            new_paper = time + "&" + course + "&" + location + "&"
            
            new_list.append(new_paper)
        
    course_dict[x] = new_list
print(course_dict)
        




