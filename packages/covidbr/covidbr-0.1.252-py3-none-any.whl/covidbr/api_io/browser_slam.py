import json
import requests
import mechanicalsoup
import requests as rq
import mechanicalsoup as ms
from requests.cookies import CookieConflictError
from requests.models import stream_decode_response_unicode
from covidbr.log import log
import os
br = mechanicalsoup.StatefulBrowser()


def save_cookies(browser:br,path_cookies:str) -> str:
    cookies = browser.session.cookies.get_dict()
    cookies_json = json.dumps(cookies)
    with open(path_cookies,'w') as file_cookies:
        file_cookies.write(cookies_json)


def load_cookies(browser:br,path_cookies:str) -> str:
    with open(path_cookies,'r') as file_cookies:
        cookies_json = file_cookies.read()
        cookies_dict = json.loads(cookies_json)
    from requests.utils import cookiejar_from_dict
    browser.session.cookies = cookiejar_from_dict(cookie_dict=cookies_dict)



def bar_percent(percent:int,use_percent_screen_size=50) -> str:
        use_percent_screen = use_percent_screen_size/100
        columns_terminal = int(os.get_terminal_size().columns*use_percent_screen)
        # total_percent_columns = columns/100
        size_real = round(columns_terminal*percent/100)
        bar_complet = '.'*size_real
        painel_percent = f'[{bar_complet:<{int(columns_terminal)}}]'
        #print(painel_percent)
        return painel_percent


userAgent = 'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; GT-I9500 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.0 QQ-URL-Manager Mobile Safari/537.36'
br.session.headers = {"User-Agent":userAgent} #
br.session.headers.update({"User-Agent":userAgent }) 
            
def download(url:str,path_file:str=None,browser:br=None) -> str:
    if path_file:
        pass
    else:
        path_file = url.split('/')[-1]
    print(f'name file: {path_file}')
    if browser:
        pass
    else:
        from browser_slam import br 
        browser = br
    if os.path.isfile(path_file):
        os.system(f'rm {path_file}')
    res = requests.get(url,stream=True)
    res.raise_for_status()
    size_file = float(res.headers.get('content-length'))
    print('loading download...')
    count = 0
    with open('only_'+path_file,'wb') as file_append:
        content_bytes = res.iter_content(chunk_size=1024)
        size_file_mb = size_file/(1024**2)
        for bytes in content_bytes:
            count += len(bytes)
            percent_complet = (count/size_file)*100
            count_mb = count/(1024**2)
            percent_complet = f'{percent_complet:.2f}'
            percent = float(percent_complet)
            sp = ' '
            painel_print = f'[{path_file}] [{count_mb:.2f}mb/{size_file_mb:.2f}mb]  [ {percent_complet}%]'
            use_percent_screen = .5
            columns_terminal = int(os.get_terminal_size().columns*use_percent_screen) - len(painel_print)
            # total_percent_columns = columns/100
            size_real = round(columns_terminal*percent/100)
            white = '\033[47m \033[0m'
            bar_complet = '.'*size_real
            painel_percent = f'[{bar_complet:<{int(columns_terminal)}}]'
            painel_print = f'[{path_file}] [{count_mb:.2f}mb/{size_file_mb:.2f}mb] {painel_percent} [ {percent_complet}%]'
            
            print(f'{painel_print}')
            file_append.write(bytes)
            
            