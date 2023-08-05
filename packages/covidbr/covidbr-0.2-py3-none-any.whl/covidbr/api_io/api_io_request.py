#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########################
## author: Reinan Br. ##
## date: 25/06/2021   ##
########################

##importando bibliotecas##
#from sys import ps1
from mechanicalsoup import browser
import requests
from .browser_slam import load_cookies, save_cookies
import os
import pandas as pd
from covidbr.log import date_base
import mechanicalsoup
from covidbr.log import log
from bs4 import BeautifulSoup as bs

br = mechanicalsoup.StatefulBrowser()

#####  coverting ctime from file in the datetime
def get_modify_day_file(path:str):
    import datetime as dt 
    import os
    time_file = dt.datetime.fromtimestamp(os.path.getmtime(path))
    return time_file




userAgent = 'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; GT-I9500 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.0 QQ-URL-Manager Mobile Safari/537.36'
path_cache_dir = '.cache/'

def verify_date_upload() -> str:
    html_source = requests.get('https://brasil.io/dataset/covid19/caso_full/').text
    soup_html_io = bs(html_source,'html.parser')
    date_upload = soup_html_io.find_all('p')[-1].text
    log(date_upload)
    path_verify = path_cache_dir+'date_update_verification'
    if os.path.isfile(path_verify):
        with open(path_verify,'r') as file_:
            date_upload_file = file_.read()
        if date_upload_file == date_upload:
            log('this cache is actually!')
            return {'date_upload':date_upload,'update':True}
        else:
            log('this cache is not actually! requirement of update for content!')
            with open(path_verify,'w') as file:
                file.write(date_upload)
            return {'date_upload':date_upload,'update':False}
    else:
        log('file of update verification not exist! initializing...')
        with open(path_verify,'w') as file:
                file.write(date_upload)
        return {'date_upload':date_upload,'update':False}

    

def login_io(user:str,password:str,path_cookies:str='.cookies'):
    br = mechanicalsoup.StatefulBrowser()
    br.session.headers = {"User-Agent":userAgent} #
    br.session.headers.update({"User-Agent":userAgent })

    url_login_io = 'https://brasil.io/auth/login/'
    log('opening site of login io...')
    br.open(url_login_io)
    #log(f'sendding login [name:{user}, password: {password}] to site...')
    br.select_form()
    br['username'] = user
    br['password'] = password
    #br.launch_browser()
    log('Sendded login!')
    res = br.submit_selected()
    if not ('tente novamente' in str(res.content)):
        log('Login accept!')
        save_cookies(browser=br,path_cookies=path_cookies)
        return br
    else:
        log("Incorrect login!")
        raise Exception(f'login required is incorrect or blocked')


def get_data_covid(city:str,state:str) -> str:
    city = city.split('_')
    br = mechanicalsoup.StatefulBrowser()
    if len(city)>=1:
        city=('+').join(city)
        url = f'https://brasil.io/dataset/covid19/caso_full/?search={city}&state={state}&format=csv'
    else:
        city=('').join(city)
        url = (f'https://brasil.io/dataset/covid19/caso_full/?state={state}&city={city}&format=csv')

    path_cookies = path_cache_dir+'/cookies_change'
    if (os.path.isfile(path_cookies)):
        load_cookies(browser=br,path_cookies=path_cookies)
    else:
        if os.path.isdir('.cache'):
            pass
        else:
            os.system('mkdir .cache')
    vf =  verify_date_upload()
    city = '+'.join(city.split('_'))
    city = city.lower()
    state = state.upper()
    file_content = path_cache_dir+f'file_content_{city}_{state}'
    if vf['update']:
        log('fileDateUpdate is update!')
        if os.path.isfile(file_content):
            date_file_content = get_modify_day_file(file_content)
            date_file_upload = get_modify_day_file(path_cache_dir+'date_update_verification')
            log('filesUpload and filesContent is update!' if (date_file_content==date_file_upload) else 'filesUpload and filesContent is update!')

            if(date_file_content==date_file_upload):
                with open(file_content,'rb') as file_b:
                    content_data = file_b.read()
                return {'content_data':content_data,'date_upload':vf['date_upload']}
            else:
                log(f'file content from city {city} is not update')
                br.session.headers = {"User-Agent":userAgent} #
                br.session.headers.update({"User-Agent":userAgent })
                log('opening dataset site...')
                res = br.get(url)
                res.raise_for_status()
                if not ("entrar" in str(res.content)):
                    with open(file_content,'wb') as file_b:
                        file_b.write(res.content)
                    return {'content_data':res.content,'date_upload':vf['date_upload']}
                else:
                    log('login required!')
                    br = login_io(user='reinan912',password='imaginando912',path_cookies=path_cookies)
                    res = br.get(url)
                    res.raise_for_status()
                    log('ok!')
                    return {'content_data':res.content,'date_upload':vf['date_upload']}

        else:
            log(f'file content from city {city} dont exists, getting...')
            log('configurate of headers')
            br.session.headers = {"User-Agent":userAgent} #
            br.session.headers.update({"User-Agent":userAgent })
            log('opening dataset site...')
            res = br.get(url)
            res.raise_for_status()
            if not ("entrar" in str(res.content)):
                with open(file_content,'wb') as file_b:
                    file_b.write(res.content)
                return {'content_data':res.content,'date_upload':vf['date_upload']}
            else:
                log('login required!')
                br = login_io(user='reinan912',password='imaginando912',path_cookies=path_cookies)
                res = br.get(url)
                res.raise_for_status()
                log('ok!')
                return {'content_data':res.content,'date_upload':vf['date_upload']}
    else:
        log('configurate of headers')
        br.session.headers = {"User-Agent":userAgent} #
        br.session.headers.update({"User-Agent":userAgent })
        log('opening dataset site...')
        res = br.get(url)
        res.raise_for_status()
        if not ("entrar" in str(res.content)):
            with open(file_content,'wb') as file_b:
                file_b.write(res.content)
            return {'content_data':res.content,'date_upload':vf['date_upload']}
        else:
            log('login required!')
            br = login_io(user='reinan912',password='imaginando912',path_cookies=path_cookies)
            res = br.get(url)
            res.raise_for_status()
            log('ok!')
            return {'content_data':res.content,'date_upload':vf['date_upload']}


