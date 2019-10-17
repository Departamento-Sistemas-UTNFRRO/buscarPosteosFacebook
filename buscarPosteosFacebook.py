import os
from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options

import ConfigManager
import PostFacebook
from OutputDataSetCSV import OuputDataSetCSV


def getFBLogin(fb_user, fb_password, headless=False):
    ffoptions = Options()
    ffoptions.add_argument("--disable-notifications")
    if headless:
        ffoptions.headless = True

    ffprofile = FirefoxProfile()
    ffprofile.set_preference("dom.webnotifications.enabled", False)

    driver = webdriver.Firefox(options=ffoptions, firefox_profile=ffprofile)
    driver.get('https://www.facebook.com/login/')
    print("Opened facebook...")
    sleep(5)

    body = driver.find_element_by_xpath('//body')
    body.send_keys(fb_user)
    body.send_keys(Keys.TAB)
    body.send_keys(fb_password)
    body.send_keys(Keys.TAB)
    body.send_keys(Keys.ENTER)
    print("Facebook login...")
    sleep(7)
    return driver


def getFBPage(url, headless=False):
    ffoptions = Options()
    ffoptions.add_argument("--disable-notifications")
    if headless:
        ffoptions.headless = True

    ffprofile = FirefoxProfile()
    ffprofile.set_preference("dom.webnotifications.enabled", False)

    driver = webdriver.Firefox(options=ffoptions, firefox_profile=ffprofile)
    driver.get(url)
    print("Opened url...")
    sleep(5)
    return driver


def getFBSearchPage(fb_login, page, month, year, destacadas):
    search_textbox = fb_login.find_element_by_name('q')
    search_textbox.send_keys(page)
    search_textbox.send_keys(Keys.ENTER)
    sleep(5)
    body = fb_login.find_element_by_xpath('//body')
    body.send_keys(Keys.ARROW_DOWN)
    body.send_keys(Keys.ENTER)
    sleep(5)

    search_more_origin = fb_login.find_element_by_class_name('_1u6r')
    search_more_origin.click()
    sleep(5)

    body.send_keys(page)
    body.send_keys(Keys.ARROW_DOWN)
    body.send_keys(Keys.ENTER)

    sleep(5)

    #0 destacadas
    #1 recientes
    search_date_more = fb_login.find_elements_by_class_name('_4f3b')[destacadas]
    search_date_more.click()
    sleep(5)

    body = fb_login.find_element_by_xpath('//body')
    body.send_keys(Keys.TAB)
    body.send_keys(Keys.CONTROL + Keys.END)
    for i in range(0, 10):
        body.send_keys(Keys.ARROW_DOWN)

    search_date_more = fb_login.find_elements_by_class_name('_1u6r')[3]
    search_date_more.click()

    # Primero el año
    body.send_keys(Keys.TAB)
    body.send_keys(Keys.TAB)

    body.send_keys(Keys.ARROW_DOWN)

    year_count = datetime.now().year - int(year)
    for i in range(0, year_count + 1):
        elem = fb_login.switch_to_active_element()
        print(elem.text)
        if elem.text == str(year):
            break
        body.send_keys(Keys.ARROW_DOWN)
    body.send_keys(Keys.ENTER)

    sleep(15)

    body.send_keys(Keys.TAB)
    body.send_keys(Keys.CONTROL + Keys.END)
    for i in range(0, 10):
        body.send_keys(Keys.ARROW_DOWN)

    search_date_more = fb_login.find_elements_by_class_name('_1u6r')[3]
    search_date_more.click()

    body.send_keys(Keys.TAB)
    body.send_keys(Keys.NUMPAD2)
    # Empieza en enero
    month_count = int(month)
    for i in range(0, month_count):
        elem = fb_login.switch_to_active_element()
        print(elem.text)
        if elem.text == str(month):
            break
        body.send_keys(Keys.ARROW_DOWN)
    body.send_keys(Keys.ENTER)
    return fb_login


def getFBPostsLinks(driver, scroll_count):
    scroll_nro = 0
    while HasScroll(driver) and scroll_nro < scroll_count:
        body = driver.find_element_by_xpath('//body')
        body.send_keys(Keys.CONTROL + Keys.END)
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        print('scroll: ' + str(scroll_nro) + ' ' + date_time)
        scroll_nro = scroll_nro + 1
        sleep(5)

    sleep(5)

    body = driver.find_element_by_xpath('//body')
    posts = body.find_elements_by_class_name('_307z')

    posts_links = []
    for html_preview in posts:
        link = html_preview.find_element_by_class_name('_lie')
        posts_links.append((link.get_attribute("href"), html_preview.get_attribute("innerHTML")))

    return posts_links


def HasScroll(driver):
    return driver.find_element_by_tag_name('div')


def exportLinksCsv(config, posts_links):
    columns = ['post_link']
    now = datetime.now()
    date_time = now.strftime("%m_%d_%Y_%H_%M_%S")
    filename_csv = config.output_post_filename_prefix + str(date_time) + ".csv"
    output_filename_csv = os.path.join(config.base_path, filename_csv)
                                       
    posts_fb = OuputDataSetCSV(output_filename_csv, columns)
    for post_link in posts_links:
        posts_fb.append([post_link[0]])
    posts_fb.save()


def exportNetvizzCsv(config, posts_links):
    columns = ['type', 'medio', 'by', 'post_id', 'post_link', 'post_message', 'picture', 'full_picture', 'link', 'link_domain', 'post_published', 'post_published_unix', 'post_published_sql', 'post_hora_argentina', 'like_count_fb', 'comments_count_fb', 'reactions_count_fb', 'shares_count_fb', 'engagement_fb', 'rea_LIKE', 'rea_LOVE', 'rea_WOW', 'rea_HAHA', 'rea_SAD', 'rea_ANGRY', 'post_picture_descripcion', 'poll_count', 'titulo_link', 'subtitulo_link', 'menciones', 'hashtags', 'video_plays_count', 'fb_action_tags_text', 'has_emoji', 'tiene_hashtags', 'tiene_menciones']
    posts_fb = OuputDataSetCSV(config.output_filename, columns)

    fb_login = getFBLogin(config.fb_username, config.fb_password)

    i = 0
    for post_link, html_preview in posts_links:
        i = i + 1
        print("Post " + str(i))
        print("URL: " + post_link)
        try:

            post = PostFacebook.PostFacebook(post_link, fb_login, html_preview)
            post.SaveHtml(config.base_path)
            posts = post.ParsePostHTML()
            posts_fb.append(posts)
            sleep(17)
        except Exception as ex:
            print("ERROR" + str(ex)) 
    
    fb_login.quit()
    print('END Post')
    posts_fb.save()


# Programa Principal
config = ConfigManager.ConfigManager()

fb_login = getFBLogin(config.fb_username, config.fb_password)
posts_links_total = []
destacadas = 0

while destacadas < 2:
    try:
        fb_search = getFBSearchPage(fb_login, config.fb_page_name,
                                    config.fb_search_month,
                                    config.fb_search_year, destacadas)
        posts_links = getFBPostsLinks(fb_search, config.max_scroll)
        for post_link in posts_links:
            posts_links_total.append(post_link)
    except Exception as ex:
            print("ERROR" + str(ex)) 
        
    fb_login.get('https://www.facebook.com')
    print("Opened facebook...")
    print("Searching Parameters: ", config.fb_search_month, " ", config.fb_search_year, " ", destacadas)
    sleep(8)

    if destacadas == 0:
        destacadas = 1
    else:
        destacadas = 2


exportLinksCsv(config, posts_links_total)
print('Post Count: ', len(posts_links_total))
fb_login.quit()
exportNetvizzCsv(config, posts_links_total)