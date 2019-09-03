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

import urllib.request
import bs4
import os
from time import sleep
from datetime import datetime, timedelta
from FacebookStringToNumber import FacebookStringToNumber
from TextOutputFile import TextOutputFile
from selenium.webdriver.common.keys import Keys


class PostFacebook():
    def __init__(self, urlLink, fb_login, html_preview):
        self.urlLink = urlLink
        self.fb_login = fb_login
        self.html_preview = html_preview
        self.html_preview_bs = self._getHtmlPost(html_preview)
        self.html_raw = self._getHtmlFacebook()
        self.html_bs = self._getHtmlPost(self.html_raw)
        self.fbStringToNumber = FacebookStringToNumber()

    def _getHtmlFacebook(self):
        url = self.urlLink.replace('videos', 'posts')
        self.fb_login.get(url)
        sleep(5)
        
        body = self.fb_login.find_element_by_xpath('//body')
        body.send_keys(Keys.ESCAPE)
        sleep(1)

        try:
            post = self.fb_login.find_element_by_css_selector('._5pcr.userContentWrapper')
            html = post.get_attribute("innerHTML")
        except Exception as ex:
            try:
                post = self.fb_login.find_element_by_css_selector('._wyj._20nr')
                html = post.get_attribute("innerHTML")
            except Exception as ex:
                try:
                    post = self.fb_login.find_element_by_css_selector('._5-g_._3qw')
                    html = post.get_attribute("innerHTML")
                except Exception as ex:
                    print("ERROR" + str(ex))
        return html

    def _getHtmlPost(self, html_raw):
        contenido = None
        if html_raw:
            contenido = bs4.BeautifulSoup(html_raw, 'lxml')
        return contenido

    def SaveHtml(self, base_path):
        post_id, page_id = self.getPostID()
        text_output_file = TextOutputFile(str(self.html_raw))
        text_output_filename = "post_page_" + page_id + "_" + post_id + ".html"
        output_filename_html = os.path.join(base_path, text_output_filename)
        text_output_file.save(output_filename_html)

    def ParsePostHTML(self):
        posts = []

        page_name = self.getPageName()
        if page_name is None:
            print('post skip')
            return posts

        posts.append('')  # type

        posts.append(page_name)

        post_id, page_id = self.getPostID()
        posts.append("post_page_" + page_id)
        posts.append(page_id + "_" + post_id)
        posts.append(self.getPostURL(page_id, post_id))

        # post_message
        posts.append(self.getPostMessage())

        # picture
        posts.append(self.getPicture())

        # full_picture
        full_picture, post_picture_descripcion = self.getFullPicture()
        posts.append(full_picture)

        link = ''
        link_domain = ''
        poll_count = 0
        link_div = self.html_bs.find_all('div', {'class': '_6ks'})
        if link_div:
            a_link_tag = link_div[0].find_all('a')
            a_link_href = a_link_tag[0].get('href')
            a_link_url_query = urllib.parse.urlsplit(a_link_href).query
            link_dict = urllib.parse.parse_qs(a_link_url_query)
            link = link_dict.get('u', [''])[0]
            # link_domain
            link_domain_div = self.html_bs.find_all('div', {'class': '_6lz _6mb _1t62 ellipsis'})
            if link_domain_div:
                link_domain = link_domain_div[0].getText()
            posts[0] = 'link'
        else:
            link_video = self.html_bs.select('video[src]')
            if link_video:
                a_link_href = self.getVideoLink(link_video)
                link_domain = 'facebook.com'
                posts[0] = 'video'
            else:
                link_imagen_tag = self.html_bs.find_all('a', {'class': '_4-eo _2t9n _50z9'})
                if link_imagen_tag:
                    a_link_href = link_imagen_tag[0].get('href')
                    link = "https://www.facebook.com" + a_link_href
                    link_domain = 'facebook.com'
                    posts[0] = 'imagen'
                else:
                    link_imagen_tag = self.html_bs.find_all('a', {'class': '_6k_ _4-eo _5dec _1ktf'})
                    if link_imagen_tag:
                        a_link_href = link_imagen_tag[0].get('href')
                        link = "https://www.facebook.com" + a_link_href
                        link_domain = 'facebook.com'
                        posts[0] = 'imagen'
                    else:
                        link_imagen_tag = self.html_bs.find_all('a', {'class': '_4-eo _2t9n'})
                        if link_imagen_tag:
                            a_link_href = link_imagen_tag[0].get('href')
                            link = "https://www.facebook.com" + a_link_href
                            link_domain = 'facebook.com'
                            posts[0] = 'imagen'
                        else:
                            cabecera_span_tag = self.html_bs.find_all('span', {'class': 'fcg'})
                            for span in cabecera_span_tag:
                                if 'encuesta' in str(span):
                                    posts[0] = 'encuesta'
                                    poll_tag = self.html_bs.find_all('div', {'class': '_204q'})
                                    if poll_tag:
                                        poll_count_text = poll_tag[0].getText().replace('votos', '')
                                        poll_count = self.fbStringToNumber.convertStringToNumber(poll_count_text)                    
                                    break

        posts.append(link)
        posts.append(link_domain)

        # post_published
        post_published_str, post_published_unix, post_published_sql, post_date_argentina = self.getPostDate(self.html_preview_bs)
        posts.append(post_published_str) 
        posts.append(post_published_unix)
        posts.append(post_published_sql)
        posts.append(post_date_argentina)

        like_count_fb, rea_LOVE, rea_WOW, rea_HAHA, rea_SAD, rea_ANGRY = self.getReactions(self.fbStringToNumber)

        posts.append(like_count_fb)

        # comments_count_fb
        comments_count = self.getCommentsCount(self.fbStringToNumber)
        posts.append(comments_count)

        # reactions_count_fb
        reactions_count = self.getReactionsCount(self.fbStringToNumber)
        posts.append(reactions_count)

        # shares_count_fb
        shares_count = self.getSharesCount(self.fbStringToNumber)
        posts.append(shares_count)

        # engagement_fb
        try:
            posts.append(comments_count + reactions_count + shares_count)
        except Exception:
            posts.append('')

        posts.append(like_count_fb)
        posts.append(rea_LOVE)
        posts.append(rea_WOW)
        posts.append(rea_HAHA)
        posts.append(rea_SAD)
        posts.append(rea_ANGRY)

        posts.append(post_picture_descripcion)
        posts.append(poll_count)

        titulo = self.getTituloLink()
        subtitulo_post = self.getSubtituloLink()

        posts.append(titulo)
        posts.append(subtitulo_post)

        mencionesLista, hashtagsLista = self.getMencionesHashtags()
        posts.append(mencionesLista)
        posts.append(hashtagsLista)

        video_plays_count = self.getVideosPlaysCount(self.fbStringToNumber)
        posts.append(video_plays_count)

        fb_action_tags_text = self.getFBActionTagsText()
        posts.append(fb_action_tags_text)

        has_emoji = self.getHasEmoji()
        posts.append(has_emoji)

        tiene_hashtags = self.getTieneHashtags(hashtagsLista)

        posts.append(tiene_hashtags)

        tiene_menciones = self.getTieneHashtags(mencionesLista)

        posts.append(tiene_menciones)
        return posts

    def getPostDate(self, html_bs):
        abbr_date = html_bs.select('abbr[data-utime]')
        post_published_unix = abbr_date[0].get('data-utime')
        post_date = datetime.utcfromtimestamp(int(post_published_unix))

        post_date_argentina = post_date.strftime('%Y-%m-%d %H:%M:%S')
        post_published = post_date + timedelta(hours=-3)
        post_published_sql = post_published.strftime("%Y-%m-%d %H:%M:%S")
        
        post_published_str = post_published.replace(microsecond=0).isoformat() + "+0000"
        return post_published_str, post_published_unix, post_published_sql, post_date_argentina

    def getVideoLink(self, link_video):
        link = link_video[0].get('src')
        if link:
            link = link.replace('blob:', '')
        return link

    def getPageName(self):
        medio_span = self.html_bs.find_all('span', {'class': 'fwb'})
        medio_span_text = None
        if medio_span:
            medio_span_text = medio_span[0].getText()
        else:
            medio_span = self.html_bs.select('a[uid]')
            medio_span_text = medio_span[1].getText()
        return medio_span_text

    def getTieneHashtags(self, hashtagsLista):
        tiene_hashtags = False
        if hashtagsLista:
            tiene_hashtags = True
        return tiene_hashtags

    def getHasEmoji(self):
        has_emoji = False
        emoji_tags = self.html_bs.find_all('span', {'class': '_6qdm'})
        if emoji_tags:
            has_emoji = True
        return has_emoji

    def getFBActionTagsText(self):
        fb_action_tags_text = ''
        fb_action_tags = self.html_bs.find_all('span', {'class': 'fcg'})
        if fb_action_tags:
            fb_action_tags_text = fb_action_tags[0].getText()
        return fb_action_tags_text

    def getVideosPlaysCount(self, fbStringToNumber):
        video_plays_count = 0
        video_play_count_tags = self.html_bs.find_all('div', {'class': 'lfloat _ohe _50f8'})
        if video_play_count_tags:
            video_play_count_span_text = video_play_count_tags[0].getText().replace('reproducciones', '')
            video_plays_count = fbStringToNumber.convertStringToNumber(video_play_count_span_text)
        else:
            video_play_count_tags = self.html_bs.find_all('span', {'class': '_26fq'})
            if video_play_count_tags:
                video_play_count_span_text = video_play_count_tags[0].getText().replace('reproducciones', '')
                video_plays_count = fbStringToNumber.convertStringToNumber(video_play_count_span_text)
            
        return video_plays_count

    def getMencionesHashtags(self):
        mencionesLista = []
        hashtagsLista = []
        post_message_html = self.html_bs.find_all('div', {'class': '_5pbx userContent _3576'})
        for tag in post_message_html:
            menciones = tag.find_all('a', {'class': 'profileLink'})
            for mencion in menciones:
                mencionesLista.append(mencion.getText())

            hashtags = tag.find_all('span', {'class': '_58cm'})
            for hashtag in hashtags:
                hashtagsLista.append(hashtag.getText())
        return mencionesLista, hashtagsLista

    def getSubtituloLink(self):
        subtitulo_post = ""
        divSubtitulo = self.html_bs.find_all('div', {'class': '_6m7 _3bt9'})
        if divSubtitulo:
            subtitulo_post = divSubtitulo[0].getText()
        return subtitulo_post

    def getTituloLink(self):
        titulo = ""
        divTitulo = self.html_bs.find_all('div', {'class': 'mbs _6m6 _2cnj _5s6c'})

        # Si la lista no esta vacia, tengo un titulo
        if divTitulo:
            titulo = divTitulo[0].getText()
        return titulo

    def getSharesCount(self, fbStringToNumber):
        shares_count = 0
        shares_count_a = self.html_preview_bs.find_all('a', {'class': '_3rwx _42ft'})
        if shares_count_a:
            shares_count_a_text = shares_count_a[0].getText()
            shares_count_text = shares_count_a_text.replace(' veces compartido', '').replace(' vez compartido', '')
            shares_count = fbStringToNumber.convertStringToNumber(shares_count_text)
        return shares_count

    def getReactionsCount(self, fbStringToNumber):
        reactions_count = 0
        reactions_count_span = self.html_preview_bs.find_all('span', {'class': '_81hb'})
        if reactions_count_span:
            reactions_count_text = reactions_count_span[0].getText()
            reactions_count = fbStringToNumber.convertStringToNumber(reactions_count_text)
        return reactions_count

    def getCommentsCount(self, fbStringToNumber):
        comments_count = 0
        comments_count_a = self.html_preview_bs.find_all('a', {'class': '_3hg- _42ft'})
        if comments_count_a:
            comments_count_a_text = comments_count_a[0].getText()
            comments_count_text = comments_count_a_text.replace(' comentarios', '').replace(' comentario', '')
            comments_count = fbStringToNumber.convertStringToNumber(comments_count_text)
        return comments_count

    def getPostURL(self, page_id, post_id):
        return "https://www.facebook.com/" + page_id + "/posts/" + post_id + "/"

    def getPostID(self):
        post_id_div = self.html_bs.find_all('div', {'class': '_5pcp _5lel _2jyu _232_'})
        if post_id_div:
            feed_id = post_id_div[0].get("id")
            page_id = feed_id.split(';')[0]
            page_id_split = page_id.split('_')
            page_id = page_id_split[2]
            post_id = feed_id.split(';')[1]
        else:
            post_id = self.urlLink.split('/')[-2]
            page_id = self.html_bs.select('a[uid]')[1].get("uid")

        return post_id, page_id

    def getPicture(self):
        picture = ''

        picture_img = self.html_preview_bs.find_all('img', {'class': '_3chq'})
        if picture_img:
            picture = picture_img[0].get('src')
        return picture

    def getFullPicture(self):
        full_picture = ''
        post_picture_descripcion = ''
        full_picture_img = self.html_bs.find_all('img', {'class': 'scaledImageFitWidth'})
        if full_picture_img:
            full_picture = full_picture_img[0].get('src')
            post_picture_descripcion = full_picture_img[0].get('aria-label')
        return full_picture, post_picture_descripcion

    def getPostMessage(self):
        post_message = ''

        post_message_div = self.html_bs.find_all('div', {'class': '_7grk'})
        if post_message_div:
            return post_message_div[0].get("title")

        post_message_div = self.html_bs.find_all('div', {'class': '_5pbx userContent _3576'})
        if post_message_div:
            post_message = post_message_div[0].find_all('p')[0].getText()
        
        return post_message

    def getReactions(self, fbStringToNumber):
        reaction_count_tags = self.html_preview_bs.find_all('a', {'class': '_1n9l'})

        like_count_fb = 0
        rea_LOVE = 0
        rea_HAHA = 0
        rea_WOW = 0
        rea_SAD = 0
        rea_ANGRY = 0
        for a in reaction_count_tags:
            reaction_label = a.get('aria-label')
            if 'Me entristece' in reaction_label:
                reaction_label = reaction_label.replace(' Me entristece', '')
                rea_SAD = fbStringToNumber.convertStringToNumber(reaction_label)
            elif 'Me divierte' in reaction_label:
                reaction_label = reaction_label.replace(' Me divierte', '')
                rea_HAHA = fbStringToNumber.convertStringToNumber(reaction_label)
            elif 'Me encanta' in reaction_label:
                reaction_label = reaction_label.replace(' Me encanta', '')
                rea_LOVE = fbStringToNumber.convertStringToNumber(reaction_label)
            elif 'Me asombra' in reaction_label:
                reaction_label = reaction_label.replace(' Me asombra', '')
                rea_WOW = fbStringToNumber.convertStringToNumber(reaction_label)
            elif 'Me enoja' in reaction_label:
                reaction_label = reaction_label.replace(' Me enoja', '')
                rea_ANGRY = fbStringToNumber.convertStringToNumber(reaction_label)
            elif 'Me gusta' in reaction_label:
                reaction_label = reaction_label.replace(' Me gusta', '')
                like_count_fb = fbStringToNumber.convertStringToNumber(reaction_label)
        return like_count_fb, rea_LOVE, rea_WOW, rea_HAHA, rea_SAD, rea_ANGRY
