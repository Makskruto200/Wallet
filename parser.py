import requests
from bs4 import BeautifulSoup 
import re
import random
import string

def phrase():
      ren=requests.get("https://studynow.ru/dicta/allwords")
      soup=BeautifulSoup(ren.text,"lxml")
      k=soup.find_all("td",class_="")
      j=[i.text for i in k]
      r = re.compile("[a-zA-Z]+")
      russian = [w for w in filter(r.match,j)]
      
      h=""
      for i in range(15):
          h+=russian[random.randint(0,len(russian)-1)]+" "
      return h

def address():
    length=40
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    return rand_string
    


      
      
      
