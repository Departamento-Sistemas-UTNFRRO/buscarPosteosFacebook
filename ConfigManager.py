# -*- coding: utf-8 -*-

#    This file is part of buscarPostFacebook.
#
#    buscarPostFacebook is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    buscarPostFacebook is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with buscarPostFacebook; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import logging
import json
import os
from datetime import datetime
logger = logging.getLogger(__name__)


class ConfigManager():
    def __init__(self):
        self.fb_username = None
        self.fb_password = None
        self.fb_avcode = None
        self.fb_page_name = None
        self.fb_search_year = None
        self.fb_search_month = None
        self.base_path = None
        self.input_filename = None
        self.output_filename = None
        self.output_post_filename_prefix = None
        self.max_scroll = None
        self.shares_per_page = None
        self.gecko_binary = None
        self.gecko_driver_exe = None
        self.gecko_headless = None
        self.loadConfigData()

    def loadConfigData(self):
        logger.info("Loading Config Options")
        with open('config.json', 'r') as config_file:
            filecontents = json.load(config_file)
            fbSection = filecontents['facebook'][0]
            self.fb_username = fbSection['user']
            self.fb_password = fbSection['password']
            self.fb_avcode = fbSection['avcode']
            self.max_scroll = fbSection['max_scroll']
            self.fb_page_name = fbSection['page_name']
            self.fb_search_year = int(fbSection['search_year'])
            self.fb_search_month = int(fbSection['search_month'])
            self.shares_per_page = fbSection['shares_per_page']

            fsWebDriver = filecontents['WebDriver'][0]
            self.gecko_binary = fsWebDriver['gecko_binary']
            self.gecko_driver_exe = fsWebDriver['gecko_driver_exe']
            self.gecko_headless = fsWebDriver['gecko_headless']

            fsSection = filecontents['FileStorageConfig'][0]
            self.base_path = fsSection['base_path']
            input_filename_prefix = fsSection['input_filename']
            self.input_filename = os.path.join(self.base_path, input_filename_prefix)
            output_filename_prefix = fsSection['output_filename']
            current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = output_filename_prefix + "_" + current_date + ".csv"
            self.output_filename = os.path.join(self.base_path, filename)
            self.output_post_filename_prefix = fsSection['output_post_filename']
