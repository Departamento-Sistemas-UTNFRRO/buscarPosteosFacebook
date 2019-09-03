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

import re


class FacebookStringToNumber():
    def convertStringToNumber(self, text):
        text_clean = text
        if 'persona' in text:
            m = re.search('(?<=y)\s+\d+,?\d*\s+mil', text)
            if m is None:
                m = re.search('(?<=y)\s+\d+,?\d*\s+', text)
                if m is None:
                    return text
            text_clean = m.group(0)

        if 'mill.' in text_clean:
            text_clean = text_clean.replace('mill.', '')
            text_clean = text_clean.replace('\xa0', '').replace(',', '')
            number = float(text_clean) * 1000000
            return int(number)

        if 'mil' in text_clean:
            text_clean = text_clean.replace('mil', '')
            text_clean = text_clean.replace('\xa0', '').replace(',', '')
            number = float(text_clean) * 1000
            return int(number)

        return int(float(text_clean.replace('.', '')))
