from bs4 import BeautifulSoup
import os
import urllib
import webbrowser
import time
import authenticate as auth
import prettify as pr


def main(email,password,cour_id):        
    url = "https://class.coursera.org/"+ cour_id + "/lecture"
    
    coursera_session = auth.auth_me(email,password)
    if coursera_session == -1:
        print "Login failed!"
        return
    print "A folder with the name " + cour_id + " will be created on your Desktop"    
    cont = coursera_session.get(url, timeout=3)
    soup = BeautifulSoup(cont.text, 'html.parser')
    
    cur_dir = os.getcwd()
    new_dir = cur_dir.split("/")
    new_dir = "/" + new_dir[1] + "/" + new_dir[2]
    
    os.chdir(new_dir+"/Desktop")
    os.mkdir(cour_id)
    os.chdir(cour_id)
    
    
   
    week_tags=[]
    for week in soup.find_all("div",{"class":"course-item-list-header"}):
        week_tags.append(((week.find("h3").text).strip()).encode("utf-8"))
        
   
    index = 0 
    
    for week in (soup.find_all("ul",{"class":"course-item-list-section-list"}))[0:2]:     
        cour_ind=1
        print     
        print "Week No : ",index
        print "-------------"    
        os.mkdir(week_tags[index])
        os.chdir(week_tags[index])   
        for data in week.find_all("li"):
            tag = str(cour_ind) + ". " + (data.find("a").text).strip()
            
            print "Video Lecture No : ",cour_ind
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
                    odd+=1
                else:
                    pass
                    #webbrowser.open(url)
                    #time.sleep(2)               
                    
                
            os.chdir("..")
        #print os.getcwd()
        index = index + 1
        os.chdir("..")
        time.sleep(5)
    
    path = new_dir + "/Downloads/"
    to_save = new_dir + "/Desktop/" + cour_id + "/"
    
    pr.prettify(path, to_save, week_tags)
    
    
if __name__ == "__main__":
   
    email = str(raw_input("Enter registered email address : "))    
    password = str(raw_input("Enter password : "))    
    cour_id = str(raw_input("Enter Coursera Course ID : ")) 
    print 
    main(email, password, cour_id)
    