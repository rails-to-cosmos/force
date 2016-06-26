# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


now = datetime.now()
prev_month = (now + relativedelta(months=-1)).replace(day=1)
next_month = (now + relativedelta(months=1)).replace(day=1)

testcases = {
    u'12.06.1975': datetime(day=12, month=6, year=1975),
    u'01.01.2015': datetime(day=1, month=1, year=2015),
    u'1 января': datetime(day=1, month=1, year=now.year),
    u'28 февраля': datetime(day=28, month=2, year=now.year),
    u'28 февраля 2015 года': datetime(day=28, month=2, year=2015),
    # u'позавчера': (now - relativedelta(hours=48), now - relativedelta(hours=49)),
    # u'вчера': (now - timedelta(hours=23), now - timedelta(hours=25)),
    # u'сегодня': (now - timedelta(hours=1), now + timedelta(hours=1)),
    # u'завтра': (now + timedelta(hours=23), now + timedelta(hours=25)),
    # u'послезавтра': now.day+2,
        u'через 2 часа': (now + timedelta(hours=1.9), now + timedelta(hours=2.1)),
    u'через 2  часа': (now + timedelta(hours=1.9), now + timedelta(hours=2.1)),
    u'через 5 минут': (now + timedelta(minutes=4), now + timedelta(minutes=6)),
    u'через 5     минут': (now + timedelta(minutes=4), now + timedelta(minutes=6)),
    u'через час': (now + timedelta(hours=0.9), now + timedelta(hours=1.1)),
    # u'через час и одну минуту': (now + timedelta(hours=1), now + timedelta(hours=1.1)),
        u'через час и 5 минут': (now + timedelta(hours=1), now + timedelta(hours=1.1)),
    u'через 2 ч': (now + timedelta(hours=1.9), now + timedelta(hours=2.1)),
    u'через 2 ч 50 мин': (now + timedelta(hours=2, minutes=49), now + timedelta(hours=2, minutes=51)),
    u'через 2 часа 30 минут': (now + timedelta(hours=2.4), now + timedelta(hours=2.6)),
    u'через 1 день': (now + timedelta(days=0.9), now + timedelta(days=1.1)),
    u'через 4 дня': (now + timedelta(days=3.9), now + timedelta(days=4.1)),
    u'через 5 дней': (now + timedelta(days=4.9), now + timedelta(days=5.1)),
    u'через 3 недели': (now + timedelta(weeks=2.9), now + timedelta(weeks=3.1)),
    # u'через неделю': (now + timedelta(weeks=0.9), now + timedelta(weeks=1.1)),
        u'2 ч назад': (now - timedelta(hours=2.1), now - timedelta(hours=1.9)),
    u'2 ч 50 мин назад': (now - timedelta(hours=2, minutes=51), now - timedelta(hours=2, minutes=49)),
    u'2 часа 30 минут назад': (now - timedelta(hours=2, minutes=31), now - timedelta(hours=2, minutes=29)),
    u'1 день назад': (now - timedelta(days=1.1), now - timedelta(days=0.9)),
    u'4 дня назад': (now - timedelta(days=4.1), now - timedelta(days=3.9)),
    u'5 дней назад': (now - timedelta(days=5.1), now - timedelta(days=4.9)),
    u'3 недели назад': (now - timedelta(weeks=3.1), now - timedelta(weeks=2.9)),
    u'12 часов': datetime(day=now.day, month=now.month, year=now.year, hour=12),
    u'1ч': datetime(day=now.day, month=now.month, year=now.year, hour=1),
    u'в 15:17': datetime(day=now.day, month=now.month, year=now.year, hour=15, minute=17),
    u'в19:26': datetime(day=now.day, month=now.month, year=now.year, hour=19, minute=26),
    u'2часа 53 минуты': (datetime(day=now.day, month=now.month, year=now.year, hour=2, minute=52),
                         datetime(day=now.day, month=now.month, year=now.year, hour=2, minute=54)),
    u'5 часов 20минут': datetime(day=now.day, month=now.month, year=now.year, hour=5, minute=20),
    u'14:10': datetime(day=now.day, month=now.month, year=now.year, hour=14, minute=10),
    u'14:10:31': datetime(day=now.day, month=now.month, year=now.year, hour=14, minute=10, second=31),
    u'в 10 часов 50 минут': datetime(day=now.day, month=now.month, year=now.year, hour=10, minute=50),
    u'через 2 года': (now + relativedelta(years=2) - relativedelta(hours=1),
                      now + relativedelta(years=2) + relativedelta(hours=1)),
    u'2 года назад': (now - relativedelta(years=2, hours=1),
                      now - relativedelta(years=2) + relativedelta(hours=1)),
    u'11:47 ДНК естественные и точные науки физика химия': datetime(day=now.day, month=now.month, year=now.year, hour=11, minute=47),
    u'Пт, 2017-02-22 13:25': datetime(day=22, month=2, year=2017, hour=13, minute=25),
    u'12.02.2016 15:12': datetime(day=12, month=2, year=2016, hour=15, minute=12),
    u'12.02.2016 5:12': datetime(day=12, month=2, year=2016, hour=5, minute=12),
    u'12.02.2016 в 15:12': datetime(day=12, month=2, year=2016, hour=15, minute=12),
    u'15:13 02/08/2014 ': datetime(day=2, month=8, year=2014, hour=15, minute=13),
    u'2015.11.03 15:29': datetime(day=3, month=11, year=2015, hour=15, minute=29),
    u'2015.11.03 15:29:31': datetime(day=3, month=11, year=2015, hour=15, minute=29, second=31),
    u'15:29:31 2015.11.03': datetime(day=3, month=11, year=2015, hour=15, minute=29, second=31),
    u'13/02/16': datetime(day=13, month=2, year=2016),
    u'30 12.2015': datetime(day=30, month=12, year=2015),
    u'30 12.15': datetime(day=30, month=12, year=2015),
    u'30.12.2015': datetime(day=30, month=12, year=2015),
    u'30.12.15': datetime(day=30, month=12, year=2015),
    u'05.02.2016 | 12:57:00': datetime(day=5, month=2, year=2016, hour=12, minute=57),
    u'1455280730': datetime.fromtimestamp(1455280730),
    u'Опубликовано: 05.11.15 в 9:40 Тест: 12': datetime(day=5, month=11, year=2015, hour=9, minute=40),
    u'Дата: 28-12-2015': datetime(day=28, month=12, year=2015),
    u'10.07.07, Москва, 17:56': datetime(day=10, month=07, year=2007, hour=17, minute=56),
    u'2013.02.28': datetime(day=28, month=2, year=2013),
    u'14:59, 17 Ноябрь 2015': datetime(day=17, month=11, year=2015, hour=14, minute=59),
    u'{0} {1}'.format(now.month, now.year): datetime(
        day=now.day,
        month=now.month,
        year=now.year
    ),
    u'{0} {1}'.format(prev_month.month, prev_month.year): datetime(
        day=(prev_month + relativedelta(months=1, days=-1)).day,
        month=prev_month.month,
        year=prev_month.year
    ),
    u'{0} {1}'.format(next_month.month, next_month.year): datetime(
        day=1,
        month=next_month.month,
        year=next_month.year
    ),
    u'13.11.2015 19.02.2016': datetime(day=13, month=11, year=2015),
    u'22 декабря 2015, 21:54 9 78 1441': datetime(day=22, month=12, year=2015, hour=21, minute=54),
    u'| 08:53 26 января 2016': datetime(day=26, month=1, year=2016, hour=8, minute=53),
    u'31 Март, 2014 - 18:36 31.03.2014 20:45': datetime(day=31, month=3, year=2014, hour=18, minute=36),
    u'14:47 16 февраля 2016': datetime(day=16, month=2, year=2016, hour=14, minute=47),


    # TODO: Переделать тесты с использованием unittest. Иметь возможность тестировать парсинг по кастомному формату даты.
    # u'!2015, 30 Декабрь': datetime(day=30, month=12, year=2015),   (?P<year>\d{4})\,\s+(?P<day>\d{2})\s+(?P<month>\d{2})

    u'19 июня, 2014' : datetime(day=19, month=6, year=2014),
    u'11:43 20 марта 2012': datetime(day=20, month=3, year=2012, hour=11, minute=43),
    u'10:15 15 Февраля 2016 г.': datetime(day=15, month=2, year=2016, hour=10, minute=15),
    u'23 Сентябрь, 2015 - 17:59': datetime(day=23, month=9, year=2015, hour=17, minute=59),
    u'Рубрика: 12 декабря 2015 Рубрика: 13 января 2015': datetime(day=12, month=12, year=2015),
    u'вторник, 16 февраля, 2016 - 17:53': datetime(day=16, month=2, year=2016, hour=17, minute=53),
    u'18 ФЕВРАЛЯ, 2016 // Интервью / Фестивали': datetime(day=18, month=2, year=2016),
    u'31 Март, 2014 - 18:36 31.03.2014': datetime(day=31, month=3, year=2014, hour=18, minute=36),
    u'22 января в 13:35 906 просмотров': datetime(day=22, month=1, year=now.year, hour=13, minute=35),
    u'22 января 13:35 906 просмотров': datetime(day=22, month=1, year=now.year, hour=13, minute=35),
    u'25 декабря 2015, 17:46': datetime(day=25, month=12, year=2015, hour=17, minute=46),
    u'Обзор Тойота Рав 4 25 августа 2011, 19:09': datetime(day=25, month=8, year=2011, hour=19, minute=9),
    u'17:04 16.02.16': datetime(day=16, month=2, year=2016, hour=17, minute=4),
    u'8 ноября `15, в 10:00 15 ноября, в 10:00': datetime(day=8, month=11, year=2015, hour=10),
    u'19 Фев, 2016': datetime(day=19, month=2, year=2016),
    u'18:09  19 февраля 2016': datetime(day=19, month=2, year=2016, hour=18, minute=9),
    u'Опубликовано: 19 февраля 2016 г. в 16:51 64 Нет комментариев 0': datetime(day=19, month=2, year=2016, hour=16, minute=51),
    u'2016-02-19t18:08:28': datetime(day=19, month=2, year=2016, hour=18, minute=8, second=28),
    u'19.02.2016,t18:08:28': datetime(day=19, month=2, year=2016, hour=18, minute=8, second=28),
    u'30 Июня, 2014 11:14': datetime(day=30, month=6, year=2014, hour=11, minute=14),
    u'30 Июня, 2014 11:14:28': datetime(day=30, month=6, year=2014, hour=11, minute=14, second=28),
    u'': now.replace(microsecond=0),
    u'8:47 25.01.16 Автор: nesluhi': datetime(day=25, month=1, year=2016, hour=8, minute=47),

    u'01 january 2016': datetime(day=1, month=1, year=2016),
    u'04 Jun 2015': datetime(day=4, month=6, year=2015),   # khabarovskonline.com
    u'Tuesday, 30 September 2014   "Первая полоса"': datetime(day=30, month=9, year=2014), # 1polosa.info

    # u'«Любовь в большом городе 3» (26.01.2016)': datetime(day=26, month=1, year=2016),
    # u'23-31 октября - Всероссийская неделя сбережений (22.10.2015)': datetime(day=22, month=10, year=2015),
    # u'Артём Левин готовится к очередной встрече с Саймоном Маркусом (27.01.2016)': datetime(day=27, month=1, year=2016),
    u'сегодня,': now.replace(microsecond=0),
    # u'полчаса назад': now.replace(microsecond=0),
    u'Вчера, 01:05 69': (now + relativedelta(days=-1)).replace(hour=1, minute=5, second=0, microsecond=0),
    # u'№ 19-20, 15 стр., 22 мая 2014'  http://sud.ua/newspaper/2014/05/22/64041-y-nenavisti--krovavij-tsvet
    # u'8 месяцев назад'
    # u'около 1 месяца назад'

    # u'Dec 14, 2012': datetime(day=14, month=12, year=2012),  # шаблон iksconsulting.ru
    # u'Новости Ассоциации July 13, 2015 01:30': datetime(day=13, month=7, year=2015, hour=1, minute=30),  # шаблон iksconsulting.ru
    #  Новости Ассоциации July 13, 2015 00:00   aakr.ru

    # u'0 часов назад': now.replace(microsecond=0),
    # u'полчаса назад': (now + relativedelta(minutes=-30)).replace(microsecond=0),

    # Фев, 20th, 2016   шаблон
    # Фев 20th, 2016   шаблон
    # u'23 ноября 18:38 2015 г. 23 ноября 18:38 2015 г. 23 ноября 18:41 23 ноября 18:49 23 ноября 19:01': datetime(day=23, month=11, year=2015, hour=18, minute=41),
    # (?P<day>\b\d{1,2}\b)\s+(?P<month>\b\d{1,2}\b)\s+(?P<hour>\b\d{1,2}\b)\:(?P<minute>\b\d{1,2}\b)\s+(?P<year>\b\d{4}\b)
}
