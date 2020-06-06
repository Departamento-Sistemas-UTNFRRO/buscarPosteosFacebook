import os
import platform
from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import ConfigManager
import PostFacebook
from OutputDataSetCSV import OuputDataSetCSV


def getFBLogin(fb_user, fb_password, gecko_binary, gecko_driver_exe, headless=False):
    driver = getFBPage('https://www.facebook.com/login/', gecko_binary, gecko_driver_exe, headless)
    body = driver.find_element_by_xpath('//body')
    body.send_keys(fb_user)
    body.send_keys(Keys.TAB)
    body.send_keys(fb_password)
    body.send_keys(Keys.TAB)
    body.send_keys(Keys.ENTER)
    print("Facebook login...")
    sleep(7)
    return driver


def getFBPage(url, gecko_binary, gecko_driver_exe, headless=False):
    ffoptions = Options()
    ffoptions.add_argument("--disable-notifications")
    if headless:
        ffoptions.headless = True

    ffprofile = FirefoxProfile()
    ffprofile.set_preference("dom.webnotifications.enabled", False)

    if platform.system() == 'Windows':
        binary = FirefoxBinary(gecko_binary)
        driver = webdriver.Firefox(firefox_binary=binary, executable_path=gecko_driver_exe, options=ffoptions, firefox_profile=ffprofile)
    else:
        driver = webdriver.Firefox(options=ffoptions, firefox_profile=ffprofile)

    driver.get(url)
    print("Opened url: " + str(url))
    sleep(5)
    return driver


def getFBSearchPage(driver, page, year):
    search_textbox = driver.find_element_by_css_selector("input[type='search'][aria-label]")
    search_textbox.send_keys(page)
    search_textbox.send_keys(Keys.ENTER)
    sleep(20)
    body = driver.find_element_by_xpath('//body')
    body.send_keys(Keys.TAB)
    body.send_keys(Keys.TAB)
    body.send_keys(Keys.TAB)
    body.send_keys(Keys.ENTER)
    sleep(5)
    
    body = driver.find_element_by_xpath('//body')
    body.send_keys(Keys.TAB)
    body.send_keys(Keys.TAB)
    body.send_keys(Keys.TAB)
    body.send_keys(Keys.TAB)
    body.send_keys(Keys.TAB)
    body.send_keys(Keys.ENTER)
    sleep(5)
    
    # tantos para abajo como años
    year_count = datetime.now().year - int(year)
    for _ in range(0, year_count):
        body.send_keys(Keys.ARROW_DOWN)
    body.send_keys(Keys.ENTER)

    sleep(2)

    search_textbox = driver.find_element_by_css_selector("input[type='search'][aria-label]")
    search_textbox.send_keys(Keys.TAB)
    for _ in range(0, 17):
        elem = driver.switch_to_active_element()
        elem.send_keys(Keys.TAB)
        sleep(1)

    sleep(52)
    elem = driver.switch_to_active_element()
    elem.send_keys(' ' + page)
    #elem.send_keys(page)
    sleep(2)
    elem = driver.switch_to.active_element
    elem.send_keys(Keys.ARROW_DOWN)

# <li aria-selected="false" class="k4urcfbm" id="{&quot;name&quot;:&quot;author&quot;,&quot;args&quot;:&quot;71339054219&quot;}" role="option"><div class="bp9cbjyn nhd2j8a9 j83agx80 ni8dbmo4 stjgntxs l9j0dhe7 ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi"><div aria-label="LA NACION" class="oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 j83agx80 mg4g778l btwxx1t3 pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb lzcic4wl abiwlrkh p8dawk7l k4urcfbm" role="button" tabindex="-1"><div class="j83agx80 oo9gr5id buofh1pr ni8dbmo4 stjgntxs cxgpxx05 dflh9lhu sj5x9vvc scb9dxdr"><div class="hpfvmrgz g5gj957u buofh1pr rj1gh0hx o8rfisnq"><div class="i1fnvgqd btwxx1t3 j83agx80"><div class="a8nywdso r8blr3vg rz4wbd8a jwdofwj8 stjgntxs ni8dbmo4 dumg13m2 jifvfom9 btwxx1t3 j83agx80"><div class="b3onmgus"><div class="l9j0dhe7"><img class="a8c37x1j ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi" src="https://scontent.fros1-1.fna.fbcdn.net/v/t1.0-1/cp0/p50x50/68688198_10157208774494220_3978553868437946368_n.jpg?_nc_cat=1&amp;_nc_sid=1eb0c7&amp;_nc_ohc=GzlSyzuZaMMAX9qZ9Lv&amp;_nc_ht=scontent.fros1-1.fna&amp;oh=4e632223b23094f9cb2203882142bd75&amp;oe=5EFF1BEC" alt="" width="36" height="36"><div class="oaz4zybt pmk7jnqg j9ispegn kr520xx4 ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi" style="height: 36px; width: 36px;"></div></div></div><div class="ni8dbmo4 kwzhilbh cbu4d94t j83agx80"><div class="hzawbc8m tw6a2znq"><span class="oi732d6d ik7dh3pa d2edcug0 qv66sw1b c1et5uql a8c37x1j muag1w35 ew0dbk1b jq4qci2q a3bd9o3v knj5qynh oo9gr5id ni8dbmo4 stjgntxs ltmttdrg g0qnabr5" dir="auto">LA NACION</span></div></div></div></div></div></div></div><div class=""></div></div></li>    
# search_textbox = driver.find_elements_by_css_selector("input[type='search'][aria-label='Elige un origen...']")
    search_textbox = driver.find_elements_by_css_selector("li.k4urcfbm[role='option']")
    for elem in search_textbox:
        if elem.text.upper() == page.upper():
            elem.click()
            break

    return driver


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
    posts = body.find_elements_by_class_name('sjgh65i0')

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

    fb_login = getFBLogin(config.fb_username, config.fb_password, config.gecko_binary, config.gecko_driver_exe, config.gecko_headless)
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

driver = getFBLogin(config.fb_username, config.fb_password, config.gecko_binary, config.gecko_driver_exe, config.gecko_headless)
posts_links_total = []

try:
    fb_search = getFBSearchPage(driver, config.fb_page_name,
                                config.fb_search_year)
    posts_links = getFBPostsLinks(fb_search, config.max_scroll)
    for post_link in posts_links:
        posts_links_total.append(post_link)
except Exception as ex:
    print("ERROR" + str(ex))

exportLinksCsv(config, posts_links_total)
print('Post Count: ', len(posts_links_total))
driver.quit()
exportNetvizzCsv(config, posts_links_total)