from flask import Flask, render_template, request, jsonify
import concurrent.futures
import requests
import bs4
import re

app = Flask(__name__, static_folder='static')

# Mock data for katdict and katdictx
katdict = {
    'Сите Категории\n': 'https://www.reklama5.mk/Search?city=&cat=0&q=&page=1',
    'Моторни Возила\n': 2,
    'Недвижности\n': 3,
    'Дом и Градина\n': 4,
    'Мода и Облека и Обувки\n': 5,
    'Мобилни телефони и додатоци\n': 6,
    'Компјутери\n': 7,
    'ТВ, Видео, Фото и Мултимедија\n': 8,
    'Музички инструменти и опрема\n': 9,
    'Часовници и Накит\n': 10,
    'Беби и Детски производи\n': 11,
    'Здравје, Убавина додат. и опрема\n': 12,
    'CD, DVD, VHS Музика, Филмови\n': 13,
    'Книги и литература\n': 14,
    'Канцелариски и Школски прибор\n': 15,
    'Слободно време и хоби, Животни\n': 16,
    'Спортска опрема и активности\n': 'https://www.reklama5.mk/Search?city=&cat=1063&page=1',
    'Антиквитети, Уметност, Колекц.\n': 'https://www.reklama5.mk/Search?city=&cat=1193&page=1',
    'Бизнис и дејности, Машини алати\n': 'https://www.reklama5.mk/Search?city=&cat=1207&page=1',
    'Храна и готвење\n': 'https://www.reklama5.mk/Search?city=&cat=1235&page=1',
    'Продавници, Трговија\n': 'https://www.reklama5.mk/Search?city=&cat=1254&page=1',
    'Услуги, Сервисери\n': 'https://www.reklama5.mk/Search?city=&cat=1255&page=1',
    'Вработување\n': 'https://www.reklama5.mk/Search?city=&cat=1256&page=1',
    'Настани, Ноќен живот, Изложби\n': 'https://www.reklama5.mk/Search?city=&cat=1257&page=1',
    'Одмор, Туризам, Билети, Патувања\n': 'https://www.reklama5.mk/Search?city=&cat=1258&page=1',
    'Лични контакти\n': 'https://www.reklama5.mk/Search?city=&cat=1259&page=1',
    'Останато\n': 'https://www.reklama5.mk/Search?city=&cat=1260&page=1'
}

katdictx = {

    2: {
        'Сите Моторни Возила \n': 'https://www.reklama5.mk/Search?city=&cat=1&q=&page=1',
        'Автомобили \n': 'https://www.reklama5.mk/Search?city=&cat=24&q=&page=1',
        'Мотори (над 50 cc) \n': 'https://www.reklama5.mk/Search?city=&cat=23&q=&page=1',
        'Мопеди (под 50 cc) \n': 'https://www.reklama5.mk/Search?city=&cat=22&q=&page=1',
        'Електрични скутери \n': 'https://www.reklama5.mk/Search?city=&cat=10046&q=&page=1',
        'Автобуси \n': 'https://www.reklama5.mk/Search?city=&cat=21&q=&page=1',
        'Комбиња \n': 'https://www.reklama5.mk/Search?city=&cat=20&q=&page=1',
        'Камиони \n': 'https://www.reklama5.mk/Search?city=&cat=27&q=&page=1',
        'Приколки \n': 'https://www.reklama5.mk/Search?city=&cat=28&q=&page=1',
        'Оштетени возила / за Резервни Делови \n': 'https://www.reklama5.mk/Search?city=&cat=29&q=&page=1',
        'Кампинг возила \n': 'https://www.reklama5.mk/Search?city=&cat=30&q=&page=1',
        'Земјоделски возила  \n': 'https://www.reklama5.mk/Search?city=&cat=31&q=&page=1',
        'Тешки воз.Градежни машини / Виљушкар  \n': 'https://www.reklama5.mk/Search?city=&cat=32&q=&page=1',
        'Бродови / чамци / Водни скутери  \n': 'https://www.reklama5.mk/Search?city=&cat=33&q=&page=1',
        'Авто делови и Авто Опрема  \n': 'https://www.reklama5.mk/Search?city=&cat=34&q=&page=1',
        'Делови за мотори / мопеди и Опрема  \n': 'https://www.reklama5.mk/Search?city=&cat=103&q=&page=1',
        'Шлеп служба \n': 'https://www.reklama5.mk/Search?city=&cat=10135&q=&page=1',
        'Откуп на Автомобили / Моторни Возила \n': 'https://www.reklama5.mk/Search?city=&cat=10150&q=&page=1',
        'Останато \n': 'https://www.reklama5.mk/Search?city=&cat=140&q=&page=1'
    },

    3: {
        'Сите Недвижности \n': 'https://www.reklama5.mk/Search?city=&cat=157&q=&page=1',
        'Куќи / Вили \n': 'https://www.reklama5.mk/Search?city=&cat=158&q=&page=1',
        'Станови \n': 'https://www.reklama5.mk/Search?city=&cat=159&q=&page=1',
        'Соби \n': 'https://www.reklama5.mk/Search?city=&cat=160&q=&page=1',
        'Викенд куќи \n': 'https://www.reklama5.mk/Search?city=&cat=161&q=&page=1',
        'Дуќани \n': 'https://www.reklama5.mk/Search?city=&cat=167&q=&page=1',
        'Деловен простор  \n': 'https://www.reklama5.mk/Search?city=&cat=168&q=&page=1',
        'Цимер / ка \n': 'https://www.reklama5.mk/Search?city=&cat=10000&q=&page=1',
        'Гаражи \n': 'https://www.reklama5.mk/Search?city=&cat=172&q=&page=1',
        'Плацеви и Ниви \n': 'https://www.reklama5.mk/Search?city=&cat=173&q=&page=1',
        'Магацини \n': 'https://www.reklama5.mk/Search?city=&cat=174&q=&page=1',
        'Бараки, киосци, трафики \n': 'https://www.reklama5.mk/Search?city=&cat=175&q=&page=1',
        'Новоградба \n': 'https://www.reklama5.mk/Search?city=&cat=176&q=&page=1',
        'Во странство \n': 'https://www.reklama5.mk/Search?city=&cat=177&q=&page=1',
        'Останато \n': 'https://www.reklama5.mk/Search?city=&cat=2441&q=&page=1'
    },

    4: {
        'Сите Дом и Градина \n': 'https://www.reklama5.mk/Search?city=&cat=189&page=1',
        'Дневна соба  \n': 'https://www.reklama5.mk/Search?city=&cat=190&page=1',
        'Спална соба  \n': 'https://www.reklama5.mk/Search?city=&cat=191&page=1',
        'Детска соба  \n': 'https://www.reklama5.mk/Search?city=&cat=192&page=1',
        'Кујна  \n': 'https://www.reklama5.mk/Search?city=&cat=193&page=1',
        'Садови и прибор  \n': 'https://www.reklama5.mk/Search?city=&cat=195&page=1',
        'Маси и столици -Трпезарии  \n': 'https://www.reklama5.mk/Search?city=&cat=196&page=1',
        'Бања / купатило  \n': 'https://www.reklama5.mk/Search?city=&cat=197&page=1',
        'Домашен текстил и Завеси  \n': 'https://www.reklama5.mk/Search?city=&cat=198&page=1',
        'Подна облога  \n': 'https://www.reklama5.mk/Search?city=&cat=199&page=1',
        'Полици и Места за складирање \n': 'https://www.reklama5.mk/Search?city=&cat=200&page=1',
        'Декорација и Украси  \n': 'https://www.reklama5.mk/Search?city=&cat=201&page=1',
        'Апарати за домаќинство  \n': 'https://www.reklama5.mk/Search?city=&cat=202&page=1',
        'Греење и климатизација  \n': 'https://www.reklama5.mk/Search?city=&cat=203&page=1',
        'Квалитет на Воздух  \n': 'https://www.reklama5.mk/Search?city=&cat=10057&page=1',
        'Соларни систeми и Опрема \n': 'https://www.reklama5.mk/Search?city=&cat=10142&page=1',
        'Светло и осветлување  \n': 'https://www.reklama5.mk/Search?city=&cat=204&page=1',
        'Струја и додатоци - Агрегати \n': 'https://www.reklama5.mk/Search?city=&cat=10012&page=1',
        'Градина  \n': 'https://www.reklama5.mk/Search?city=&cat=205&page=1',
        'Врати, Прозори и додатоци  \n': 'https://www.reklama5.mk/Search?city=&cat=206&page=1',
        'Безбедност и безбедносна опрема  \n': 'https://www.reklama5.mk/Search?city=&cat=207&page=1',
        'Домашни Алати и машини, Прибор  \n': 'https://www.reklama5.mk/Search?city=&cat=208&page=1',
        'Потреби за домаќинство  \n': 'https://www.reklama5.mk/Search?city=&cat=209&page=1',
        'Градежни материјали \n': 'https://www.reklama5.mk/Search?city=&cat=210&page=1',
        'Потрошни материјали  \n': 'https://www.reklama5.mk/Search?city=&cat=211&page=1',
        'Останато \n': 'https://www.reklama5.mk/Search?city=&cat=212&page=1'
    },

    5: {
        'Сите Мода и Облека и Обувки \n': 'https://www.reklama5.mk/Search?city=&cat=396&page=1',
        'Женска Облека \n': 'https://www.reklama5.mk/Search?city=&cat=397&page=1',
        'Машка Облека \n': 'https://www.reklama5.mk/Search?city=&cat=398&page=1',
        'Женски обувки \n': 'https://www.reklama5.mk/Search?city=&cat=399&page=1',
        'Машки обувки \n': 'https://www.reklama5.mk/Search?city=&cat=400&page=1',
        'Облека за момчиња \n': 'https://www.reklama5.mk/Search?city=&cat=401&page=1',
        'Облека за девојчиња \n': 'https://www.reklama5.mk/Search?city=&cat=402&page=1',
        'Обувки за момчиња \n': 'https://www.reklama5.mk/Search?city=&cat=403&page=1',
        'Обувки за девојчиња \n': 'https://www.reklama5.mk/Search?city=&cat=404&page=1',
        'Асесери / прибор  \n': 'https://www.reklama5.mk/Search?city=&cat=405&page=1',
        'Облека за трудници и додатоци  \n': 'https://www.reklama5.mk/Search?city=&cat=406&page=1',
        'Работна облека  \n': 'https://www.reklama5.mk/Search?city=&cat=407&page=1',
        'Останато \n': 'https://www.reklama5.mk/Search?city=&cat=408&page=1'
    },

    6: {
        'Сите Мобилни телефони и додатоци \n': 'https://www.reklama5.mk/Search?city=&cat=558&page=1',
        'Мобилни телефони \n': 'https://www.reklama5.mk/Search?city=&cat=559&page=1',
        'Додатоци за Мобилни телефони  \n': 'https://www.reklama5.mk/Search?city=&cat=560&page=1',
        'Паметни часовници - Smartwatch \n': 'https://www.reklama5.mk/Search?city=&cat=10004&page=1',
        'Фиксни телефони  \n': 'https://www.reklama5.mk/Search?city=&cat=561&page=1',
        'Факсови \n': 'https://www.reklama5.mk/Search?city=&cat=562&page=1',
        'Стари телефони \n': 'https://www.reklama5.mk/Search?city=&cat=10005&page=1',
        'Останато \n': 'https://www.reklama5.mk/Search?city=&cat=563&page=1'
    },

    7: {
        'Сите Компјутери \n': 'https://www.reklama5.mk/Search?city=&cat=580&page=1',
        'Десктоп компјутери \n': 'https://www.reklama5.mk/Search?city=&cat=581&page=1',
        'Лаптоп компјутери \n': 'https://www.reklama5.mk/Search?city=&cat=582&page=1',
        'Геминг и Дотатоци за Геминг  \n': 'https://www.reklama5.mk/Search?city=&cat=10111&page=1',
        'Таблети \n': 'https://www.reklama5.mk/Search?city=&cat=583&page=1',
        'Делови за Компјутери и додатоци  \n': 'https://www.reklama5.mk/Search?city=&cat=584&page=1',
        'Делови и опрема за Лаптопи  \n': 'https://www.reklama5.mk/Search?city=&cat=586&page=1',
        'Складирање меморија и медиумски додатоци \n': 'https://www.reklama5.mk/Search?city=&cat=10010&page=1',
        'Сервери и додатоци \n': 'https://www.reklama5.mk/Search?city=&cat=10011&page=1',
        'Mining Bitcoin Hardware \n': 'https://www.reklama5.mk/Search?city=&cat=10099&page=1',
        'Софтвери  \n': 'https://www.reklama5.mk/Search?city=&cat=585&page=1',
        'ПОС уреди \n': 'https://www.reklama5.mk/Search?city=&cat=587&page=1',
        'Останато \n': 'https://www.reklama5.mk/Search?city=&cat=588&page=1'
    },

    8: {
        'Сите ТВ, Видео, Фото и Мултимедија \n': 'https://www.reklama5.mk/Search?city=&cat=637&page=1',
        'Телевизори / LCD / Плазма \n': 'https://www.reklama5.mk/Search?city=&cat=638&page=1',
        'Дигитални фотоапарати \n': 'https://www.reklama5.mk/Search?city=&cat=640&page=1',
        'Галантерија за Фотоапарати  \n': 'https://www.reklama5.mk/Search?city=&cat=10124&page=1',
        'Hi-Fi / Аудио  \n': 'https://www.reklama5.mk/Search?city=&cat=641&page=1',
        'Домашно кино \n': 'https://www.reklama5.mk/Search?city=&cat=642&page=1',
        'DVD/HD/Видео/Blu-ray плеери  \n': 'https://www.reklama5.mk/Search?city=&cat=643&page=1',
        'Видео камери - Аналог  \n': 'https://www.reklama5.mk/Search?city=&cat=644&page=1',
        'Видео камери - Дигитални  \n': 'https://www.reklama5.mk/Search?city=&cat=645&page=1',
        'Дрон камери \n': 'https://www.reklama5.mk/Search?city=&cat=10001&page=1',
        'Сателитски антени и IPTV  \n': 'https://www.reklama5.mk/Search?city=&cat=646&page=1',
        'Играчки конзоли  \n': 'https://www.reklama5.mk/Search?city=&cat=647&page=1',
        'PC Игри и Видео игри  \n': 'https://www.reklama5.mk/Search?city=&cat=648&page=1',
        'МP3/4/5 плеери и iPod \n': 'https://www.reklama5.mk/Search?city=&cat=649&page=1',
        'Bluetooth уреди \n': 'https://www.reklama5.mk/Search?city=&cat=10003&page=1',
        'Паметни очила - Smart Glasses \n': 'https://www.reklama5.mk/Search?city=&cat=10002&page=1',
        'Фотокопири \n': 'https://www.reklama5.mk/Search?city=&cat=650&page=1',
        'GPS уреди \n': 'https://www.reklama5.mk/Search?city=&cat=651&page=1',
        'Безжична технологија \n': 'https://www.reklama5.mk/Search?city=&cat=652&page=1',
        'Далинси \n': 'https://www.reklama5.mk/Search?city=&cat=653&page=1',
        'Диктафони \n': 'https://www.reklama5.mk/Search?city=&cat=654&page=1',
        'Видео проектори и опрема \n': 'https://www.reklama5.mk/Search?city=&cat=655&page=1',
        'Електроника \n': 'https://www.reklama5.mk/Search?city=&cat=656&page=1',
        'Останато \n': 'https://www.reklama5.mk/Search?city=&cat=657&page=1'
    },

    9: {
        'Сите Музички инструменти и опрема \n': 'https://www.reklama5.mk/Search?city=&cat=753&page=1',
        'Mузички инструменти  \n': 'https://www.reklama5.mk/Search?city=&cat=754&page=1',
        'Опрема за музички инструменти  \n': 'https://www.reklama5.mk/Search?city=&cat=755&page=1',
        'ДЈ Опрема \n': 'https://www.reklama5.mk/Search?city=&cat=756&page=1',
        'Аудио и видео продукција \n': 'https://www.reklama5.mk/Search?city=&cat=757&page=1',
        'Изнајмување \n': 'https://www.reklama5.mk/Search?city=&cat=758&page=1',
        'Останато \n': 'https://www.reklama5.mk/Search?city=&cat=759&page=1'
    },

    10: {
        'Сите Часовници и Накит \n': 'https://www.reklama5.mk/Search?city=&cat=776&page=1',
        'Накит  \n': 'https://www.reklama5.mk/Search?city=&cat=777&page=1',
        'Часовници  \n': 'https://www.reklama5.mk/Search?city=&cat=778&page=1',
        'Бижутерија \n': 'https://www.reklama5.mk/Search?city=&cat=779&page=1',
        'Останато \n': 'https://www.reklama5.mk/Search?city=&cat=780&page=1',
    },

    11: {
        'Сите Беби и Детски производи \n': 'https://www.reklama5.mk/Search?city=&cat=856&page=1',
        'Детска машка облека  \n': 'https://www.reklama5.mk/Search?city=&cat=857&page=1',
        'Детска женска облека  \n': 'https://www.reklama5.mk/Search?city=&cat=858&page=1',
        'Детски чевли Машки  \n': 'https://www.reklama5.mk/Search?city=&cat=859&page=1',
        'Детски чевли Женски  \n': 'https://www.reklama5.mk/Search?city=&cat=860&page=1',
        'Бебешка опрема  \n': 'https://www.reklama5.mk/Search?city=&cat=861&page=1',
        'Бебешка нега \n': 'https://www.reklama5.mk/Search?city=&cat=862&page=1',
        'Бебешка детска храна \n': 'https://www.reklama5.mk/Search?city=&cat=863&page=1',
        'Играчки и игри \n': 'https://www.reklama5.mk/Search?city=&cat=864&page=1',
        'Кукли - Фигури од Видео игри \n': 'https://www.reklama5.mk/Search?city=&cat=10021&page=1',
        'Градинки \n': 'https://www.reklama5.mk/Search?city=&cat=865&page=1',
        'Останато \n': 'https://www.reklama5.mk/Search?city=&cat=866&page=1',
    },

    12: {
        'Сите Здравје, Убавина додат. и опрема \n': 'https://www.reklama5.mk/Search?city=&cat=919&page=1',
        'Нега на лице \n': 'https://www.reklama5.mk/Search?city=&cat=920&page=1',
        'Нега на коса \n': 'https://www.reklama5.mk/Search?city=&cat=921&page=1',
        'Нега на тело \n': 'https://www.reklama5.mk/Search?city=&cat=922&page=1',
        'Ослабување и Исхрана \n': 'https://www.reklama5.mk/Search?city=&cat=923&page=1',
        'Женска козметика \n': 'https://www.reklama5.mk/Search?city=&cat=924&page=1',
        'Машка козметика \n': 'https://www.reklama5.mk/Search?city=&cat=925&page=1',
        'Шминка \n': 'https://www.reklama5.mk/Search?city=&cat=926&page=1',
        'Депилација и Производи за бричење  \n': 'https://www.reklama5.mk/Search?city=&cat=10067&page=1',
        'Маникир и педикир \n': 'https://www.reklama5.mk/Search?city=&cat=927&page=1',
        'Парфеми и мириси  \n': 'https://www.reklama5.mk/Search?city=&cat=928&page=1',
        'Масажа и Сауна \n': 'https://www.reklama5.mk/Search?city=&cat=929&page=1',
        'Заштита од сонце \n': 'https://www.reklama5.mk/Search?city=&cat=930&page=1',
        'Стоматолошка грижа \n': 'https://www.reklama5.mk/Search?city=&cat=931&page=1',
        'Управување со тежината \n': 'https://www.reklama5.mk/Search?city=&cat=932&page=1',
        'Алтернативна медицина \n': 'https://www.reklama5.mk/Search?city=&cat=933&page=1',
        'Благосостојба и Wellness \n': 'https://www.reklama5.mk/Search?city=&cat=934&page=1',
        'Детска козметика \n': 'https://www.reklama5.mk/Search?city=&cat=935&page=1',
        'Медицински материјали  \n': 'https://www.reklama5.mk/Search?city=&cat=936&page=1',
        'Оптички уреди  \n': 'https://www.reklama5.mk/Search?city=&cat=937&page=1',
        'Останато \n': 'https://www.reklama5.mk/Search?city=&cat=938&page=1',
    },

    13: {
        'Сите CD, DVD, VHS Музика, Филмови \n': 'https://www.reklama5.mk/Search?city=&cat=959&page=1',
        'Film & DVD / VHS  \n': 'https://www.reklama5.mk/Search?city=&cat=960&page=1',
        'Blu-ray \n': 'https://www.reklama5.mk/Search?city=&cat=10013&page=1',
        '3D Blu-ray \n': 'https://www.reklama5.mk/Search?city=&cat=10014&page=1',
        '4K Ultra HD Blu-ray \n': 'https://www.reklama5.mk/Search?city=&cat=10015&page=1',
        'Музика & CD  \n': 'https://www.reklama5.mk/Search?city=&cat=961&page=1',
        'Грамафонски плочи \n': 'https://www.reklama5.mk/Search?city=&cat=962&page=1',
        'Останато \n': 'https://www.reklama5.mk/Search?city=&cat=963&page=1',
    },

    14: 'https://www.reklama5.mk/Search?city=&cat=987&page=1',
    15: 'https://www.reklama5.mk/Search?city=&cat=1019&page=1',
    16: {
        'Сите Слободно време и хоби, Животни \n': 'https://www.reklama5.mk/Search?city=&cat=1032&page=1',
        'Велосипеди \n': 'https://www.reklama5.mk/Search?city=&cat=1033&page=1',
        'Делови за Велосипеди и додатоци  \n': 'https://www.reklama5.mk/Search?city=&cat=10029&page=1',
        'Ховерборд и додатоци \n': 'https://www.reklama5.mk/Search?city=&cat=10007&page=1',
        'Тротинети и додатоци \n': 'https://www.reklama5.mk/Search?city=&cat=10028&page=1',
        'Колекционерски предмети \n': 'https://www.reklama5.mk/Search?city=&cat=1034&page=1',
        'Сувенири и подароци \n': 'https://www.reklama5.mk/Search?city=&cat=1035&page=1',
        'Забавни игри и Играчки  \n': 'https://www.reklama5.mk/Search?city=&cat=1036&page=1',
        'Празнични украси \n': 'https://www.reklama5.mk/Search?city=&cat=1037&page=1',
        'Цигари и Прибор за пушење \n': 'https://www.reklama5.mk/Search?city=&cat=1038&page=1',
        'Животни  \n': 'https://www.reklama5.mk/Search?city=&cat=1039&page=1',
        'Oдгледување на растенија \n': 'https://www.reklama5.mk/Search?city=&cat=10008&page=1',
        'Oдгледување на животни \n': 'https://www.reklama5.mk/Search?city=&cat=10009&page=1',
        'Останато \n': 'https://www.reklama5.mk/Search?city=&cat=1040&page=1',
    },

    

}

def is_gui_active():
    return False  # Since this is a Flask app, GUI is not active

def select_category(category_id):
    try:
        # Find category based on category_id (assuming category_id is a 1-based index)
        primary_category = list(katdict.keys())[category_id - 1]  
        primary_id = katdict[primary_category]
        primary_value = katdictx.get(primary_id)
        return primary_category, primary_value
    except IndexError:
        # Handle invalid category_id
        return None, None

def select_sec_category(primary_category, primary_value, subcategory_id=None):
    if isinstance(primary_value, str):
        # If the primary_value is a string, it is the URL
        return primary_category, primary_value
    elif isinstance(primary_value, dict):
        if subcategory_id is None:
            # If no subcategory_id is provided, return all subcategories
            return list(primary_value.items())
        else:
            # Otherwise, return the specific subcategory and its URL
            try:
                secondary_category = list(primary_value.keys())[subcategory_id - 1]
                secondary_url = primary_value[secondary_category]
                return secondary_category, secondary_url
            except IndexError:
                # Handle invalid subcategory_id
                return None, None
    else:
        return None, None


def page_read(secondary_url, max_page):
    adid = []
    adlink = []
    for page in range(1, max_page + 1):
        url = secondary_url + str(page)
        req = requests.get(url)
        if req.status_code == 200:
            soup = bs4.BeautifulSoup(req.text, 'html.parser')
            ads_on_page = soup.find_all('div', class_='ad-image-preview-table r5-slider')
            for ad in ads_on_page:
                adid.append(ad['data-adid'])
    adlink = ['https://www.reklama5.mk/AdDetails/?ad=' + str(i) for i in adid]
    return adlink

def fetch_ad_details(adrequest):
    adreq = requests.get(adrequest)
    adsoup = bs4.BeautifulSoup(adreq.text, 'html.parser')
    title = adsoup.find('h5', class_='card-title')
    price = adsoup.find('h5', class_='mb-0 defaultBlue')
    addesc = adsoup.find('p', class_='mt-3')
    addate_element = adsoup.find_all('div', class_='col-4 align-self-center')
    addate = addate_element[2].find('span').text if len(addate_element) > 2 else "N/A"
    ad_info = {
        'adlink': adrequest,
        'adtitle': title.text.strip() if title else 'N/A',
        'adprice': price.text.replace('\r\n', '').strip() if price else 'N/A',
        'addate': addate,
        'addesc': addesc.text.strip() if addesc else 'N/A',
    }
    return ad_info

def search_ads_and_update_progress(ads, keywords, search_title=True, search_desc=True, search_all=False):
    results = []
    for ad in ads:
        match_found = False
        if search_title or search_all:
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', ad.get("adtitle", "").lower()):
                    match_found = True
                    break
        if (not match_found) and (search_desc or search_all):
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', ad.get("addesc", "").lower()):
                    match_found = True
                    break
        if match_found:
            results.append(ad)
    return results

@app.route('/')
def index():
    return render_template('index.html', categories=katdict.items(), katdict=katdict, katdictx=katdictx)

@app.route('/select_category/<int:category_id>')
def select_category_route(category_id):
    # Get the primary category and its value
    primary_category, primary_value = select_category(category_id)
    
    if isinstance(primary_value, dict):
        # If primary_value is a dictionary, get the list of subcategories
        subcategories = select_sec_category(primary_category, primary_value)
        return jsonify({
            "primary_category": primary_category,
            "subcategories": subcategories
        })
    else:
        # If primary_value is a string (URL), return it directly
        return jsonify({
            "primary_category": primary_category,
            "url": primary_value
        })

@app.route('/select_subcategory/<int:category_id>/<int:subcategory_id>')
def select_subcategory_route(category_id, subcategory_id):
    # Get the primary category and its value
    primary_category, primary_value = select_category(category_id)
    
    # Get the specific subcategory and its URL
    secondary_category, secondary_url = select_sec_category(primary_category, primary_value, subcategory_id)
    
    return jsonify({
        "secondary_category": secondary_category,
        "url": secondary_url
    })

@app.route('/fetch_ads', methods=['POST'])
def fetch_ads():
    data = request.json
    secondary_url = data.get('url')
    max_page = data.get('max_page', 1)
    adlink = page_read(secondary_url, max_page)
    ads = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        future_to_ad = {executor.submit(fetch_ad_details, adrequest): adrequest for adrequest in adlink}
        for future in concurrent.futures.as_completed(future_to_ad):
            try:
                ad_info = future.result()
                if ad_info:
                    ads.append(ad_info)
            except Exception as exc:
                print(f'Ad request generated an exception: {exc}')
    return jsonify(ads)

@app.route('/search_ads', methods=['POST'])
def search_ads():
    data = request.json
    ads = data.get('ads')
    keywords = data.get('keywords')
    search_title = data.get('search_title', False)
    search_desc = data.get('search_desc', False)

    search_all = search_title and search_desc
    
    results = search_ads_and_update_progress(ads, keywords, search_title, search_desc, search_all)
    return jsonify(results)

# Translation for input
latin_to_macedonian = {
    'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е', 'zh': 'ж', 'z': 'з',
    'i': 'и', 'j': 'ј', 'k': 'к', 'l': 'л', 'lj': 'љ', 'm': 'м', 'n': 'н', 'nj': 'њ',
    'o': 'о', 'p': 'п', 'r': 'р', 's': 'с', 't': 'т', 'c': 'ц', 'ch': 'ч', 'dz': 'џ',
    'sh': 'ш', 'u': 'у', 'f': 'ф', 'h': 'х', 'y': 'у'
}

def transliterate_to_macedonian(text):
    """Convert a string from Latin to Macedonian Cyrillic."""
    sorted_keys = sorted(latin_to_macedonian.keys(), key=len, reverse=True)
    for key in sorted_keys:
        text = text.replace(key, latin_to_macedonian[key])
    return text

@app.route('/transliterate', methods=['POST'])
def transliterate():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    transliterated_text = transliterate_to_macedonian(text)
    return jsonify({'original': text, 'transliterated': transliterated_text})


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

""" @app.route('/results')
def results():
    return render_template('results.html') """

if __name__ == '__main__':
    app.run(debug=True)