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


class InputDataSetCSV(object):
    def __init__(self, inputFilename, init=None, end=None):
        self.inputFilename = inputFilename
        self.dataset = self._obtenerDataSet()
        self.init = init
        if init is None:
            self.init = 0
        self.end = end
        if end is None:
            self.end = len(self.dataset)

    def _obtenerDataSet(self):
        csv_file = pd.read_csv(self.inputFilename, header=0, sep=',', quotechar='\"', encoding="utf-8")
        return csv_file.values.tolist()