# -*- coding: utf-8 -*-
def rusparse():
    import selenium
    from selenium import webdriver
    import time
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException#,ElementNotInteractableException 
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from pymongo import MongoClient
    import json
    
    
    # Задаем параметры
    with open('parameters.txt', 'r', encoding='utf-8') as file:
        data = file.read()
        
    elements = data.split('\n')
    name_mongodb = elements[1]
    password_mongodb = elements[3]
    begin_date = elements[5]
    end_date = elements[7]
    bd_result_name = elements[9]
    url_start = elements[11]
    town_start = elements[13]
    bd_towns = elements[15]
    bd_urls_and_ADSacc = elements[17]
    # подключаемся к MongoDB
    
    client = MongoClient("mongodb+srv://{name_mongodb}:{password_mongodb}@googleads-1rrcj.mongodb.net/test?retryWrites=true&w=majority".format(name_mongodb = name_mongodb, password_mongodb=password_mongodb))
    db = client.test
    db = client.traffic_bd
    db1 = client[bd_urls_and_ADSacc]
    # a мы используем еще ниже чтобы достать ссылки
    a = db1.posts.find_one()
    
    # Задаем параметры
    gmail = a['google_name']
    password = a['google_password']
    url_ads_company = a['googleads_url']
    print('Parameters:\n')
    print('name mongoDB: ',name_mongodb)
    print('password mongoDB: ',password_mongodb)
    print('begin date: ',begin_date)
    print('end date: ',end_date)
    print('gmail: ',gmail)
    print('password: ',password)
    print('url ads company:\n',url_ads_company)
    print('bd result name: ',bd_result_name)
    print('url start: ',url_start)
    print('town start: ',town_start)
    print('bd urls and ADSacc: ',bd_urls_and_ADSacc)
    print('bd towns: ',bd_towns)
    
    # считываем города и ссылки с файлов
    # ссылки
    links = [a['urls'][i]['link'] for i in range(len(a['urls']))]
    print('len(links): ',len(links))
    print(links[0])
    
    # чистим ссылки от непонятных параметров и playlists
    for i in range(len(links)):
        if '?' in links[i]:
            links[i] = links[i].split('?')[0]
    a = True 
    i = 0
    while a:
        try:
            if 'playlist' in links[i]:
                links.pop(i)
                print(links[i])
            i+=1
        except IndexError:
            a = False
    
    # города
    db_towns = client[bd_towns]
    a = db_towns.posts.find_one()
    towns =[]
    for town in a['towns']:
        if town['country']=='Russia':
            towns.append(town['ADS_name'])
    print('len(towns): ',len(towns))
    print(towns[0])
    
    
    db_result = client[bd_result_name]
    
    #begin_date = '20.04.2020'
    #end_date = '23.04.2020'
    #gmail = 'polinagorbatenko493@gmail.com'
    #password = 'buw0Ybet3'
    #url_ads_company = 'https://ads.google.com/aw/campaigns/new/video?ocid=444700965&cmpnInfo=%7B%221%22%3A4%2C%228%22%3A%228e1ca698-a1bb-473d-a4c1-b60be882d090%22%2C%2219%22%3A%7B%224%22%3A1%7D%7D&euid=397612770&__u=1208091730&uscid=444700965&__c=7675444285&authuser=0&enableAllBrowsers=1&sourceid=emp'
    """
    # считываем города и ссылки с файлов
    with open('towns.txt', 'r', encoding='utf-8') as file:
        data = file.read()
    towns = data.split('\n')
    print('len(towns): ',len(towns))
    print(towns[0])
    # теперь получаем links  с mongodb
    links = [a['urls'][i]['link'] for i in range(len(a['urls']))]
    print('len(links): ',len(links))
    print(links[0])
    #with open('links.txt', 'r', encoding='utf-8') as file:
    #    data = file.read()
    """    
        
    #links = data.split('\n')
    #print('len(links): ',len(links))
    #print(links[0])
    
    
    
    # Здесь находятся функции проверки
    # проверяем xpath
    def find_element_by_xpath(driver, xpath):
        try:
            element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except TimeoutException:
            print ("Username -> Loading the element took too much time!")
            
    # првоеряем class_name        
    def find_element_by_class_name(driver, class_name):
        try:
            element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
        except TimeoutException:
            print ("Username -> Loading the element took too much time!")
            
    # проверяем css_selector
    def find_element_by_css_selector(driver, css_selector):
        try:
            element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
            )
        except TimeoutException:
            print ("Username -> Loading the element took too much time!")
    
    # Парсим значение "Показы" из ads.google.com
    # Сначала выставляем необходимые параметры
    
    # Задаем параметры
    result = []
    
    print('selenium version: ',selenium.__version__)
            
    capabilities = {
        "browserName": "firefox",
        "version": "56.0",
        "enableVNC": True,
        "enableVideo": False,
        "sessionTimeout":"120s"
    }
    
    driver = webdriver.Remote(
        command_executor="http://185.204.0.149:4444/wd/hub",
        desired_capabilities=capabilities)
    
    
    driver.get('https://www.google.com/accounts/')
    #print('сделали вэбдрайвер')
    
    
    
    # надо авторизоваться в google account
    time.sleep(5)
    email = driver.find_element_by_id('identifierId')
    email.send_keys(gmail)
    next = driver.find_element_by_id('identifierNext')
    next.click()
    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
    finally:
        pass
    time.sleep(2)
    
    passwd = driver.find_element_by_name('password')    
    passwd.send_keys(password)
    next = driver.find_element_by_id('passwordNext')
    next.click()
    time.sleep(3)
    # переходим на страницу для создания новой рекламной компании
    driver.get(url_ads_company)
    # нажимаем Все равно продолжить
    date = driver.find_element_by_xpath("//*[.='Все равно продолжить']")
    date.click()
    
    
    # выставляем дату начала
    # открываем окошко с датами
    find_element_by_xpath(driver, "//*[.='Дата начала']")
    date = driver.find_element_by_xpath("//*[.='Дата начала']")
    d = date.find_element_by_xpath("//div/div/material-datepicker/div")
    d.click()
    # вписываем нашу дату
    find_element_by_xpath(driver, "//*[.='П']/../../../div[2]/material-input/div/div/label/input")
    d = driver.find_element_by_xpath("//*[.='П']/../../../div[2]/material-input/div/div/label/input")
    d.send_keys(Keys.CONTROL + 'a')
    d.send_keys(begin_date)
    d.send_keys(Keys.ENTER)
    time.sleep(10)
    # выставляем дату окончания
    # открываем окошко с датами
    find_element_by_xpath(driver, "//*[.='Дата окончания']")
    date = driver.find_element_by_xpath("//*[.='Дата окончания']")
    d = date.find_element_by_xpath("//../end-date-picker/optional-date-picker/div/div/material-datepicker/div/dropdown-button")
    d.click()
    time.sleep(10)
    # вписываем нашу дату
    find_element_by_xpath(driver, "//*[.='П']/../../../div[2]/material-input/div/div/label/input")
    d = driver.find_element_by_xpath("//*[.='П']/../../../div[2]/material-input/div/div/label/input")
    d.send_keys(Keys.CONTROL + 'a')
    d.send_keys(end_date)
    d.send_keys(Keys.ENTER)
    
    
    # открываем вкладку сети
    #date = driver.find_elements_by_css_selector("material-icon._ngcontent-awn-VIDEO-12")
    #date[5].click()
    # открываем вкладку сети
    date = driver.find_element_by_xpath("//*[.='Результаты поиска на YouTube, Видео YouTube, Партнерские видеоресурсы в КМС']")
    date.click()
    
    # оставляем галочку на Видео YouTube, по двум другим клацаем, чтобы убрать
    find_element_by_css_selector(driver, 'material-icon._ngcontent-awn-VIDEO-24')
    date = driver.find_elements_by_css_selector("material-icon._ngcontent-awn-VIDEO-24")
    date[0].click()
    date[2].click()
    
    
    # открываем вкладку местоположение
    date = driver.find_elements_by_css_selector("material-icon._ngcontent-awn-VIDEO-18")
    date[8].click()
    # нажимаем иконку "указать другое местоположение"
    find_element_by_css_selector(driver, "material-icon._ngcontent-awn-VIDEO-76")
    date = driver.find_elements_by_css_selector("material-icon._ngcontent-awn-VIDEO-76")
    date[2].click()
    
    
    # открываем тип ресурса
    date = driver.find_elements_by_css_selector("material-icon._ngcontent-awn-VIDEO-18")
    date[10].click()
    # выбираем тип ресурса
    find_element_by_css_selector(driver, "radio-box._ngcontent-awn-VIDEO-32")
    date = driver.find_elements_by_css_selector("radio-box._ngcontent-awn-VIDEO-32")
    date[2].click()
    
    
    # открываем дополнительные настройки
    date = driver.find_elements_by_css_selector("material-icon._ngcontent-awn-VIDEO-41")
    date[0].click()
    # нажимаем ограничение частоты показов
    date = driver.find_elements_by_css_selector("material-icon._ngcontent-awn-VIDEO-18")
    date[15].click()
    # ставим галочку ограничить частоту показов
    date = driver.find_elements_by_css_selector("material-icon._ngcontent-awn-VIDEO-24")
    date[3].click()
    # вводим число показов 1
    date = driver.find_elements_by_css_selector("input._ngcontent-awn-VIDEO-17")
    date[3].send_keys('1')
    
    
    # нажмем стрелку место размещения
    date = driver.find_elements_by_css_selector("material-icon._ngcontent-awn-VIDEO-18")
    date[22].click()
    
    # Теперь начинаем перебирать каналы и города
    # перебираем каналы ютуб
    i=1 # это чтобы засечь место элемента на котором будет ошибка, чтобы потов insert его опять за ним же и опять попробовать его обработать
    for canal in range(len(links[int(url_start):])):
        i += 1 # смотрим номер итерации
        try:
            url_name = links[int(url_start):][canal].split('/')[-1]
            traffic_artists = {
                "entityId" : '1',
                "start_date" : begin_date,  
                "end_date" : end_date,
                "url_name": links[int(url_start):][canal],
                "array": []
            }
    
            with open("result_json\\{begin_date}_{end_date}_{url_name}.json".format(begin_date=begin_date, end_date=end_date, url_name=url_name),'w') as file:
                json.dump(traffic_artists,file)
    
            start_link = time.time()
            # вводим ссылку на канал
            start = time.time()
            try:
                element = WebDriverWait(driver, 200).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/div/div[1]/picker-search-box/material-input/div/div[1]/label/input"))
                )
            finally:
                pass
    
            date = driver.find_element_by_xpath('/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/div/div[1]/picker-search-box/material-input/div/div[1]/label/input')
            date.send_keys(links[int(url_start):][canal])
            time.sleep(5)
            # нажмем крестик где введен канал(удалим текст в поисковой строке)
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/div/div[1]/picker-search-box/material-icon/i"))
                )
            finally:
                pass
    
            date = driver.find_element_by_xpath('/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/div/div[1]/picker-search-box/material-icon/i')
            date.click()
    
                # вводим ссылку на канал
            start = time.time()
            try:
                element = WebDriverWait(driver, 200).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/div/div[1]/picker-search-box/material-input/div/div[1]/label/input"))
                )
            finally:
                pass
    
            date = driver.find_element_by_xpath('/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/div/div[1]/picker-search-box/material-input/div/div[1]/label/input')
            date.send_keys(links[int(url_start):][canal])
            time.sleep(3)
            # появляются каналы YouTube (по ссылке всего один должен быть) нажимаем 
            start = time.time()
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/div/div[2]/dynamic-component/angular-picker-section/div/div[1]/div/picker-tree-root/div/picker-tree[1]/div/div/placement-component/div/material-icon/i"))
                )
            finally:
                pass
    
            date = driver.find_element_by_xpath('/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/div/div[2]/dynamic-component/angular-picker-section/div/div[1]/div/picker-tree-root/div/picker-tree[1]/div/div/placement-component/div/material-icon/i')
            date.click()
            time.sleep(1)
            # нажимаем галочку выбрать канал
            start = time.time()
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/div/div[2]/dynamic-component/angular-picker-section/div/div[1]/div/picker-tree-root/div/picker-tree/div/material-checkbox/div[1]/material-icon"))
                )
            finally:
                pass
    
            date = driver.find_element_by_xpath('/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/div/div[2]/dynamic-component/angular-picker-section/div/div[1]/div/picker-tree-root/div/picker-tree/div/material-checkbox/div[1]/material-icon')
            date.click()
    
        # достаем наше значение охвата - "Показы" для всего мира, а не для отдельного города
            time.sleep(20)# дело в том что элемент есть всегда, обновляется число
    
            def check_exists_by_class_name(class_name):
                try:
                    driver.find_element_by_class_name(class_name)
                except NoSuchElementException:
                    return False
                return True
    
            def check_exists_by_css_selector(css_selector):
                try:
                    driver.find_element_by_css_selector(css_selector)
                except NoSuchElementException:
                    return False
                return True
    
            if check_exists_by_css_selector('div._ngcontent-awn-VIDEO-66'):
                oxvat_world = driver.find_elements_by_css_selector('span._ngcontent-awn-VIDEO-66')[1].text
                print('world',oxvat_world)
            else:
                print('polomka')
                traffic_artists1 = {
                    "entityId" : '1',
                    "start_date" : begin_date,  
                    "end_date" : end_date,
                    "url_name": links[int(url_start):][canal],
                    "array": ['everywhere zero']
                }
                
                db.posts.insert_one(traffic_artists1)
                continue
            # перебираем города
            for city in range(int(town_start),len(towns)):    
    
                try:
                    # вписываем город
                    try:
                        element = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[1]/campaign-construction-panel/video-location-picker/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div[2]/div/basic-geopicker-editor/fieldset/custom-location-input/div/location-suggest-input/div/div[1]/material-input/div[1]/div[1]/label/input"))
                        )
                    finally:
                        pass    
    
                    date = driver.find_element_by_xpath('/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[1]/campaign-construction-panel/video-location-picker/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div[2]/div/basic-geopicker-editor/fieldset/custom-location-input/div/location-suggest-input/div/div[1]/material-input/div[1]/div[1]/label/input')
                    date.send_keys(towns[city])
                    # нажимаем кнопку включить
    
                    try:
                        element = WebDriverWait(driver, 200).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[5]/div/div/div[2]/div/material-list/div[1]/div/location-data-suggestion-entry/div/div/div[1]/material-button"))
                        )
                    finally:
                        pass
    
                    date = driver.find_element_by_xpath('/html/body/div[3]/div[5]/div/div/div[2]/div/material-list/div[1]/div/location-data-suggestion-entry/div/div/div[1]/material-button')
                    date.click()
    
                    # достаем наше значение охвата - "Показы"
                    time.sleep(1)# дело в том что элемент есть всегда, обновляется число
    
                    def check_exists_by_class_name(class_name):
                        try:
                            driver.find_element_by_class_name(class_name)
                        except NoSuchElementException:
                            return False
                        return True
    
                    def check_exists_by_css_selector(css_selector):
                        try:
                            driver.find_element_by_css_selector(css_selector)
                        except NoSuchElementException:
                            return False
                        return True
                    try:
                        if check_exists_by_css_selector('div._ngcontent-awn-VIDEO-66'):
                            oxvat = driver.find_elements_by_css_selector('span._ngcontent-awn-VIDEO-66')[1].text
    
                            while oxvat == oxvat_world:
                                #print('in while')
                                time.sleep(1)
    
    
                                try:
                                #if check_exists_by_css_selector('div._ngcontent-awn-VIDEO-63'):
                                    oxvat = driver.find_elements_by_css_selector('span._ngcontent-awn-VIDEO-66')[1].text
                                    metka = True
                                except IndexError:
                                #else:
                                    metka = False
                                    oxvat = '0'
    
                            if metka:
                                print(begin_date,';',end_date,';',towns[city],';',links[int(url_start):][canal],';',oxvat)
                                line_file ='{begin_date} ; {end_date} ; {city} ; {canal} ; {oxvat} ; '.format(begin_date=begin_date, end_date=end_date,city=towns[city] ,canal=links[int(url_start):][canal], oxvat=oxvat)
                                line_file = line_file.replace(' тыс.','000')
                                line_file = line_file.replace(' млн','000000')
    
                                result.append('{begin_date} ; {end_date} ; {city} ; {canal} ; {oxvat} ; '.format(begin_date=begin_date, end_date=end_date,city=city ,canal=links[int(url_start):][canal], oxvat=oxvat))
                                url_name = links[int(url_start):][canal].split('/')[-1]
                                with open("result\\{begin_date}_{end_date}_{url_name}.txt".format(begin_date=begin_date, end_date=end_date, url_name=url_name), "a") as file:
                                    print(line_file, file=file)
    
                            # in json 
                            oxvat = oxvat.replace(' тыс.','000')
                            oxvat = oxvat.replace(' млн','000000')
                            with open("result_json\\{begin_date}_{end_date}_{url_name}.json".format(begin_date=begin_date, end_date=end_date, url_name=url_name),'r') as read_file:
                                data = json.load(read_file)
                            a = {'city': towns[city], 'traffic': oxvat}
                            data['array'].append(a)    
                            with open("result_json\\{begin_date}_{end_date}_{url_name}.json".format(begin_date=begin_date, end_date=end_date, url_name=url_name),'w') as file:
                                json.dump(data,file)
    
                            # отправляем на mongo
                            db_result.posts.insert_one({'begin_date':begin_date, 'end_date':end_date,'url':links[int(url_start):][canal], 'town':towns[city], 'traffic': oxvat})
    
    
                        else:
                            try:
                                element = WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[2]/traffic-estimation-panel/div/nudge/div/div"))
                                )
    
                            finally:
                                pass
                            print(begin_date,';',end_date,';',towns[city],';',links[int(url_start):][canal],';',0)
                            line_file ='{begin_date} ; {end_date} ; {city} ; {canal} ; 0 ; '.format(begin_date=begin_date, end_date=end_date,city=towns[city] ,canal=links[int(url_start):][canal])            
                            result.append('{begin_date} ; {end_date} ; {city} ; {canal} ; 0 ; '.format(begin_date=begin_date, end_date=end_date,city=city ,canal=links[int(url_start):][canal]))
                            url_name = links[int(url_start):][canal].split('/')[-1]
                            with open("result\\{begin_date}_{end_date}_{url_name}.txt".format(begin_date=begin_date, end_date=end_date, url_name=url_name), "a") as file:
                                print(line_file, file=file) 
    
                            # in json
                            with open("result_json\\{begin_date}_{end_date}_{url_name}.json".format(begin_date=begin_date, end_date=end_date, url_name=url_name),'r') as read_file:
                                data = json.load(read_file)
                            a = {'city': towns[city], 'traffic': '0'}
                            data['array'].append(a)    
                            with open("result_json\\{begin_date}_{end_date}_{url_name}.json".format(begin_date=begin_date, end_date=end_date, url_name=url_name),'w') as file:
                                json.dump(data,file)
    
                            # отправляем на mongo
                            db_result.posts.insert_one({'begin_date':begin_date, 'end_date':end_date,'url':links[int(url_start):][canal], 'town':towns[city], 'traffic': 0})
    
    
    
    
                    except IndexError:
                        print('from except')
                        print(begin_date,';',end_date,';',towns[city],';',links[int(url_start):][canal],';',0)
                        line_file ='{begin_date} ; {end_date} ; {city} ; {canal} ; 0 ; '.format(begin_date=begin_date, end_date=end_date,city=towns[city] ,canal=links[int(url_start):][canal])            
                        result.append('{begin_date} ; {end_date} ; {city} ; {canal} ; 0 ; '.format(begin_date=begin_date, end_date=end_date,city=city ,canal=links[int(url_start):][canal]))
                        url_name = links[int(url_start):][canal].split('/')[-1]
                        with open("result\\{begin_date}_{end_date}_{url_name}.txt".format(begin_date=begin_date, end_date=end_date, url_name=url_name), "a") as file:
                            print(line_file, file=file)
    
    
    
    
    
                    # закрываем город чтобы потом вбить новый
                    try:
                        element = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[1]/campaign-construction-panel/video-location-picker/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div[2]/div/basic-geopicker-editor/fieldset/custom-location-input/location-display-list-group/location-display-list/table/thead/tr/th[2]/material-icon"))
                        )
                    finally:
                        pass
    
                    date = driver.find_element_by_xpath('/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[1]/campaign-construction-panel/video-location-picker/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div[2]/div/basic-geopicker-editor/fieldset/custom-location-input/location-display-list-group/location-display-list/table/thead/tr/th[2]/material-icon')
                    date.click()
    
                except (TimeoutException, NoSuchElementException, StaleElementReferenceException):#, ElementNotInteractableException
                    print('TOWN - TimeoutException, or NoSuchElementException, or ElementNotInteractableException, or StaleElementReferenceException!')
                    # закрываем город чтобы опять его ввести в теле цикла
                    try:
                        element = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[1]/campaign-construction-panel/video-location-picker/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div[2]/div/basic-geopicker-editor/fieldset/custom-location-input/location-display-list-group/location-display-list/table/thead/tr/th[2]/material-icon"))
                        )
                    except TimeoutException:
                        pass
                    else:
                        date = driver.find_element_by_xpath('/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[1]/campaign-construction-panel/video-location-picker/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div[2]/div/basic-geopicker-editor/fieldset/custom-location-input/location-display-list-group/location-display-list/table/thead/tr/th[2]/material-icon')
                        date.click()
                    finally:
                        pass
    
                    # удаляем город который вписывали, но не включили
                    try:
                        element = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[1]/campaign-construction-panel/video-location-picker/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div[2]/div/basic-geopicker-editor/fieldset/custom-location-input/div/location-suggest-input/div/div[1]/material-input/div[1]/div[1]/label/input"))
                        )
                    except TimeoutException:
                        pass
                    else:
                        date = driver.find_element_by_xpath('/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[1]/campaign-construction-panel/video-location-picker/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div[2]/div/basic-geopicker-editor/fieldset/custom-location-input/div/location-suggest-input/div/div[1]/material-input/div[1]/div[1]/label/input')
                        date.send_keys(Keys.CONTROL + 'a')
                        date.send_keys(Keys.DELETE)
                    finally:
                        pass    
    
                    city -=1 
    
    
            # отправим джейсон на монгодб
            with open("result_json\\{begin_date}_{end_date}_{url_name}.json".format(begin_date=begin_date, end_date=end_date, url_name=url_name),'r') as read_file:
                json_artist = json.load(read_file)
    
            db.posts.insert_one(json_artist)
    
            # после того как перебрали все города по ссылке артиста, надо закрыть ссылку
            # нажмем крестик где введен канал(удалим текст в поисковой строке)
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/div/div[1]/picker-search-box/material-icon/i"))
                )
            finally:
                pass
    
            date = driver.find_element_by_xpath('/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/div/div[1]/picker-search-box/material-icon/i')
            date.click()
            # удаляем канал, в списке выбранных каналов
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/dynamic-component/picker-shopping-cart/div/div[2]/div/div[2]/div[2]/picker-tree/div/material-icon"))
                )
            finally:
                pass
    
            date = driver.find_element_by_xpath('/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/dynamic-component/picker-shopping-cart/div/div[2]/div/div[2]/div[2]/picker-tree/div/material-icon')
            date.click()
    
            result = []
            print(time.time()- start_link)
    
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException):#, ElementNotInteractableException
            print('LINK - TimeoutException, or NoSuchElementException, or ElementNotInteractableException, or StaleElementReferenceException!')
            links.insert(i+int(url_start),links[int(url_start):][canal])
            print(links[int(url_start):int(url_start)+10])
            # нажмем крестик где введен канал(удалим текст в поисковой строке)
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/div/div[1]/picker-search-box/material-icon/i"))
                )
            except TimeoutException:
                pass
            else:
                date = driver.find_element_by_xpath('/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/div/div[1]/picker-search-box/material-icon/i')
                date.click()
            # удаляем канал, в списке выбранных каналов
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/dynamic-component/picker-shopping-cart/div/div[2]/div/div[2]/div[2]/picker-tree/div/material-icon"))
                )
            except TimeoutException:
                pass
            else:
                date = driver.find_element_by_xpath('/html/body/div[2]/root/div/div[1]/div/div/div[3]/awsm-child-content/div[2]/div/video-root/base-root/div/div[2]/div[1]/view-loader/video-campaign-construction-shell/video-campaign-construction/material-stepper/div[2]/div/div[1]/div[1]/section[2]/ad-group-construction-panel/pickers-section[2]/section/placement-picker-panel/expansion-panel/material-expansionpanel/div/div[2]/div/div[1]/div/div/div/placement-picker/picker/div/div/dynamic-component/picker-shopping-cart/div/div[2]/div/div[2]/div[2]/picker-tree/div/material-icon')
                date.click()
        
        
            
    # Закроем webdriver (браузер)
    driver.close()
