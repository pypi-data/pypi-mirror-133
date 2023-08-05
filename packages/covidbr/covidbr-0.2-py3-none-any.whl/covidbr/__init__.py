#!/usr/bin/env python3
# -*- coding: utf-8 -*-

########################
## author: Reinan Br. ##
## init: 25/06/2021   ##
## project: API_covid ##
########################

from covidbr.log import logging
from covidbr.api_io import get_data_covid,login_io
from covidbr.get_data import data_from_city
from covidbr.plot_data.plotting import plot_media_cases
from covidbr.plot_data.plotting import plot_media_deaths
from covidbr.plot_data.painel import painel_covid
from covidbr.log.logging import show_console as show_logs
from covidbr.log.logging import log


all = [data_from_city,
       login_io,logging,
       get_data_covid,
       plot_media_cases,
       plot_media_deaths,
       painel_covid,
       show_logs,log
]