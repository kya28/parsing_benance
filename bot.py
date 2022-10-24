import os
import sys

from selenium.webdriver.chrome.service import Service

sys.path.append('/dist/bot/')

from selenium import webdriver
from selenium.webdriver.common.by import By
from telegram.ext import Updater, CommandHandler

import logging
import telegram

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

bot = telegram.Bot(token='2048881693:AAHTWGVj26XT_KIH3E5dNjuVAfweQKr1IiI')


def writing():
    browser = webdriver.Chrome(service=Service("C:\\Users\\home\\Desktop\\chromedriver.exe"))
    url = 'https://www.binance.com/ru/markets'
    browser.get(url)
    f = open('text.txt', 'w')
    nominations = browser.find_elements(By.CLASS_NAME, 'css-5do4ya')
    count_nomination = len(nominations)
    nom = 0
    count_nom = 0
    while nom <= count_nomination:
        nomination = browser.find_elements(By.CLASS_NAME, 'css-8vrl2p')
        nomination[count_nom].click()
        #print("Какая номинация: (пара): ", nom)
        pages = browser.find_elements(By.CLASS_NAME, 'css-hlqxzb')
        last_page = int(pages[-1].text)
        #print("Количество страниц: ", last_page)
        i = 1
        count_name = 0
        while i <= last_page:
            # print("Номер страницы: ", i)
            element = browser.find_elements(By.CLASS_NAME, 'css-17wnpgm')
            for value in element:
                f.write(value.text + '\n')
                # print(value.text)
                count_name += 1
            page = browser.find_element(By.XPATH, '//button[@aria-label="Next page"]')
            page.click()
            i += 1
        # print(count_name)  # записать в текстовом формате
        count_nom += 1
        browser.close()
        path_to_chromedriver = r'C:\Users\home\Desktop\chromedriver.exe'
        browser = webdriver.Chrome(executable_path=path_to_chromedriver)
        url = 'https://www.binance.com/ru/markets'
        browser.get(url)
        nom += 1
    browser.close()


def uniq_():
    with open('text.txt') as result:
        uniqlines = set(result.readlines())
        with open('nomination_new.txt', 'w') as rmdup:
            rmdup.writelines(set(uniqlines))


def checking():
    data = [set(open(i).read().split()) for i in ('nomination.txt', 'nomination_new.txt')]
    diff = data[1].difference(data[0])
    if diff:
        rename_file()
        print('А вот и новые монетки: ' + ', '.join(diff))
        return 'А вот и новые монетки: ' + ', '.join(diff)


def rename_file():
    os.remove('nomination.txt')
    os.rename('nomination_new.txt', 'nomination.txt')


def chat_id_uniq():
    with open('chat_id.txt') as result:
        uniqlines = set(result.readlines())
        with open('chat_id_uniq.txt', 'w') as rmdup:
            rmdup.writelines(set(uniqlines))


def start(update, context):
    f = open('chat_id.txt', 'a')
    chat_id = update.message.chat_id
    f.write(str(chat_id) + '\n')
    chat_id_uniq()
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Добро пожаловать в мир Новой монетки!")


def callback_minute(context):
    writing()
    uniq_()
    chat_ids = set(open('chat_id_uniq.txt').readlines())
    for chat_id in chat_ids:
        context.bot.send_message(chat_id=chat_id,
                                 text=checking())


def main():
    updater = Updater(token='2048881693:AAHTWGVj26XT_KIH3E5dNjuVAfweQKr1IiI', use_context=True)
    dp = updater.dispatcher
    updater.job_queue.run_repeating(callback_minute, interval=600, first=5)
    dp.add_handler(CommandHandler("start", start, pass_job_queue=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
