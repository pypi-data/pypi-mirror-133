#!/usr/bin/env python3
# -*- coding: utf-8 -*-




from covidbr.plot_data.plotting import plot_media_cases
from PIL import ImageFont
from PIL import ImageDraw 
from PIL import Image
import matplotlib.pyplot as plt
from covidbr.log.logging import log
import os
import requests as rq
import covidbr as cb

#### painel covidb ####
def painel_covid(data,limit_period:int=15,path_file:str='painel.jpg',
                  path_img:str='painel_covid.jpg',show:bool=True,
                  save_cache:bool=True):
        city,state = data.city,data.state
        
        #verification of path_img or font exists#
        #or needed download from a base#
        if not os.path.isfile(path_img):
            content_img = rq.get('https://raw.githubusercontent.com/gpftc/covid_br/main/base/painel_covid.jpeg').content
            with open(path_img, 'wb') as file_img:
                file_img.write(content_img)
        if not os.path.isfile('arial_unicode.ttf'):
            content_ttf= rq.get('https://github.com/gpftc/covid_br/raw/main/base/arial_unicode.ttf').content
            with open('arial_unicode.ttf', 'wb') as file_ttf:
                file_ttf.write(content_ttf)
        else:
            pass
       
        
        
        painel_cache = 'cache_painel/'
        if save_cache:
            if not os.path.isdir(painel_cache):
                os.system(f'mkdir {painel_cache}')
        log('creating the image')
        img = Image.open(path_img).convert('RGB')
        size_image_base = img.size
        
        ## plotting the media deaths ##
        log(f"creating the image from plot media deaths from period {limit_period} day's...")
        plt = cb.plot_media_deaths(data=data, show=False,
                          color_bar='#8e43b5', color_line='black', limit_period=limit_period)
        plt.xticks([])
        #plt.grid()
        path_graph_cases = f'{painel_cache}plot_media_deaths_{data.city[:3]}.png'
        plt.savefig(path_graph_cases,dpi=200)
        img_graph = Image.open(path_graph_cases).convert('RGB')
        data.mining_statistical_data(limit_period=limit_period)
        self = data
        size = limit_period
       
        base = 220
        img_graph = img_graph.resize((base,int(base*9/16)),Image.ANTIALIAS)
        #img_graph.save('mierda.jpg')
        size_graph_x,size_graph_y = img_graph.size
        print(img_graph.size)
        base_loc = (430,360)
        img.paste(img_graph,(base_loc[0],base_loc[1]
                            ,base_loc[0]+size_graph_x
                            ,base_loc[1]+size_graph_y))
        
        ## plotting the media cases ##
        log(f"creating image from plot media cases from period of {limit_period} day's...")
        plt_media_cases = cb.plot_media_cases(data=data, show=False,
                          color_bar='#4ea286', color_line='black', limit_period=limit_period)
        #plt_media_cases.grid()
        plt_media_cases.xticks([])
        path_graph_cases = f'{painel_cache}plot_media_cases_{data.city[:3]}.png'
        plt_media_cases.savefig(path_graph_cases,dpi=200)
        img_graph = Image.open(path_graph_cases).convert('RGB')
        data.mining_statistical_data(limit_period=limit_period)
       
        base = 220
        img_graph = img_graph.resize((base,int(base*9/16)),Image.ANTIALIAS)
        #img_graph.save('mierda2.jpg')
        size_graph_x,size_graph_y = img_graph.size
        print(img_graph.size)
        base_loc = (35,360)
        img.paste(img_graph,(base_loc[0],base_loc[1]
                            ,base_loc[0]+size_graph_x
                            ,base_loc[1]+size_graph_y))
        
        ## plotting the media from total cases ##
        log(f"creating image from plot from the all cases data...")
        plt_media_cases_total = cb.plot_media_cases(data=data, show=False,
                          color_bar='#4ea286', color_line='black')
        #plt_media_cases_total.grid()
        #plt_media_cases_total.xticks([])
        plt_media_cases_total.title('Média Móvel Total de Casos',weight='bold')
        path_graph_cases = f'{painel_cache}plot_media_cases_total_{data.city[:3]}.png'
        plt_media_cases_total.savefig(path_graph_cases,dpi=200)
        img_graph = Image.open(path_graph_cases).convert('RGB')
        data.mining_statistical_data(limit_period=limit_period)
        
        base = 250
        img_graph = img_graph.resize((base,int(base*9/16)),Image.ANTIALIAS)
        #img_graph.save('mierda2.jpg')
        size_graph_x,size_graph_y = img_graph.size
        print(img_graph.size)
        base_loc = (360,100)
        img.paste(img_graph,(base_loc[0],base_loc[1]
                            ,base_loc[0]+size_graph_x
                            ,base_loc[1]+size_graph_y))
        
        ## plotting the media from deaths total ##
        log(f"creating a image from plot from the all deaths data...")
        plt_media_deaths_total = cb.plot_media_deaths(data=data, show=False,
                          color_bar='#8e43b5', color_line='black')
        plt_media_deaths_total.title(f'Média Móvel Total de Mortes',weight='bold')
        #plt_media_cases_total.grid()
        #plt_media_deaths_total.xticks([])
        path_graph_deaths = f'{painel_cache}plot_media_deaths_total_{data.city[:3]}.png'
        plt_media_deaths_total.savefig(path_graph_deaths,dpi=200)
        img_graph = Image.open(path_graph_deaths).convert('RGB')
        data.mining_statistical_data(limit_period=limit_period)
        base = 250
        img_graph = img_graph.resize((base,int(base*9/16)),Image.ANTIALIAS)
        #img_graph.save('mierda2.jpg')
        size_graph_x,size_graph_y = img_graph.size
        print(img_graph.size)
        base_loc = (600,100)
        img.paste(img_graph,(base_loc[0],base_loc[1]
                            ,base_loc[0]+size_graph_x
                            ,base_loc[1]+size_graph_y))

        ######################################################
        #### downloading tha background painel covid base ####
        #data.mining_statistical_data(limit_period=limit_period)
        if not os.path.isfile(path_img):
            log(f'path {path_img} not found! downlading a image base.')
            url_image = 'https://raw.githubusercontent.com/gpftc/covid_br/main/painel_covid.png'
            content_img = rq.get(url_image,stream=True).content
            with open(path_img,'wb') as img_file:
                img_file.write(content_img)

        
        ###############################################
        ### Starting the creation from Painel Image ###
        ###############################################
        draw = ImageDraw.Draw(img)
        ## adding date update in the image ##
        log("writing the data update...")
        font = ImageFont.truetype("arial_unicode.ttf",18)
        draw.text((150,150),self.date[-1],'#8b9bae',font=font)
        ## adding the name city ##
        log("writing the name city...")
        font = ImageFont.truetype("arial_unicode.ttf",18)
        draw.text((35,200),f'Cidade: {self.city} {self.state}','#8b9bae',font)
        
        ############################################
        ### creating the painel from deaths data ###
        log("writing the number of all deaths...")
        font = ImageFont.truetype("arial_unicode.ttf", 40)
        draw.text((460, 320),self.all_deaths_string,'#8e43b5',font=font)
        ## 24h ##
        log("writing the number of deaths on 24h ago...")
        font = ImageFont.truetype("arial_unicode.ttf", 20)
        draw.text((700, 245),' 24h','#8e43b5',font=font)
        font = ImageFont.truetype("arial_unicode.ttf", 35)
        draw.text((700, 265),f' {self.mortes_diarias[-2]}','#8e43b5',font=font)
        ## from period days ##
        log(f"writing the number of deaths from {size} day's ago...")
        font = ImageFont.truetype("arial_unicode.ttf", 20)
        draw.text((700, 320),f'{size} dias','#8e43b5',font=font)
        font = ImageFont.truetype("arial_unicode.ttf", 35)
        sum_deaths_period = list(f'{sum(self.mortes_diarias[-size:])}')
        if len(sum_deaths_period) >= 4:
            sum_deaths_period.insert(-3,'.')
        #sum_deaths
        sum_deaths_period=''.join(sum_deaths_period)
        draw.text((700, 340),f' {sum_deaths_period}','#8e43b5',font=font)
        ## percent variation ##
        log(f"writing the change of deaths on this period of {size} day's...")
        font = ImageFont.truetype("arial_unicode.ttf", 20)
        #font=ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Arial.ttf', 16)
        draw.text((680, 400),'variância móvel','#8e43b5',font=font)
        font = ImageFont.truetype("arial_unicode.ttf", 35)
        draw.text((690, 420),f'{self.percent_deaths}%','#8e43b5',font=font)
        
        ###########################################
        ### creating the painel image for cases ###
        log("writing the number of cases confirmeds...")
        font = ImageFont.truetype("arial_unicode.ttf", 40)
        draw.text((60, 320),self.all_cases_string,'#4ea286',font=font)
        ## 24h ##
        log("writing the number of cases confirmed on 24h ago...")
        font = ImageFont.truetype("arial_unicode.ttf", 20)
        draw.text((290, 245),' 24h','#4ea286',font=font)
        font = ImageFont.truetype("arial_unicode.ttf", 35)
        draw.text((290, 265),f'{self.casos_diarios[-2]}','#4ea286',font=font)
        ## 15 days ##
        log(f"writing the number of cases confirmed on {limit_period} day's ago...")
        font = ImageFont.truetype("arial_unicode.ttf", 20)
        draw.text((290, 320),f' {size} dias','#4ea286',font=font)
        font = ImageFont.truetype("arial_unicode.ttf", 35)
        sum_cases_period = list(f'{sum(self.casos_diarios[-size:])}')
        if len(sum_cases_period) >= 4:
            sum_cases_period.insert(-3,'.')
        sum_cases_period=''.join(sum_cases_period)
        draw.text((290, 340),sum_cases_period,'#4ea286',font=font)
        ## percent variation ##
        log(f"writing the variation percent of the cases number on {limit_period} day's ago...")
        font = ImageFont.truetype("arial_unicode.ttf", 20)
        #font=ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Arial.ttf', 16)
        draw.text((260, 400),'variância móvel','#4ea286',font=font)
        font = ImageFont.truetype("arial_unicode.ttf", 35)
        draw.text((290, 420),f'{self.percent_cases}%','#4ea286',font=font)

        plt.cla()
        plt.clf()
        
        ###### show the painel #######
        if show:
            img.show()
        ##############################
        #### saving painel image #####
        ##############################
        if path_file == 'painel.jpg':
            log(f"saving painel as '{city}{state}_{path_file}'")
            img.save(f'{city}{state}_{path_file}')
        log("painel saved!")
        return f'''
                    "date_update": {self.date[-1]},
                    "all_confirmeds": {self.casos[-1]},
                    "all_deaths": {self.mortes[-1]},
                    "variation_deaths_movel": {self.percent_deaths},
                    "percent_variation_death": {self.percent_all_deaths},
                    "variation_cases_movel": {self.percent_cases},
                    ""
                '''
