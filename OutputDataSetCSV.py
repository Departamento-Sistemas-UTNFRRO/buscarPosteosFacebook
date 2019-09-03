# -*- coding: utf-8 -*-

#    This file is part of buscarTitulosFacebook.
#
#    buscarTitulosFacebook is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    buscarTitulosFacebook is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with buscarTitulosFacebook; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import pandas as pd
import csv


class OuputDataSetCSV(object):
    def __init__(self, outputFileName, columns):
        self.outputFileName = outputFileName
        self.columns = columns
        self.dataset = []

    def append(self, newrow):
        self.dataset.append(newrow)

    def save(self):
        df = pd.DataFrame(data=self.dataset, columns=self.columns)
        df.to_csv(self.outputFileName, index=False, columns=self.columns, sep=';', quoting=csv.QUOTE_ALL, doublequote=True, quotechar='"', encoding="utf-8")    
