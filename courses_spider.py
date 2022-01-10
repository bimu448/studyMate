from bs4 import BeautifulSoup
from urllib.request import urlopen
import pymysql
import time


url = "https://www.calendar.auckland.ac.nz/en/courses.html"
html = urlopen(url)
bs_obj = BeautifulSoup(html.read())
faculities = bs_obj.findAll("a", {"class":"linkTxt"})



#open database
db = pymysql.connect("35.244.108.13", "root", "123456", "uni_courses")
cursor = db.cursor()

count = 0
counts = 0
countss = 0


faculty_dict = {}
for x in faculities[1:-1]:
    depart_info = str(x)
    depart_link = depart_info[depart_info.find("href")+6: depart_info.find("html")+4]
    department = depart_info[depart_info.find("html")+6: depart_info.find("</a>")].strip()
    
    split_name = department.split()
    faculty_name = ''
    for part in split_name:
        parts = part[0].upper()+part[1:]
        faculty_name += parts
    faculty_name = faculty_name[0].lower() + faculty_name[1:]   
    faculty_dict[faculty_name] = depart_link

    
    #create table 
    cursor.execute("DROP TABLE IF EXISTS " + faculty_name)
    sql = "CREATE TABLE IF NOT EXISTS `%s`(\
   `department` VARCHAR(100),\
   `courseCode` VARCHAR(100) ,\
   `courseName` VARCHAR(100),\
   `courseDes` VARCHAR(5000),\
   `courseExtra` VARCHAR(5000),\
   `comments` VARCHAR(10000),\
   `announcement` VARCHAR(500),\
    PRIMARY KEY ( `courseCode` ));"%(faculty_name)
    cursor.execute(sql)

print("tables create successful")
time.sleep(10)
print("start insert info")

error_dict = {}
for x in faculty_dict:
    html = urlopen(faculty_dict[x])
    bs_major = BeautifulSoup(html.read())
    major_name = bs_major.findAll("a", {"class":"linkTxt"})
    print(x)
    major_dict = {}
    for y in major_name:
        major_info = str(y)
        major_link = major_info[major_info.find("href")+6: major_info.find("html")+4]
        major = major_info[major_info.find("html")+6: major_info.find("</a>")].strip()
        major_dict[major] = major_link
       
    for z in major_dict:
        html = urlopen(major_dict[z])
        bs_courses = BeautifulSoup(html.read())
        course = bs_courses.findAll("div", {"class":"coursePaper section"})
       
        
        for c in course:
            course_info = str(c)
            course_code = course_info[course_info.find('/a>')+4: course_info.find('</div')].strip()
            course_name = course_info[course_info.find('<p class="title">')+17: course_info.find('<p class="description">')-5].strip()
            course_des = course_info[course_info.rfind('<p class="description">')+23: course_info.find('<p class="prerequisite">')-5].strip()
            if course_info.find('<i>') == -1:
                course_extra = "null"
            else:
                course_extra = course_info[course_info.find('<i>')+3: course_info.find('</i>')].strip()
            
            #insert data
            
            try:
                
                
                sql = 'INSERT INTO %s VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s");'%(x, z, course_code, course_name, course_des, course_extra, "", "")
                cursor.execute(sql)
                db.commit()
                
            except Exception as e:
                try:
    
                    letters_l = 'zxcvbnmkljhgfdsaqwertyuiop'
                    letters_u = letters_l.upper()

                    for l in sql:
                        if l.isalpha():
                            if l not in letters_l and l not in letters_u:
                                sql = sql[:sql.find(l)]+sql[sql.find(l)+1:]
                    #sql = sql.replace("'", "`")
                    #sql = sql.replace('"', '`')

                    cursor.execute(sql)
                    db.commit()
                    
            
                except Exception as e:
                   error_dict[course_code] = str(e)

            
            
            
            countss += 1
            
        counts += 1
        
    count += 1

print("courses:", countss)
print("majors:", counts)
print("faculty:", count)
db.close()

print("error information:")    
for x in error_dict:
    print("   {}: {}".format(x, error_dict[x]))
