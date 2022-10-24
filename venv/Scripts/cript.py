import os

import uniq as uniq
from selenium import webdriver
from selenium.webdriver.common.by import By


def writing():
    path_to_chromedriver = r'C:\Users\home\Desktop\chromedriver.exe'
    browser = webdriver.Chrome(executable_path=path_to_chromedriver)
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
            #print("Номер страницы: ", i)
            element = browser.find_elements(By.CLASS_NAME, 'css-17wnpgm')
            for value in element:
                f.write(value.text + '\n')
                #print(value.text)
                count_name += 1
            page = browser.find_element(By.XPATH, '//button[@aria-label="Next page"]')
            page.click()
            i += 1
        #print(count_name)  # записать в текстовом формате
        count_nom += 1
        browser.close()
        path_to_chromedriver = r'C:\Users\home\Desktop\chromedriver.exe'
        browser = webdriver.Chrome(executable_path=path_to_chromedriver)
        url = 'https://www.binance.com/ru/markets'
        browser.get(url)
        nom += 1
    browser.close()


def uniq():
    with open('text.txt') as result:
        uniqlines = set(result.readlines())
        with open('nomination_new.txt', 'w') as rmdup:
            rmdup.writelines(set(uniqlines))


def checking():
    writing()
    uniq()
    data = [set(open(i).read().split()) for i in ('nomination.txt', 'nomination_new.txt')]
    diff = data[1].difference(data[0])
    if diff:
        print('А вот и новые монетки: ' + ', '.join(diff))
        return 'А вот и новые монетки: ' + ', '.join(diff)
    else:
        print('Новых монет пока нет:(')
        return 'Новых монет пока нет:('


def rename_file():
    os.remove('nomination.txt')
    os.rename('nomination_new.txt', 'nomination.txt')


#writing()
#uniq()
#checking()



