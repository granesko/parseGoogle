Данная программа выполняет следующие действия:
	1) подключается к базе MongoDB.Atlas (https://cloud.mongodb.com/)
	2) она считывает два списка (города и ссылки артистов) из базы Mongo
	3) проходит авторизацию в гугл
	4) переходит по ссылке на настройку рекламной компании в Google Ads,
	   созданной в этом аккаунте гугл
	5) потом выставляет необходимые параметры и начинаем менять 
	   города и ссылки на каналы youtube, доставая при этом значение
	   трафика
	6) затем сохраняет значение трафика в файл, в папку result, в формате:
	   {begin_date}_{end_date}_{url_name}.txt 
	7) затем сохраняет значение трафика в файл, в папку result_json, в формате:
	   {begin_date}_{end_date}_{url_name}.json 
	8) отправляет на MongoDB файл .json в базу указанную в параметре bd_result_name

geckodriver.exe необходим, чтобы selenium мог управлять браузером, он должен быть в дирректории с программой

скрипт запускает портативную версию браузера FirefoxPortable 56.0.1

Чтобы задать необходимые вам параметры воспользуйтесь parameters.txt.
Заполните параметры таким образом, как показано в parameters_exemple.txt
ВАЖНО: не ставьте в параметрах сегодняшнее число!
	-при желании можете указать свой аккаунт гугл, но не забудьте тогда сгенерировать ссылку
	 для гугл рекламы с этого аккаунта
параметры url и town помогут вам запустить скрипт с того места на котором вы остановились, вы можете зайти на mongo и посмотреть на каком моменте остановился скрипт, или глянуть в файлах папок result и result_json
параметры bd_result_name, bd_towns, bd_urls_and_ADSacc указывают базы которые будут использоваться для работы скрипта
из базы bd_urls_and_ADSacc вы берете аккаунт гугл с ссылкой на аккаунт гугл рекламы и ссылки артистов, которые вы будете использовать при парсинге
из базы bd_towns вы получаете список городов, в городах так же можно произвести сортировку по странам


так же убедитесь, что в вашей версии Python установлена библиотека selenium-3.3.3, для ее установки используйте команду: 
pip install selenium==3.3.3
ВАЖНО! С версией отличной от 3.3.3 скрипт работать не будет, selenoid не поймет
Если у вас возникли трудности с установкой библиотеки перейдите по данной ссылке:
https://pypi.org/project/selenium/

при установке pymongo воспользуйтесь следующими командами
!easy_install pymongo
!pip3 install pymongo[srv] - чтобы установить dnspython

Список версий:
pip-20.0.2
selenium-3.3.3
urllib3-1.25.8
Python 3.7.5
geckodriver 0.26
dnspython-1.16.0 pymongo-3.10.1