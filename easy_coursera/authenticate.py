import requests
from bs4 import BeautifulSoup
import string
import random
 

def auth_me(email,password):
    
    user_agent = ("Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36") 
 
    
    def randomCookie(length):
        return ''.join(random.choice(string.letters + string.digits) for i in xrange(length))
     
     
    def make_soup(url):
        html = requests.get(url)
        soup = BeautifulSoup(html.content)
        return soup
        
    signin_link = "https://accounts.coursera.org/api/v1/login"
    signin_info = {"email": email,
                     "password": password,
                     "webrequest": "true"
                     }
     
    XCSRF2Cookie = 'csrf2_token_%s' % ''.join(randomCookie(8))
    XCSRF2Token = ''.join(randomCookie(24))
    XCSRFToken = ''.join(randomCookie(24))
    cookie = "csrftoken=%s; %s=%s" % (XCSRFToken, XCSRF2Cookie, XCSRF2Token)
    post_headers = {"User-Agent": user_agent,
                        "Referer": "https://accounts.coursera.org/signin",
                        "X-Requested-With": "XMLHttpRequest",
                        "X-CSRF2-Cookie": XCSRF2Cookie,
                        "X-CSRF2-Token": XCSRF2Token,
                        "X-CSRFToken": XCSRFToken,
                        "Cookie": cookie
                        }
        
    coursera_session = requests.Session()
        
        
        
    login_res = coursera_session.post(signin_link,
                                              data=signin_info,
                                              headers=post_headers,
                                              )
        
    if login_res.status_code == 200:
        return coursera_session
    else:
        return -1
        