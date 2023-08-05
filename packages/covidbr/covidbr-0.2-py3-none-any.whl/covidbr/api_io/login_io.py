import os
import json
import requests
import mechanicalsoup
from requests.cookies import CookieConflictError
from ..log import log
import pandas as pd
from ..log import date_base

URL_IO_DATASET_COVID = 'https://brasil.io/dataset/covid19/caso_full/'
URL_IO_LOGIN = 'https://brasil.io/auth/login/'

COOKIES_CREDENTIALS = {"sessionid": "prd8pmk8tjvi0h360k2berid71yovrze", "csrftoken": "InjqWp5KWpzcOMpqQjQuAMpr2TYylIpGimN7fEkyueF7Oue261S5z5ETnRrSOq4i"}


path_cookies = '__cookies__'
headers = {'User-Agent':'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; GT-I9500 Build/KOT49H) AppleWebKit/537.36(KHTML, like Gecko)Version/4.0 MQQBrowser/5.0 QQ-URL-Manager Mobile Safari/537.36'}
credentials = ('','')


def save_cookies(browser,path_cookies=path_cookies):
    cookies = browser.session.cookies.get_dict()
    cookies_json = json.dumps(cookies)
    with open(path_cookies,'w') as file_cookies:
        file_cookies.write(cookies_json)


def load_cookies(browser,path_cookies=path_cookies):
    with open(path_cookies,'r') as file_cookies:
        cookies_json = file_cookies.read()
        cookies_dict = json.loads(cookies_json)
    from requests.utils import cookiejar_from_dict
    browser.session.cookies = cookiejar_from_dict(cookie_dict=cookies_dict)





class API_io:

    def __init__(self,username:str=credentials[0],password:str=credentials[1]):
        self.username = username
        self.password = password

        if(not os.path.isdir('cache')):
            os.system('mkdir cache/')
            self.path_cache = 'cache/'
        else:
            self.path_cache = 'cache/'

        self.browser = mechanicalsoup.StatefulBrowser()
        self.browser.session.headers = headers
        self.browser.session.headers.update(headers)
        log(f' configuração dos headers do browser completa! \n {self.browser.session.headers}')




    def get_data_covid_from_city(self,city_and_state:str,type:str='csv'):
        self.city,self.state = tuple(city_and_state.split())
        self.url = (f'https://brasil.io/dataset/covid19/caso_full/?state={self.state}&city={self.city}&format={type}')
        FILE_KEY_UPGRADE = f'{self.path_cache}__file_key_upgrade__'
        date_today = date_base("%d_%m_%y")
        self.file_data = f'{self.path_cache}{self.city}_{self.state}.{type}'

        if((not os.path.isfile(FILE_KEY_UPGRADE)) or (not os.path.isfile(self.file_data))):
            with open(FILE_KEY_UPGRADE,'w') as file:
                file.write(f'{date_today}')

            self.login_with_cookies_credentials(path_cookies=path_cookies)
            print('bundass')
            self.content = self.get_content_url(self.url)['content']
            self.file_data = self.save_content_in_data_cache(self.content)
            self.save_data_in_excel_cache(file_data=self.file_data)
        else:
            print('bundd')
            with open(FILE_KEY_UPGRADE,'r') as file:
                date_of_cache = file.read()
            if(date_today != date_of_cache):
                log(f'pegando o datasete da covid-19: cidade: {self.city} estado: {self.state} ')
                with open(FILE_KEY_UPGRADE,'w') as file:
                    file.write(f'{date_today}')


                self.login_with_cookies_credentials(path_cookies=path_cookies)
                self.content = self.get_content_url(self.url)['content']
                self.file_data = self.save_content_in_data_cache(self.content)
                self.save_data_in_excel_cache(file_data=self.file_data)
            else:
                with open(FILE_KEY_UPGRADE,'w') as file:
                    file.write(f'{date_today}')
                self.pd_data = pd.read_csv(self.file_data,sep=',')
                self.file_data_excel = f'{self.path_cache}{self.city}_{self.state}.xlsx'

        return self.pd_data



    def get_content_url(self,url:str):
        try:
            self.res = self.browser.get(url)
            self.size_data = round(len(self.res.content)/1024,3)
            self.res.raise_for_status()
            log(f'{self.size_data}Kbytes dados recebidos!')
            return {'content':self.res.content,'size':self.size_data}

        except(requests.exceptions.HTTPError):
            raise Exception(f'[{date_base()}] nome da cidade {self.city}-{self.state} não foi encotrada! Por favor verifique o nome e tende novamente.')



    def  save_content_in_data_cache(self,content:str,type:str='csv'):
        log('salvando dados no data...')
        file_data = f'{self.path_cache}{self.city}_{self.state}.{type}'
        with open(file_data,'wb') as file_:
            file_.write(content)
        if(os.path.isfile(file_data)):
            log(f'{file_data} salvo com sucesso!')
            return file_data
        else:
            raise(f'[{date_base()}] {file_data} não foi salvo!')



    def save_data_in_excel_cache(self,file_data):
        log('salvando agora o seu excel...')
        self.pd_data = pd.read_csv(self.file_data,sep=',')
        self.file_data_excel = f'{self.path_cache}{self.city}_{self.state}.xlsx'
        self.pd_data.to_excel(self.file_data_excel)
        if(os.path.isfile(self.file_data_excel)):
            log(f'{self.file_data_excel} salvo com sucesso!')
        else:
            raise(f'[{date_base()}] {self.file_data_excel} não foi salvo!')
        return self.file_data_excel



    def load_cookies_credentials(self,cookies_credentials):
        from requests.utils import cookiejar_from_dict
        self.browser.session.cookies = cookiejar_from_dict(cookies_credentials)



    def login_with_cookies_credentials(self,path_cookies:str):
        log('verificando a existência de cookies...')
        if(os.path.isfile(path_cookies)):
            log(f'existem cookies salvos!')
            log('Carregando os seus cookies salvos...')
            load_cookies(self.browser)
            log(f'cookies carregados no browser!')
            log('verificando aceitação da pagina do dataset \n...')
            self.res_page_dataset = self.browser.get(self.url)
            log(self.res_page_dataset.url)
            if(not 'login' in str(self.res_page_dataset.content)):
                print(self.res_page_dataset.content,2)
                print('bunda')
                log(f'Ok! logado com sucesso! \n ')
            else:
                log('login requerido')
                nome = 'reinan912'
                senha = 'imaginando912'
                self.login(username=nome,password=senha)
        else:
            log('Não existem cookies salvos!')
            log('carregando nossas credenciais!')
            self.load_cookies_credentials(COOKIES_CREDENTIALS)
            log('verificando aceitação na pagina do dataset \n...')
            self.res_page_dataset = self.browser.get(self.url)

            if('Login' in str(self.res_page_dataset.content)):
                log('Atenção! O login foi requerido!')
                self.login(username=self.username,password=self.password)

            else:
                log('Ok! logado com sucesso!')
                #log('salvando cookies')
                #save_cookies(self.browser)



    def upgrade_cache(self):
        FILE_KEY_UPGRADE = '__file_key_upgrade__'
        date_today = date_base("%d_%m_%y")
        if(not os.path.isfile(FILE_KEY_UPGRADE)):
            with open(FILE_KEY_UPGRADE,'w') as file:
                file.write(f'{date_today}')
        else:
            with open(FILE_KEY_UPGRADE,'r') as file:
                date_of_cache = file.read()
            if(date_today != date_of_cache):
                self.get_data_covid_from_city()
    
    
    
    def verify_cache(self):
        pass



    def login(self,username:str,password:str):
        log(f'promovendo a requisição do login \n username: {username}\n password: {password}\n...')
        self.browser.open(self.url)
        log(self.browser.get(self.url).text)
        self.browser.select_form()
        self.browser['username'] = username
        self.browser['password'] = password
        #self.browser.launch_browser()
        log('verificando aceitação na pagina do dataset \n...')
        self.res_page_dataset = self.browser.submit_selected()
        log(self.res_page_dataset.url)
        self.url = self.res_page_dataset.url
        if(not 'login' in self.res_page_dataset.url):
            log(f'logado com sucesso! pela requisição de login \n ')
            log('salvando cookies...')
            save_cookies(self.browser)
            log('cookies salvos!')
            
        else:
            raise Exception(f'[{date_base()}] login incorreto ou site temporariamente indisponivel!')
