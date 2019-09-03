import os
from datetime import datetime, timedelta
from time import sleep
from urllib.parse import urlparse

import bs4
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import ConfigManager
from InputDataSetCSV import InputDataSetCSV
from OutputDataSetCSV import OuputDataSetCSV
from FacebookStringToNumber import FacebookStringToNumber
from TextOutputFile import TextOutputFile


def getFacebookLogin(fb_user, fb_password):
    ffoptions = Options()
    ffoptions.add_argument("--disable-notifications")
    ffoptions.headless = True

    ffprofile = FirefoxProfile()
    ffprofile.set_preference("dom.webnotifications.enabled", False)

    driver = webdriver.Firefox(options=ffoptions, firefox_profile=ffprofile)
    driver.get('https://www.facebook.com/')
    print("Opened facebook...")
    wait = WebDriverWait(driver, 12)
    wait.until(EC.visibility_of_element_located((By.ID, "email")))
    a = driver.find_element_by_id('email')
    a.send_keys(fb_user)
    print("Email Id entered...")
    b = driver.find_element_by_id('pass')
    b.send_keys(fb_password)
    print("Password entered...")
    c = driver.find_element_by_id('loginbutton')
    c.click()
    print("Facebook login...")
    return driver


def getFacebookHtml(driver, target_page, scroll_count, fb_avcode):
    print("going to " + target_page)
    urlparsed = urlparse(target_page)
    urlpath = urlparsed.path
    urlsplit = urlpath.split('/')

    shares_link = 'https://www.facebook.com/shares/view?id=' + urlsplit[3] + '&av=' + fb_avcode
    print('Share Link:')
    print(shares_link)
    driver.get(shares_link)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, "repost_view_permalink")))

    scroll_nro = 0
    while HasScroll(driver) and scroll_nro < scroll_count:
        driver.find_element_by_xpath('//body').send_keys(Keys.CONTROL + Keys.END)
        now = datetime.now() # current date and time
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        print('scroll: ' + str(scroll_nro) + ' ' + date_time)
        scroll_nro = scroll_nro + 1
        sleep(5)

    html_body_elem = driver.find_element_by_id('repost_view_permalink')
    html_body = html_body_elem.get_attribute("innerHTML")
    return TextOutputFile(html_body)


def HasScroll(driver):
    link = driver.find_elements_by_css_selector('.uiMorePagerPrimary')
    return len(link) > 0


def exportNetvizzCsv(shared_posts, post_id, html_body):
    content = bs4.BeautifulSoup(html_body, 'lxml')
    div_post = content.find_all('div', {'class': '_5pcr userContentWrapper'})
    facebookStringToNumber = FacebookStringToNumber()

    shares_number = 0
    for d in div_post:
        shares_number = shares_number + 1
        print('Post Share: ' + str(shares_number))
        post = []
        post.append(post_id)

        # username
        profile_a = d.find_all('span', {'class': 'fwb'})
        profile_a = profile_a[0].find_all('a')
        profile_a_text = profile_a[0].getText()
        post.append(profile_a_text)

        post_type = '' # profile_a[1].getText()
        post.append(post_type)

        # post_published
        abbr_date = d.find_all('abbr', {'class': '_5ptz'})
        if (len(abbr_date) == 0):
            continue
        abbr_date_title = abbr_date[0].get('title')
        post_date = datetime.strptime(abbr_date_title, '%d/%m/%y %H:%M')
        post_date_argentina = post_date.strftime('%Y-%m-%d %H:%M:%S')
        post_published = post_date + timedelta(hours=3)
        post_published_sql = post_published.strftime("%Y-%m-%d %H:%M:%S")
        post_published_unix = abbr_date[0].get('data-utime')
        post.append(post_published.replace(microsecond=0).isoformat() + "+0000") 
        post.append(post_published_unix)
        post.append(post_published_sql)
        post.append(post_date_argentina)

        reaction_count_tags = d.find_all('a', {'class': '_3emk'})

        like_count_fb = 0
        rea_NONE = 0
        rea_LOVE = 0
        rea_HAHA = 0
        rea_WOW = 0
        rea_SAD = 0
        rea_ANGRY = 0
        rea_THANKFUL = 0
        for a in reaction_count_tags:
            reaction_aria_label = a.get('aria-label')
            if 'Me entristece' in reaction_aria_label:
                rea_SAD_text = reaction_aria_label.replace(' Me entristece', '')
                rea_SAD = facebookStringToNumber.convertStringToNumber(rea_SAD_text)
            elif 'Me divierte' in reaction_aria_label:
                rea_HAHA_text = reaction_aria_label.replace(' Me divierte', '')
                rea_HAHA = facebookStringToNumber.convertStringToNumber(rea_HAHA_text)
            elif 'Me encanta' in reaction_aria_label:
                rea_LOVE_text = reaction_aria_label.replace(' Me encanta', '')
                rea_LOVE = facebookStringToNumber.convertStringToNumber(rea_LOVE_text)
            elif 'Me asombra' in reaction_aria_label:
                rea_WOW_text = reaction_aria_label.replace(' Me asombra', '')
                rea_WOW = facebookStringToNumber.convertStringToNumber(rea_WOW_text)
            elif 'Me enoja' in reaction_aria_label:
                rea_ANGRY_text = reaction_aria_label.replace(' Me enoja', '')
                rea_ANGRY = facebookStringToNumber.convertStringToNumber(rea_ANGRY_text)
            elif 'Me gusta' in reaction_aria_label:
                likes_count_text = reaction_aria_label.replace(' Me gusta', '')
                like_count_fb = facebookStringToNumber.convertStringToNumber(likes_count_text)
            else:
                print(reaction_aria_label)

        post.append(like_count_fb)

        # comments_count_fb
        comments_count = 0
        comments_count_a = d.find_all('a', {'class': '_ipm _-56'})
        if len(comments_count_a) != 0:
            comments_count_a_text = comments_count_a[0].getText()
            comments_count_text = comments_count_a_text.replace(' comentarios', '').replace(' comentario', '')
            comments_count = facebookStringToNumber.convertStringToNumber(comments_count_text)

        post.append(comments_count)

        # reactions_count_fb
        reactions_count = 0
        reactions_count_span = d.find_all('span', {'class': '_4arz'})
        if len(reactions_count_span) != 0:
            reactions_count_text = reactions_count_span[0].find_all('span')[0].getText()
            reactions_count = facebookStringToNumber.convertStringToNumber(reactions_count_text)

        post.append(reactions_count)

        # shares_count_fb
        shares_count = 0
        shares_count_a = d.find_all('a', {'class': '_ipm _2x0m'})
        if len(shares_count_a) != 0:
            shares_count_a_text = shares_count_a[0].getText()
            shares_count_text = shares_count_a_text.replace(' veces compartido', '').replace(' vez compartido', '')
            shares_count = facebookStringToNumber.convertStringToNumber(shares_count_text)

        post.append(shares_count)

        engagement_fb = comments_count + reactions_count + shares_count
        post.append(engagement_fb)

        post.append(rea_NONE)
        post.append(like_count_fb)
        post.append(rea_LOVE)
        post.append(rea_WOW)
        post.append(rea_HAHA)
        post.append(rea_SAD)
        post.append(rea_ANGRY)
        post.append(rea_THANKFUL)

        # post_message
        post_message = ''
        has_emoji = False
        post_message_div = d.find_all('div', {'class': '_5pbx userContent _3576'})
        if len(post_message_div) != 0:
            post_message = post_message_div[0].find_all('p')[0].getText()
            emoji_tags = post_message_div[0].find_all('span', {'class': '_5mfr'})
            if len(emoji_tags) != 0:
                has_emoji = True

        post.append(post_message)
        post.append(has_emoji)

        mencionesLista = []
        hashtagsLista = []
        post_message_html = d.find_all('div', {'class': '_5pbx userContent _3576'})
        for tag in post_message_html:
            menciones = tag.find_all('a', {'class': 'profileLink'})
            for mencion in menciones:
                mencionesLista.append(mencion.getText())

            hashtags = tag.find_all('span', {'class': '_58cm'})
            for hashtag in hashtags:
                hashtagsLista.append(hashtag.getText())

        post.append(mencionesLista)
        post.append(hashtagsLista)

        tiene_hashtags = False
        if len(hashtagsLista) != 0:
            tiene_hashtags = True

        post.append(tiene_hashtags)

        tiene_menciones = False
        if len(mencionesLista) != 0:
            tiene_menciones = True

        post.append(tiene_menciones)

        #TODO: read shared comment and export to excel
        shared_posts.append(post)

config = ConfigManager.ConfigManager()
columns = ['post_id', 'username', 'post_type', 'post_published', 'post_published_unix', 'post_published_sql', 'post_hora_argentina','like_count_fb', 'comments_count_fb', 'reactions_count_fb', 'shares_count_fb', 'engagement_fb', 'rea_NONE', 'rea_LIKE', 'rea_LOVE', 'rea_WOW', 'rea_HAHA', 'rea_SAD', 'rea_ANGRY', 'rea_THANKFUL', 'post_message', 'has_emoji', 'menciones', 'hashtags', 'tiene_hashtags', 'tiene_menciones']

dataset_csv = InputDataSetCSV(config.input_filename, config.input_init, config.input_end)
posts_shares = OuputDataSetCSV(config.output_filename, columns)
facebook_login = getFacebookLogin(config.fb_username, config.fb_password)

i = 0
j = 0
posts = dataset_csv.dataset
for i in range(dataset_csv.init, dataset_csv.end):
    print('Post Nr: ' + str(i))
    j = j + 1
    post_id = posts[i][0]
    post_url = posts[i][1]
    shares_count_fb = posts[i][2]
    scroll_count = 1 + shares_count_fb / config.shares_per_page
    if scroll_count > config.max_scroll:
        scroll_count = config.max_scroll
    print("Shared Count:" + str(shares_count_fb))
    print("Max Scroll:" + str(scroll_count))

    try:
        text_output_file = getFacebookHtml(facebook_login, post_url, scroll_count, config.fb_avcode)
        output_filename_html = os.path.join(config.base_path, config.output_post_filename_prefix + str(post_id) + ".html")
        text_output_file.save(output_filename_html)
        exportNetvizzCsv(posts_shares, post_id, text_output_file.content)
        # Cada 5 posteos guardar el excel para no perder datos
        if j == config.shares_per_page * 2:
            posts_shares.save()
            facebook_login.quit()
            facebook_login = getFacebookLogin(config.fb_username, config.fb_password)
            j = 0 
    except Exception as ex:
        print(str(ex))

    #facebook_login.refresh()

facebook_login.quit()
# guardar posts_compartidos
posts_shares.save()
