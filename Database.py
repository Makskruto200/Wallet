import sqlite3 as sq
from datetime import datetime
import string
import random
def create_account(adress,phrase, password):
    try:
            with sq.connect("wallet.db") as con:
                cur=con.cursor()
                cur.execute(f"""INSERT INTO  wallets (adress,phrase, password) VALUES ("{adress}","{phrase}","{password}")""")
    except:
       pass
   

def authorization_account(phrase, password):
   try:
            with sq.connect("wallet.db") as con:
                cur=con.cursor()
                a=[i for i in cur.execute(f"SELECT * FROM wallets WHERE phrase='{phrase}'")]
                if a[0][3]==str(password):
                    return a
                else:
                    return False
   except:
             return False
             
def transactions_create(adress,adress_2,sum):
    try:
        data = datetime.now()
        with sq.connect("wallet.db") as con:
            cur=con.cursor()
            cur.execute(f"""INSERT INTO  transactions (adress,adress_2, data,sum) VALUES ("{adress}","{adress_2}","{data}","{sum}")""")
    except:
        pass
    
def transactions_select(adress):
      try:
            with sq.connect("wallet.db") as con:
                cur=con.cursor()
                a=[i for i in cur.execute(f"SELECT * FROM transactions WHERE  adress_2='{adress}' ")]
                return a
      except:
             pass
             
      

def  blockchain():
      with sq.connect("wallet.db") as con:
                  cur=con.cursor()
                  
                  a=[i for i in cur.execute(f"SELECT * FROM transactions ORDER BY id DESC LIMIT 0,10")]
                  return a
                                                             
def send_account(adress,phrase,sum):
    sum=abs(int((sum)))
    try:
                with sq.connect("wallet.db") as con:
                    cur=con.cursor()
                    a=[i for i in cur.execute(f"SELECT * FROM wallets WHERE phrase='{phrase}'")]
                    b=[i for i in cur.execute(f"SELECT * FROM wallets WHERE adress='{adress}'")]
                    transactions_create(adress,a[0][1],int(sum))
                    if int(a[0][4])>=int(sum):
                     t=int(a[0][4])-int(sum)
                     g=int(b[0][4])+int(sum)

                     cur.execute(f"""UPDATE wallets SET balance=({t}) WHERE phrase=("{phrase}")""")
                     cur.execute(f"""UPDATE wallets SET balance=({g}) WHERE adress=("{adress}")""")
                     return "Успех"
                    else:
                         return "недостаточно средст"
    except IndexError:
              return "Неправильный адрес.."
                     




def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


          
                 
                
    
def create_promo_cod(author,sum,users,adress):
    
            with sq.connect("wallet.db") as con:
                cur=con.cursor()
                cod=generate_random_string(8)
                a=[i for i in cur.execute(f"SELECT * FROM wallets WHERE adress='{adress}'")]
                if int(a[0][4])>=int(sum):
                    g=int(a[0][4])-abs(sum)
                    cur.execute(f"""UPDATE wallets SET balance=({g}) WHERE adress=("{adress}")""")
                    cur.execute(f"""INSERT INTO  promocode (author,sum,users,adress,cod) VALUES ("{author}",{abs(sum)},{abs(users)},"{adress}","{cod}")""")
    

def select_account(phrase):
    with sq.connect("wallet.db") as con:
                cur=con.cursor()
                a=[i for i in cur.execute(f"SELECT * FROM wallets WHERE phrase='{phrase}'")]
                return a

def activate_promo_cod(secret,cod):
    try:
    
                with sq.connect("wallet.db") as con:
                    cur=con.cursor()
                    promo_cod=[i for i in cur.execute(f"SELECT * FROM promocode WHERE cod='{cod}'")]
                    a=[i for i in cur.execute(f"SELECT * FROM wallets WHERE phrase='{secret}'")]
                    t=int(a[0][4])+promo_cod[0][2]//promo_cod[0][3]
                    g=promo_cod[0][2]-promo_cod[0][2]//promo_cod[0][3]
                    k=[i for i in cur.execute(f"SELECT * FROM promocode_activate WHERE cod='{cod}' AND adress='{a[0][1]}'")]
                    if k==[]:
                        cur.execute(f"""UPDATE wallets SET balance=({t}) WHERE adress=("{a[0][1]}")""")
                        cur.execute(f"""UPDATE promocode SET  sum=({g}) WHERE cod=("{cod}")""")
                        cur.execute(f"""UPDATE promocode SET  users=({promo_cod[0][3]-1}) WHERE cod=("{cod}")""")
                        cur.execute(f"""INSERT INTO  promocode_activate (adress,cod) VALUES ("{a[0][1]}","{cod}")""")
                        return "Успех"
                    else:
                        return "Вы уже активировали такой промокод"
    except IndexError:
         return "Ошибка,неправильный промокод"
        
    
def transfer(secret,sum):
     a=select_account(secret)[0]
     s=a[4]+sum
     with sq.connect("wallet.db") as con:
         cur=con.cursor()
         cur.execute(f"""UPDATE wallets SET balance=({s}) WHERE phrase=("{secret}")""")
     

    
def check(sum):
    k=0
    a=random.randint(0,51)
    if 0<=a<=20:
        k-=sum
    elif 20<a<=30:
        k=0
    elif 30<a<=40:
        k+=sum*0.5
    elif 40<a<=50:
        k+=sum
    elif a==51:
        k=sum*30
    
    return k
    

