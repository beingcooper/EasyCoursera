from bs4 import BeautifulSoup
import os
import urllib
import webbrowser
import time
import authenticate as auth
import prettify as pr
import getpass as gp
import platform as pf


def get_ctime(file):
    attr_list = []
    fl_stat = os.stat(file)
    attr_list = time.ctime(fl_stat.st_ctime).split() 
    return attr_list[2] + "-" + attr_list[3]


def main(email,password,cour_id,new_dir):        
    url = "https://class.coursera.org/"+ cour_id + "/lecture"    
    coursera_session = auth.auth_me(email,password)
    if coursera_session == -1:
        print "Login failed!"
        return
    
    cont = coursera_session.get(url, timeout=30)
    soup = BeautifulSoup(cont.text, 'html.parser')
        
    week_tags=[]
    for week in soup.find_all("div",{"class":"course-item-list-header"}):
        week_tags.append(((week.find("h3").text).strip()).encode("utf-8"))
        
    if len(week_tags) == 0:
	print "Either incorrect course ID or you are not enrolled in that course!"
	print "(Make sure you have accepted the Honor Code of that course)"
	return  
    
    os.chdir(new_dir+"/Desktop")
    os.mkdir(cour_id)
    os.chdir(cour_id)
    
    
    
    index = 0 
    tot_files=0
    time_attr = time.ctime().split()
    st_time = time_attr[2] + "-" + time_attr[3]
    
    for week in (soup.find_all("ul",{"class":"course-item-list-section-list"})):     
        cour_ind=1
        print     
        print "Entered Week No :",index
        print "#####################"    
        os.mkdir(week_tags[index])
        os.chdir(week_tags[index])   
        
        for data in week.find_all("li"):
            tag = str(cour_ind) + ". " + (data.find("a").text).strip()
            tag=tag.replace("/","-")
            print "Downloading Lecture :",tag
            cour_ind+=1
            try:
                os.mkdir(tag)
                os.chdir(tag)
                loc = os.getcwd()
            except:
                pass
            len_links = len(data.find("div").find_all("a"))
            odd = 0
            for link in (data.find("div").find_all("a"))[len_links-2:len_links]:
                url = link.get("href")
                if odd == 0:
                    urllib.urlretrieve(url,loc+"/subtitle.srt")
                    tot_files+=1
                    odd+=1
                else:                    
                    webbrowser.open(url)
                    time.sleep(2)               
                    
                
            os.chdir("..")
        
        index = index + 1
        os.chdir("..")
        time.sleep(4)
    
    path = new_dir + "/Downloads/"
    to_save = new_dir + "/Desktop/" + cour_id + "/"   
    print 
    print "Downloading of files will take some time, depending on your internet."
    print 
    
    file_count = 0
    while(file_count < tot_files):
        file_count=0
        for fl in os.listdir(path):
            if get_ctime(path + fl) > st_time:
                file_count+=1
        time.sleep(15)    
    
    print "All files downloaded." 
    pr.prettify(st_time,path, to_save, week_tags)
    print "A course folder with the name "+ cour_id + " is created on your desktop."
    print "Thank you for using EasyCoursera. Happy to Help :)"
    

def start():
    
    print "\n**Make sure you are logged in to your Coursera Account from your default web browser**\n"
    email = str(raw_input("Enter registered email address : "))    
    password = str(gp.getpass("Enter password (Typing will be hidden): "))    
    cour_id = str(raw_input("Enter Coursera Course ID : ")) 
    print 
    
    cur_os = pf.system()
    cur_user = gp.getuser()
    if cur_os == "Windows":
    	new_dir = "C:/Users/"+cur_user
    else:
    	new_dir = "/home/"+cur_user

    
    main(email, password, cour_id, new_dir)
    
