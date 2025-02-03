# Reklama 5 scraper
# Author: Milosh Smiljkovikj
# Date: 29/01/2025
# Description: Proverka na reklami objaveni na reklama 5 so izbor na del od opisot

import bs4
import json
import requests
import concurrent.futures
import re

#urlselector
katdict = {
    '1. Сите Категории\n': 1,
    '2. Моторни Возила\n': 2,
    '3. Недвижности\n': 3,
    '4. Дом и Градина\n': 4,
    '5. Мода и Облека и Обувки\n': 5,
    '6. Мобилни телефони и додатоци\n': 6,
    '7. Компјутери\n': 7,
    '8. ТВ, Видео, Фото и Мултимедија\n': 8,
    '9. Музички инструменти и опрема\n': 9,
    '10. Часовници и Накит\n': 10,
    '11. Беби и Детски производи\n': 11,
    '12. Здравје, Убавина додат. и опрема\n': 12,
    '13. CD, DVD, VHS Музика, Филмови\n': 13,
    '14. Книги и литература\n': 14,
    '15. Канцелариски и Школски прибор\n': 15,
    '16. Слободно време и хоби, Животни\n': 16,
    '17. Спортска опрема и активности\n': 17,
    '18. Антиквитети, Уметност, Колекц.\n': 18,
    '19. Бизнис и дејности, Машини алати\n': 19,
    '20. Храна и готвење\n': 20,
    '21. Продавници, Трговија\n': 21,
    '22. Услуги, Сервисери\n': 22,
    '23. Вработување\n': 23,
    '24. Настани, Ноќен живот, Изложби\n': 24,
    '25. Одмор, Туризам, Билети, Патувања\n': 25,
    '26. Лични контакти\n': 26,
    '27. Останато\n': 27
}

katdictx = {

1: 'https://www.reklama5.mk/Search?city=&cat=0&q=&page=1',

2: {
    '1.Сите Моторни Возила \n': 'https://www.reklama5.mk/Search?city=&cat=1&q=&page=1',
    '2.Автомобили \n': 'https://www.reklama5.mk/Search?city=&cat=24&q=&page=1',
    '3.Мотори (над 50 cc) \n': 'https://www.reklama5.mk/Search?city=&cat=23&q=&page=1',
    '4.Мопеди (под 50 cc) \n': 'https://www.reklama5.mk/Search?city=&cat=22&q=&page=1',
    '5.Електрични скутери \n': 'https://www.reklama5.mk/Search?city=&cat=10046&q=&page=1',
    '6.Автобуси \n': 'https://www.reklama5.mk/Search?city=&cat=21&q=&page=1',
    '7.Комбиња \n': 'https://www.reklama5.mk/Search?city=&cat=20&q=&page=1',
    '8.Камиони \n': 'https://www.reklama5.mk/Search?city=&cat=27&q=&page=1',
    '9.Приколки \n': 'https://www.reklama5.mk/Search?city=&cat=28&q=&page=1',
    '10.Оштетени возила / за Резервни Делови \n': 'https://www.reklama5.mk/Search?city=&cat=29&q=&page=1',
    '11.Кампинг возила \n': 'https://www.reklama5.mk/Search?city=&cat=30&q=&page=1',
    '12.Земјоделски возила  \n': 'https://www.reklama5.mk/Search?city=&cat=31&q=&page=1',
    '13.Тешки воз.Градежни машини / Виљушкар  \n': 'https://www.reklama5.mk/Search?city=&cat=32&q=&page=1',
    '14.Бродови / чамци / Водни скутери  \n': 'https://www.reklama5.mk/Search?city=&cat=33&q=&page=1',
    '15.Авто делови и Авто Опрема  \n': 'https://www.reklama5.mk/Search?city=&cat=34&q=&page=1',
    '16.Делови за мотори / мопеди и Опрема  \n': 'https://www.reklama5.mk/Search?city=&cat=103&q=&page=1',
    '17.Шлеп служба \n': 'https://www.reklama5.mk/Search?city=&cat=10135&q=&page=1',
    '18.Откуп на Автомобили / Моторни Возила \n': 'https://www.reklama5.mk/Search?city=&cat=10150&q=&page=1',
    '19.Останато \n': 'https://www.reklama5.mk/Search?city=&cat=140&q=&page=1'
},

3: {
    '1.Сите Недвижности \n': 'https://www.reklama5.mk/Search?city=&cat=157&q=&page=1',
    '2.Куќи / Вили \n': 'https://www.reklama5.mk/Search?city=&cat=158&q=&page=1',
    '3.Станови \n': 'https://www.reklama5.mk/Search?city=&cat=159&q=&page=1',
    '4.Соби \n': 'https://www.reklama5.mk/Search?city=&cat=160&q=&page=1',
    '5.Викенд куќи \n': 'https://www.reklama5.mk/Search?city=&cat=161&q=&page=1',
    '6.Дуќани \n': 'https://www.reklama5.mk/Search?city=&cat=167&q=&page=1',
    '7.Деловен простор  \n': 'https://www.reklama5.mk/Search?city=&cat=168&q=&page=1',
    '8.Цимер / ка \n': 'https://www.reklama5.mk/Search?city=&cat=10000&q=&page=1',
    '9.Гаражи \n': 'https://www.reklama5.mk/Search?city=&cat=172&q=&page=1',
    '10.Плацеви и Ниви \n': 'https://www.reklama5.mk/Search?city=&cat=173&q=&page=1',
    '11.Магацини \n': 'https://www.reklama5.mk/Search?city=&cat=174&q=&page=1',
    '12.Бараки, киосци, трафики \n': 'https://www.reklama5.mk/Search?city=&cat=175&q=&page=1',
    '13.Новоградба \n': 'https://www.reklama5.mk/Search?city=&cat=176&q=&page=1',
    '14.Во странство \n': 'https://www.reklama5.mk/Search?city=&cat=177&q=&page=1',
    '15.Останато \n': 'https://www.reklama5.mk/Search?city=&cat=2441&q=&page=1'
},

4: {
    '1.Сите Дом и Градина \n': 'https://www.reklama5.mk/Search?city=&cat=189&page=1',
    '2.Дневна соба  \n': 'https://www.reklama5.mk/Search?city=&cat=190&page=1',
    '3.Спална соба  \n': 'https://www.reklama5.mk/Search?city=&cat=191&page=1',
    '4.Детска соба  \n': 'https://www.reklama5.mk/Search?city=&cat=192&page=1',
    '5.Кујна  \n': 'https://www.reklama5.mk/Search?city=&cat=193&page=1',
    '6.Садови и прибор  \n': 'https://www.reklama5.mk/Search?city=&cat=195&page=1',
    '7.Маси и столици -Трпезарии  \n': 'https://www.reklama5.mk/Search?city=&cat=196&page=1',
    '8.Бања / купатило  \n': 'https://www.reklama5.mk/Search?city=&cat=197&page=1',
    '9.Домашен текстил и Завеси  \n': 'https://www.reklama5.mk/Search?city=&cat=198&page=1',
    '10.Подна облога  \n': 'https://www.reklama5.mk/Search?city=&cat=199&page=1',
    '11.Полици и Места за складирање \n': 'https://www.reklama5.mk/Search?city=&cat=200&page=1',
    '12.Декорација и Украси  \n': 'https://www.reklama5.mk/Search?city=&cat=201&page=1',
    '13.Апарати за домаќинство  \n': 'https://www.reklama5.mk/Search?city=&cat=202&page=1',
    '14.Греење и климатизација  \n': 'https://www.reklama5.mk/Search?city=&cat=203&page=1',
    '15.Квалитет на Воздух  \n': 'https://www.reklama5.mk/Search?city=&cat=10057&page=1',
    '16.Соларни систeми и Опрема \n': 'https://www.reklama5.mk/Search?city=&cat=10142&page=1',
    '17.Светло и осветлување  \n': 'https://www.reklama5.mk/Search?city=&cat=204&page=1',
    '18.Cтруја и додатоци - Агрегати \n': 'https://www.reklama5.mk/Search?city=&cat=10012&page=1',
    '19.Градина  \n': 'https://www.reklama5.mk/Search?city=&cat=205&page=1',
    '20.Врати, Прозори и додатоци  \n': 'https://www.reklama5.mk/Search?city=&cat=206&page=1',
    '21.Безбедност и безбедносна опрема  \n': 'https://www.reklama5.mk/Search?city=&cat=207&page=1',
    '22.Домашни Алати и машини, Прибор  \n': 'https://www.reklama5.mk/Search?city=&cat=208&page=1',
    '23.Потреби за домаќинство  \n': 'https://www.reklama5.mk/Search?city=&cat=209&page=1',
    '24.Градежни материјали \n': 'https://www.reklama5.mk/Search?city=&cat=210&page=1',
    '25.Потрошни материјали  \n': 'https://www.reklama5.mk/Search?city=&cat=211&page=1',
    '26.Останато \n': 'https://www.reklama5.mk/Search?city=&cat=212&page=1'
},

5: {
    '1.Сите Мода и Облека и Обувки \n': 'https://www.reklama5.mk/Search?city=&cat=396&page=1',
    '2.Женска Облека \n': 'https://www.reklama5.mk/Search?city=&cat=397&page=1',
    '3.Машка Облека \n': 'https://www.reklama5.mk/Search?city=&cat=398&page=1',
    '4.Женски обувки \n': 'https://www.reklama5.mk/Search?city=&cat=399&page=1',
    '5.Машки обувки \n': 'https://www.reklama5.mk/Search?city=&cat=400&page=1',
    '6.Облека за момчиња \n': 'https://www.reklama5.mk/Search?city=&cat=401&page=1',
    '7.Облека за девојчиња \n': 'https://www.reklama5.mk/Search?city=&cat=402&page=1',
    '8.Обувки за момчиња \n': 'https://www.reklama5.mk/Search?city=&cat=403&page=1',
    '9.Обувки за девојчиња \n': 'https://www.reklama5.mk/Search?city=&cat=404&page=1',
    '10.Асесери / прибор  \n': 'https://www.reklama5.mk/Search?city=&cat=405&page=1',
    '11.Облека за трудници и додатоци  \n': 'https://www.reklama5.mk/Search?city=&cat=406&page=1',
    '12.Работна облека  \n': 'https://www.reklama5.mk/Search?city=&cat=407&page=1',
    '13.Останато \n': 'https://www.reklama5.mk/Search?city=&cat=408&page=1'
},

6: {
    '1.Сите Мобилни телефони и додатоци \n': 'https://www.reklama5.mk/Search?city=&cat=558&page=1',
    '2.Мобилни телефони \n': 'https://www.reklama5.mk/Search?city=&cat=559&page=1',
    '3.Додатоци за Мобилни телефони  \n': 'https://www.reklama5.mk/Search?city=&cat=560&page=1',
    '4.Паметни часовници - Smartwatch \n': 'https://www.reklama5.mk/Search?city=&cat=10004&page=1',
    '5.Фиксни телефони  \n': 'https://www.reklama5.mk/Search?city=&cat=561&page=1',
    '6.Факсови \n': 'https://www.reklama5.mk/Search?city=&cat=562&page=1',
    '7.Стари телефони \n': 'https://www.reklama5.mk/Search?city=&cat=10005&page=1',
    '8.Останато \n': 'https://www.reklama5.mk/Search?city=&cat=563&page=1'
},

7: {
    '1.Сите Компјутери \n': 'https://www.reklama5.mk/Search?city=&cat=580&page=1',
    '2.Десктоп компјутери \n': 'https://www.reklama5.mk/Search?city=&cat=581&page=1',
    '3.Лаптоп компјутери \n': 'https://www.reklama5.mk/Search?city=&cat=582&page=1',
    '4.Геминг и Дотатоци за Геминг  \n': 'https://www.reklama5.mk/Search?city=&cat=10111&page=1',
    '5.Таблети \n': 'https://www.reklama5.mk/Search?city=&cat=583&page=1',
    '6.Делови за Компјутери и додатоци  \n': 'https://www.reklama5.mk/Search?city=&cat=584&page=1',
    '7.Делови и опрема за Лаптопи  \n': 'https://www.reklama5.mk/Search?city=&cat=586&page=1',
    '8.Складирање меморија и медиумски додатоци \n': 'https://www.reklama5.mk/Search?city=&cat=10010&page=1',
    '9.Сервери и додатоци \n': 'https://www.reklama5.mk/Search?city=&cat=10011&page=1',
    '10.Mining Bitcoin Hardware \n': 'https://www.reklama5.mk/Search?city=&cat=10099&page=1',
    '11.Софтвери  \n': 'https://www.reklama5.mk/Search?city=&cat=585&page=1',
    '12.ПОС уреди \n': 'https://www.reklama5.mk/Search?city=&cat=587&page=1',
    '13.Останато \n': 'https://www.reklama5.mk/Search?city=&cat=588&page=1'
},

8: {
    '1.Сите ТВ, Видео, Фото и Мултимедија \n': 'https://www.reklama5.mk/Search?city=&cat=637&page=1',
    '2.Телевизори / LCD / Плазма \n': 'https://www.reklama5.mk/Search?city=&cat=638&page=1',
    '3.Дигитални фотоапарати \n': 'https://www.reklama5.mk/Search?city=&cat=640&page=1',
    '4.Галантерија за Фотоапарати  \n': 'https://www.reklama5.mk/Search?city=&cat=10124&page=1',
    '5.Hi-Fi / Аудио  \n': 'https://www.reklama5.mk/Search?city=&cat=641&page=1',
    '6.Домашно кино \n': 'https://www.reklama5.mk/Search?city=&cat=642&page=1',
    '7.DVD/HD/Видео/Blu-ray плеери  \n': 'https://www.reklama5.mk/Search?city=&cat=643&page=1',
    '8.Видео камери - Аналог  \n': 'https://www.reklama5.mk/Search?city=&cat=644&page=1',
    '9.Видео камери - Дигитални  \n': 'https://www.reklama5.mk/Search?city=&cat=645&page=1',
    '10.Дрон камери \n': 'https://www.reklama5.mk/Search?city=&cat=10001&page=1',
    '11.Сателитски антени и IPTV  \n': 'https://www.reklama5.mk/Search?city=&cat=646&page=1',
    '12.Играчки конзоли  \n': 'https://www.reklama5.mk/Search?city=&cat=647&page=1',
    '13.PC Игри и Видео игри  \n': 'https://www.reklama5.mk/Search?city=&cat=648&page=1',
    '14.МP3/4/5 плеери и iPod \n': 'https://www.reklama5.mk/Search?city=&cat=649&page=1',
    '15.Bluetooth уреди \n': 'https://www.reklama5.mk/Search?city=&cat=10003&page=1',
    '16.Паметни очила - Smart Glasses \n': 'https://www.reklama5.mk/Search?city=&cat=10002&page=1',
    '17.Фотокопири \n': 'https://www.reklama5.mk/Search?city=&cat=650&page=1',
    '18.GPS уреди \n': 'https://www.reklama5.mk/Search?city=&cat=651&page=1',
    '19.Безжична технологија \n': 'https://www.reklama5.mk/Search?city=&cat=652&page=1',
    '20.Далинси \n': 'https://www.reklama5.mk/Search?city=&cat=653&page=1',
    '21.Диктафони \n': 'https://www.reklama5.mk/Search?city=&cat=654&page=1',
    '22.Видео проектори и опрема \n': 'https://www.reklama5.mk/Search?city=&cat=655&page=1',
    '23.Електроника \n': 'https://www.reklama5.mk/Search?city=&cat=656&page=1',
    '24.Останато \n': 'https://www.reklama5.mk/Search?city=&cat=657&page=1'
},

9: {
    '1.Сите Музички инструменти и опрема \n': 'https://www.reklama5.mk/Search?city=&cat=753&page=1',
    '2.Музички инструменти  \n': 'https://www.reklama5.mk/Search?city=&cat=754&page=1',
    '3.Опрема за музички инструменти  \n': 'https://www.reklama5.mk/Search?city=&cat=755&page=1',
    '4.ДЈ Опрема \n': 'https://www.reklama5.mk/Search?city=&cat=756&page=1',
    '5.Аудио и видео продукција \n': 'https://www.reklama5.mk/Search?city=&cat=757&page=1',
    '6.Изнајмување \n': 'https://www.reklama5.mk/Search?city=&cat=758&page=1',
    '7.Останато \n': 'https://www.reklama5.mk/Search?city=&cat=759&page=1'
},

10: {
    '1.Сите Часовници и Накит \n': 'https://www.reklama5.mk/Search?city=&cat=776&page=1',
    '2.Накит  \n': 'https://www.reklama5.mk/Search?city=&cat=777&page=1',
    '3.Часовници  \n': 'https://www.reklama5.mk/Search?city=&cat=778&page=1',
    '4.Бижутерија \n': 'https://www.reklama5.mk/Search?city=&cat=779&page=1',
    '5.Останато \n': 'https://www.reklama5.mk/Search?city=&cat=780&page=1',
},

11: {
    '1.Сите Беби и Детски производи \n': 'https://www.reklama5.mk/Search?city=&cat=856&page=1',
    '2.Детска машка облека  \n': 'https://www.reklama5.mk/Search?city=&cat=857&page=1',
    '3.Детска женска облека  \n': 'https://www.reklama5.mk/Search?city=&cat=858&page=1',
    '4.Детски чевли Машки  \n': 'https://www.reklama5.mk/Search?city=&cat=859&page=1',
    '5.Детски чевли Женски  \n': 'https://www.reklama5.mk/Search?city=&cat=860&page=1',
    '6.Бебешка опрема  \n': 'https://www.reklama5.mk/Search?city=&cat=861&page=1',
    '7.Бебешка нега \n': 'https://www.reklama5.mk/Search?city=&cat=862&page=1',
    '8.Бебешка детска храна \n': 'https://www.reklama5.mk/Search?city=&cat=863&page=1',
    '9.Играчки и игри \n': 'https://www.reklama5.mk/Search?city=&cat=864&page=1',
    '10.Кукли - Фигури од Видео игри \n': 'https://www.reklama5.mk/Search?city=&cat=10021&page=1',
    '11.Градинки \n': 'https://www.reklama5.mk/Search?city=&cat=865&page=1',
    '12.Останато \n': 'https://www.reklama5.mk/Search?city=&cat=866&page=1',
},

12: {
    '1.Сите Здравје, Убавина додат. и опрема \n': 'https://www.reklama5.mk/Search?city=&cat=919&page=1',
    '2.Нега на лице \n': 'https://www.reklama5.mk/Search?city=&cat=920&page=1',
    '3.Нега на коса \n': 'https://www.reklama5.mk/Search?city=&cat=921&page=1',
    '4.Нега на тело \n': 'https://www.reklama5.mk/Search?city=&cat=922&page=1',
    '5.Ослабување и Исхрана \n': 'https://www.reklama5.mk/Search?city=&cat=923&page=1',
    '6.Женска козметика \n': 'https://www.reklama5.mk/Search?city=&cat=924&page=1',
    '7.Машка козметика \n': 'https://www.reklama5.mk/Search?city=&cat=925&page=1',
    '8.Шминка \n': 'https://www.reklama5.mk/Search?city=&cat=926&page=1',
    '9.Депилација и Производи за бричење  \n': 'https://www.reklama5.mk/Search?city=&cat=10067&page=1',
    '10.Маникир и педикир \n': 'https://www.reklama5.mk/Search?city=&cat=927&page=1',
    '11.Парфеми и мириси  \n': 'https://www.reklama5.mk/Search?city=&cat=928&page=1',
    '12.Масажа и Сауна \n': 'https://www.reklama5.mk/Search?city=&cat=929&page=1',
    '13.Заштита од сонце \n': 'https://www.reklama5.mk/Search?city=&cat=930&page=1',
    '14.Стоматолошка грижа \n': 'https://www.reklama5.mk/Search?city=&cat=931&page=1',
    '15.Управување со тежината \n': 'https://www.reklama5.mk/Search?city=&cat=932&page=1',
    '16.Алтернативна медицина \n': 'https://www.reklama5.mk/Search?city=&cat=933&page=1',
    '17.Благосостојба и Wellness \n': 'https://www.reklama5.mk/Search?city=&cat=934&page=1',
    '18.Детска козметика \n': 'https://www.reklama5.mk/Search?city=&cat=935&page=1',
    '19.Медицински материјали  \n': 'https://www.reklama5.mk/Search?city=&cat=936&page=1',
    '20.Оптички уреди  \n': 'https://www.reklama5.mk/Search?city=&cat=937&page=1',
    '21.Останато \n': 'https://www.reklama5.mk/Search?city=&cat=938&page=1',
},

13: {
    '1.Сите CD, DVD, VHS Музика, Филмови \n': 'https://www.reklama5.mk/Search?city=&cat=959&page=1',
    '2.Film & DVD / VHS  \n': 'https://www.reklama5.mk/Search?city=&cat=960&page=1',
    '3.Blu-ray \n': 'https://www.reklama5.mk/Search?city=&cat=10013&page=1',
    '4.3D Blu-ray \n': 'https://www.reklama5.mk/Search?city=&cat=10014&page=1',
    '5.4K Ultra HD Blu-ray \n': 'https://www.reklama5.mk/Search?city=&cat=10015&page=1',
    '6.Музика & CD  \n': 'https://www.reklama5.mk/Search?city=&cat=961&page=1',
    '7.Грамафонски плочи \n': 'https://www.reklama5.mk/Search?city=&cat=962&page=1',
    '8.Останато \n': 'https://www.reklama5.mk/Search?city=&cat=963&page=1',
},

14: 'https://www.reklama5.mk/Search?city=&cat=987&page=1',
15: 'https://www.reklama5.mk/Search?city=&cat=1019&page=1',
16: {
    '1.Сите Слободно време и хоби, Животни \n': 'https://www.reklama5.mk/Search?city=&cat=1032&page=1',
    '2.Велосипеди \n': 'https://www.reklama5.mk/Search?city=&cat=1033&page=1',
    '3.Делови за Велосипеди и додатоци  \n': 'https://www.reklama5.mk/Search?city=&cat=10029&page=1',
    '4.Ховерборд и додатоци \n': 'https://www.reklama5.mk/Search?city=&cat=10007&page=1',
    '5.Тротинети и додатоци \n': 'https://www.reklama5.mk/Search?city=&cat=10028&page=1',
    '6.Колекционерски предмети \n': 'https://www.reklama5.mk/Search?city=&cat=1034&page=1',
    '7.Сувенири и подароци \n': 'https://www.reklama5.mk/Search?city=&cat=1035&page=1',
    '8.Забавни игри и Играчки  \n': 'https://www.reklama5.mk/Search?city=&cat=1036&page=1',
    '9.Празнични украси \n': 'https://www.reklama5.mk/Search?city=&cat=1037&page=1',
    '10.Цигари и Прибор за пушење \n': 'https://www.reklama5.mk/Search?city=&cat=1038&page=1',
    '11.Животни  \n': 'https://www.reklama5.mk/Search?city=&cat=1039&page=1',
    '12.Oдгледување на растенија \n': 'https://www.reklama5.mk/Search?city=&cat=10008&page=1',
    '13.Oдгледување на животни \n': 'https://www.reklama5.mk/Search?city=&cat=10009&page=1',
    '14.Останато \n': 'https://www.reklama5.mk/Search?city=&cat=1040&page=1',
},

17: 'https://www.reklama5.mk/Search?city=&cat=1063&page=1',
18: 'https://www.reklama5.mk/Search?city=&cat=1193&page=1',
19: 'https://www.reklama5.mk/Search?city=&cat=1207&page=1',
20: 'https://www.reklama5.mk/Search?city=&cat=1235&page=1',
21: 'https://www.reklama5.mk/Search?city=&cat=1254&page=1',
22: 'https://www.reklama5.mk/Search?city=&cat=1255&page=1',
23: 'https://www.reklama5.mk/Search?city=&cat=1256&page=1',
24: 'https://www.reklama5.mk/Search?city=&cat=1257&page=1',
25: 'https://www.reklama5.mk/Search?city=&cat=1258&page=1',
26: 'https://www.reklama5.mk/Search?city=&cat=1259&page=1',
27: 'https://www.reklama5.mk/Search?city=&cat=1260&page=1'



}

def is_gui_active():
    try:
        import PySimpleGUI as sg
        if "window" in globals() and isinstance(globals()["window"], sg.Window):
            return True
    except ImportError:
        pass
    return False

def select_category():
    print("Избери категорија:")
    for i, (category, cat_id) in enumerate(katdict.items(), 1):
        print(f"{i}. {category}")
    
    primary_choice = int(input("Внеси број на категорија: "))
    primary_category = list(katdict.keys())[primary_choice - 1]
    primary_id = katdict[primary_category]
    
    print(f"\nИзбравте: {primary_category}")

    # Get the corresponding value from katdictx
    primary_value = katdictx.get(primary_id)
    return primary_category,primary_value
   

def select_sec_category(primary_category, primary_value):
    # If primary_value is a string, return it directly
    if isinstance(primary_value, str):
        print(f"URL: {primary_value}")
        return primary_category, primary_value

    # If it's a dictionary, allow selection of a secondary category
    elif isinstance(primary_value, dict):
        print("Избери подкатегорија:")
        for i, (subcategory, url) in enumerate(primary_value.items(), 1):
            print(f"{i}. {subcategory}")
        
        secondary_choice = int(input("Внеси број на подкатегорија: "))
        secondary_category = list(primary_value.keys())[secondary_choice - 1]
        secondary_url = primary_value[secondary_category]
        
        print(f"\Одбравте: {secondary_category}")
        print(f"URL: {secondary_url}")
        
        return secondary_category, secondary_url  # Return both category and URL

    else:
        print(f"Error: Unexpected type for '{primary_category}': {type(primary_value)}.")
        return None

def page_read(secondary_url, max_page):
    adid = []
    adlink = []
   
    for page in range(1, max_page + 1):  # Check the first 4 pages
        url = secondary_url + str(page)
        req = requests.get(url)
        
        if req.status_code == 200:
            soup = bs4.BeautifulSoup(req.text, 'html.parser')
            ads_on_page = soup.find_all('div', class_='ad-image-preview-table r5-slider')
            if not ads_on_page:
                print(f'Не се најдени реклами на страна {page}')
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
    # dava error u gui bez ovoj u threading
    if len(addate_element) > 2:
        addate = addate_element[2].find('span').text
    else:
        addate = "N/A"


    ad_info = {
        'adlink': adrequest,
        'adtitle': title.text.strip() if title else 'N/A',
        'adprice': price.text.replace('\r\n', '').strip() if price else 'N/A',
        'addate' : addate if addate else 'N/A', #vrakja i denes mozda bolje da konvertira denes u date today idk?
        'addesc' : addesc.text.strip() if addesc else 'N/A',

    }
    return ad_info

def keyword_search():
    #keyword input unti; user types 'exit'
    keywords = []
    while True:
        keyword = input('Внеси збор кој се бара или ! за излез: ')
        if keyword.lower() == '!':
            break
        keywords.append(keyword)
    
    return keywords

def search_ads_and_update_progress(ads, keywords, values=None):
    
    results = []

    if not ads:
        print("Нема реклами за пребарување." if not is_gui_active() else "No ads to search.")
        return results

    
    if is_gui_active():
        search_title = values.get("-TITLE-", False)
        search_desc = values.get("-DESC-", False)
        search_all = values.get("-ALL-", False)
    else:
        search_type = input('Барање по наслов на реклама (1), опис на реклама (2) или и двете (3)? ')
        search_title = search_type == '1'
        search_desc = search_type == '2'
        search_all = search_type == '3'

    if is_gui_active() and "window" in globals():
        window["-AD_PROGRESS-"].update(0, max=len(ads))

    for i, ad in enumerate(ads):
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

            if not is_gui_active():
                print(f"Наслов: {ad['adtitle']}")
                print(f"Датум: {ad['addate']}")
                print(f"Цена: {ad['adprice']}")
                print(f"Линк: {ad['adlink']}")
                print('---')

        if is_gui_active() and "window" in globals():
            window["-AD_PROGRESS-"].update(i + 1)

    return results

latin_to_macedonian = {
    'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е', 'zh': 'ж', 'z': 'з', 
    'i': 'и', 'j': 'ј', 'k': 'к', 'l': 'л', 'lj': 'љ', 'm': 'м', 'n': 'н', 'nj': 'њ', 
    'o': 'о', 'p': 'п', 'r': 'р', 's': 'с', 't': 'т', 'c': 'ц', 'ch': 'ч', 'dz': 'џ', 
    'sh': 'ш', 'u': 'у', 'f': 'ф', 'h': 'х', 'c': 'ц', 'y': 'у', 'e': 'е'
}


def transliterate_to_macedonian(text):
    """Convert a string from Latin to Macedonian Cyrillic."""
    sorted_keys = sorted(latin_to_macedonian.keys(), key=len, reverse=True)
    for key in sorted_keys:
        text = text.replace(key, latin_to_macedonian[key])
    return text


def print_results(results):
    """
    Prints the results of the search to the console.

    :param results: A list of dictionaries, each dictionary representing an ad
    """
    for ad in results:
        print(f"Title: {ad['adtitle']}")
        print(f"Date: {ad['addate']}")
        print(f"Price: {ad['adprice']}")
        print(f"Link: {ad['adlink']}")
        print('---')


def main():
    """
    Main function to run the Reklama5 scraper in command line mode.

    This function will select a category, select a secondary category, fetch ad links,
    fetch ad details, search for keywords in the fetched ads, and print the results.
    """
    global max_page
    ads = []  # List to store scraped ads

    # Category selection
    primary_category, primary_value = select_category()
    secondary_category, secondary_url = select_sec_category(primary_category, primary_value)
    
    try:
        max_page = int(input("Внеси број на страници: "))
    except ValueError:
        print("Грешка при внесување на бројот на страници.")
        max_page = 1

    # Fetch ads if secondary URL is valid
    if secondary_url:
        adlink = page_read(secondary_url, max_page)

        # Submit tasks to the executor
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            future_to_ad = {executor.submit(fetch_ad_details, adrequest): adrequest for adrequest in adlink}

            for future in concurrent.futures.as_completed(future_to_ad):
                try:
                    ad_info = future.result()
                    if ad_info:
                        ads.append(ad_info)  # Add to ads list
                except Exception as exc:
                    print(f'Ad request generated an exception: {exc}')

        executor.shutdown(wait=True)

    # Get keywords
    if is_gui_active():
        keywords = [keyword.strip().lower() for keyword in values["-KEYWORDS-"].split(",")]
    else:
        keywords = keyword_search()

    # Search ads
    results = search_ads_and_update_progress(ads, keywords, values=None)

    # Print results (if not using GUI)
    if not is_gui_active() and results:
        print_results(results)
    elif not results:
        print("Нема реклами кои одговараат на вашите критериуми.")


if __name__ == "__main__":
    main()