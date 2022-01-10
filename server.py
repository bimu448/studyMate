from selenium import webdriver
from bs4 import BeautifulSoup
import time
import getpass

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.parse import parse_qs


class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/timetable.txt'
        
        file2 = open(self.path[1:]).read()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(file2, 'utf8'))
        
    def do_POST(self):
        if self.path == '/':
            self.path = '/timetable.txt'
        
        self.send_response(200)
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        up_list = str(post_data)[2:-1].split('&')
        upi = up_list[0]
        pwd = up_list[1]

        #parse part
        driver = webdriver.PhantomJS()
        url = 'https://www.student.auckland.ac.nz/psc/ps/EMPLOYEE/SA/c/NUI_FRAMEWORK.PT_LANDINGPAGE.GBL?languageCd=ENG'
        driver.get(url)
        time.sleep(5)

        try:
            driver.find_element_by_xpath("/html/body/div/main/div/div/div/div[2]/div[2]/fieldset/form/div[1]/input").send_keys(upi)
            print("Upi")
        except:
            print("Upi error")
        try:
            driver.find_element_by_xpath("/html/body/div/main/div/div/div/div[2]/div[2]/fieldset/form/div[2]/div/input").send_keys(pwd)
            print("Pwd")
        except:
            print("Pwd error")
        time.sleep(3)
        try:
            driver.find_element_by_xpath("/html/body/div/main/div/div/div/div[2]/div[2]/fieldset/form/div[3]/button").click()
            print("Login")
        except:
            print("Login error")
        
        time.sleep(60)
        
        ##timetable
        try:
            driver.find_element_by_xpath("/html/body/form/div[2]/div[4]/div[2]/div/div/div/div/div[3]/section/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/div[4]/div[1]/div").click()
            print("Timetable")
        except:
            print("Timetable error")
        
        time.sleep(30)
        
        ##previous week
        try:
            driver.find_element_by_xpath("/html/body/form/div[2]/div[4]/div[2]/div/div/div/div/div[3]/div[3]/div/div/div[1]/div[1]/span/a").click()
            print("Previous")
        except:
            print("Previous error")
        
        time.sleep(10)
        
        ##elements
        ps = driver.page_source
        bs = BeautifulSoup(ps)
        course_list = bs.findAll("td")
        
        ##close driver
        driver.close()
        print("Close Driver")

        courses = []
        course_dict = {'Monday':[], 'Tuesday':[], 'Wednesday':[], 'Thursday':[], 'Friday':[]}
        for i in course_list:
            courses.append(i.get_text())

        courses = courses[1:-2]

        for i in range(len(courses)):
            if courses[i] == '\xa0':
                courses[i] = 'None'

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
                time_point = y.rfind("PM")
                if time_point != -1:
                    time_frag = y[:time_point+2]
                    course_point = y.rfind(" ")
                    course = y[time_point+2:course_point+4]
                else:
                    time_point = y.rfind("AM")
                    time_frag = y[:time_point+2]
                    course_point = y.rfind(" ")
                    course = y[time_point+2:course_point+4]
                location = y[course_point+4:]
                new_list.append(time_frag + "&" + course + "&" + location)
            course_dic[x] = new_list

        file = open('timetable.txt', 'w')
        file.write(str(course_dict))
        file.close()

        file2 = open(self.path[1:]).read()
        print(file2)
        self.end_headers()
        
        self.wfile.write(bytes(file2, encoding='utf8'))


httpd = HTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()
