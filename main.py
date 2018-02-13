import requests
from bs4 import BeautifulSoup as bs
import random
import names
import time
from time import sleep
from random import *
import os
import json
import string
from utils import c_logging, n_logging

with open("config.json") as file:
    config = json.load(file)
    file.close()

with open("addconfig.json") as file:
    aconfig = json.load(file)
    file.close()

genrandphone = aconfig['genrandomphone']
phonenum = aconfig['phonenum']
addline1 = aconfig['addressline1']
statecode = aconfig['StateCode']
zipcode = aconfig['ZipCode']
city = aconfig['City']

lognum = randint(111, 999999)
lognum = str(lognum)
logfile = "logs/LOG{}.txt".format(lognum)
f = open(logfile, "w+")
f.close()

emailjig = config['emailjig']
gmailadd = config['gmailadd']
domain = config['domain']
randomname = config['randomname']
name = config['name']
randominsta = config['randominsta']
useproxies = config['useproxies']
gender = config['gender']
insta = config['insta']
num = config['num']
passw = config['password']

def main():
    count = 0
    scount = 0
    for i in range(int(num)):
        count = count + 1
        if useproxies == "true":
            def random_line(fname):
                lines = open(fname).read().splitlines()
                return choice(lines)
            proxy = random_line('proxies.txt')
            try:
                proxytest = proxy.split(":")[2]
                userpass = True
            except IndexError:
                userpass = False
            if userpass == True:
                ip = proxy.split(":")[0]
                port = proxy.split(":")[1]
                userpassproxy = ip + ":" + port
                proxyuser = proxy.split(":")[2].rstrip()
                proxypass = proxy.split(":")[3].rstrip()
            if userpass == True:
                proxies = {'http': 'http://' + proxyuser + ':' + proxypass + '@' + userpassproxy, 'https': 'http://' + proxyuser + ':' + proxypass + '@' + userpassproxy}
            if userpass == False:
                proxies = {'http': 'http://' + proxy, 'https': 'http://' + proxy}


        if emailjig == "gmail":
            prefix = names.get_first_name()
            prefixp2 = randint(111, 9999)
            prefixp2 = str(prefixp2)
            fullprefix = prefix + prefixp2
            realemail = gmailadd.split("@")[0]
            email = "{}+{}@gmail.com".format(realemail, fullprefix)
        else:
            prefix = names.get_first_name()
            prefixp2 = radnint(111, 9999)
            prefixp2 = str(prefixp2)
            fullprefix = prefix + prefixp2
            email = "{}@{}".format(fullprefix, domain)


        if randomname == "true":
            if gender == "male":
                firstname = names.get_first_name(gender="male")
            else:
                firstname = names.get_first_name(gender="female")
            lastname = names.get_last_name()
        else:
            firstname = name.split(" ")[0]
            lastname = name.split(" ")[1]

        if randominsta == "true":
            instapart1 = names.get_first_name()
            instapart2 = names.get_last_name()
            instapart3 = randint(111, 9999)
            instapart3 = str(instapart3)
            instaname = "{}.{}{}".format(instapart1, instapart2, instapart3)
        else:
            instaname = config['insta']
        n_logging("==============================================")
        c_logging("Starting Task {}/{}".format(count, num), "cyan")
        if useproxies == "true":
            c_logging("Using Proxy {}".format(proxy), "yellow")

        regheaders = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.9',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'footdistrict.com',
            'Origin':'https://footdistrict.com',
            'Referer':'https://footdistrict.com/en/customer/account/create/',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
        }

        s = requests.session()
        if useproxies == "true":
            a = s.post("https://footdistrict.com/en/customer/account/create/", headers=regheaders, proxies=proxies)
        else:
            a = s.post("https://footdistrict.com/en/customer/account/create/", headers=regheaders)

        soup0 = bs(a.text, "html.parser")
        formkey1 = soup0.find('input', {'name':'form_key'})['value']

        regpayload = {
            'success_url':'',
            'error_url':'',
            'form_key':formkey1,
            'firstname':firstname,
            'lastname':lastname,
            'email':email,
            'password':passw,
            'confirmation':passw
        }

        if useproxies == "true":
            b = s.post("https://footdistrict.com/en/customer/account/createpost/", data=regpayload, headers=regheaders, proxies=proxies)
        else:
            b = s.post("https://footdistrict.com/en/customer/account/createpost/", data=regpayload, headers=regheaders)

        if "Thank you for registering with foot District." in b.text:
            c_logging("Created Account", "green")
        else:
            c_logging("Error Creating Account", "red")
            n_logging("==============================================")
            print("")
            continue

        addheaders1 = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',''
            'Accept-Language':'en-US,en;q=0.9',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'footdistrict.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
        }

        #add address
        if useproxies == "true":
            c = s.post("https://footdistrict.com/en/customer/address/new/", headers=addheaders1, proxies=proxies)
        else:
            c = s.post("https://footdistrict.com/en/customer/address/new/", headers=addheaders1)

        addheaders2 = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.9',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'footdistrict.com',
            'Origin':'https://footdistrict.com',
            'Referer':'https://footdistrict.com/en/customer/address/new/',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
        }

        soup1 = bs(c.text, "html.parser")
        formkey2 = soup1.find('input', {'name':'form_key'})['value']

        if genrandphone == "true":
            pnum = randint(1111111111, 9999999999)
        else:
            pnum = phonenum
        addpay = {
            'form_key':formkey2,
            'success_url':'',
            'error_url':'',
            'firstname':firstname,
            'lastname':lastname,
            'telephone':pnum,
            'street[]':addline1,
            'city':city,
            'region_id':statecode,
            'region':'',
            'postcode':zipcode,
            'country_id':'US',
            'default_billing':'1',
            'default_shipping':'1'
        }

        if useproxies == "true":
            d = s.post("https://footdistrict.com/en/customer/address/formPost/", headers=addheaders2, data=addpay, proxies=proxies)
        else:
            d = s.post("https://footdistrict.com/en/customer/address/formPost/", headers=addheaders2, data=addpay)

        if "The address has been saved." in d.text:
            c_logging("Added Address Into Account", "green")
        else:
            c_logging("Error Adding Address Into Account", "red")
            n_logging("==============================================")
            print("")
            continue


        sizelist = ['7 US - 40 EU', '7.5 US - 40.5 EU', '8 US - 41 EU', '8.5 US - 42 EU', '9 US - 42.5 EU', '9.5 US - 43 EU', '10 US - 44 EU', '10.5 US - 44.5 EU', '11 US - 45 EU', '11.5 US - 45.5 EU', '12 US - 46 EU', '12.5 US - 47 EU', '13 US - 47.5 EU']
        sizenum = randint(0, len(sizelist) - 1)
        size = sizelist[sizenum]

        enterheaders = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.9',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'footdistrict.typeform.com',
            'Origin':'https://footdistrict.typeform.com',
            'Referer':'https://footdistrict.typeform.com/to/EMg8ts',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }

        enterpay = {
            'form[language]':'en',
            'form[textfield:kX7xgn6R3OSw]':instaname,
            'form[list:JFrgN8tk6o3V][choices]':'English',
            'form[list:JFrgN8tk6o3V][other]':'',
            'form[textfield:xMF5nPz41QJn]':'{} {}'.format(firstname, lastname),
            'form[email:mGswtWzGMmma]':email,
            'form[dropdown:I29KaKm566yp]':size,
            'form[landed_at]':int(time.time()),
            'form[token]':'e9c01c3389f973d829960b97c0d839e1$2y$11$e2dJZC0zIXZQK1pxbSZbL.GlvrtkB8Cog6cLRHUvnLHLyhLEKzIda'
        }

        if useproxies == "true":
            e = s.post("https://footdistrict.typeform.com/app/form/submit/EMg8ts", headers=enterheaders, data=enterpay, proxies=proxies)
        else:
            e = s.post("https://footdistrict.typeform.com/app/form/submit/EMg8ts", headers=enterheaders, data=enterpay)

        if "success" in e.text:
            scount = scount + 1
            c_logging("Successfully Entered {}/{} SuccessCount: {}".format(count, num, scount), "green")
            f = open(logfile, "a+")
            f.write("{} | {} {} | {} | {}\n".format(email, firstname, lastname, pnum, size))
            n_logging("==============================================")
            print("")
        else:
            c_logging("Failed Entering {}/{}".format(count, num), "red")
            n_logging("==============================================")
            print("")
    c_logging("Finished Entering Into Raffle", "green")
    c_logging("Successfully Entered {}/{}".format(scount, num), "green")
    c_logging("By XO", "cyan")

if __name__ == '__main__':
    c_logging("footdistrict freethrow line raffle", "cyan")
    c_logging("By XO", "magenta")
    print("")
    main()
