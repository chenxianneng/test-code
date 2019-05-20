import requests
from lxml import etree
from urllib.request import urlretrieve
import time
from bs4 import  BeautifulSoup
from openpyxl import workbook
from openpyxl import load_workbook
import six
import pickle
import os

def run(username, password):
    catch_data = []

    catche_history = []
    if os.path.exists('catche_hsitory.p'):
        with open("catche_hsitory.p", "rb") as f:
            catche_history = pickle.load(f)

    headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    login_data = {
        'commit': 'Sign in',
        'utf8': '%E2%9C%93',
        'login': username,
        'password': password
    }

    with requests.Session() as session:
        url = "https://github.com/session"
        session_result = session.get(url, headers=headers)
        # soup = BeautifulSoup(r.content, 'html5lib')
        # session_html = etree.HTML(session_result.content)
        # session_list = session_html.xpath('//input[@name="authenticity_token"]')
        # if len(session_list) != 0:
        #     login_data['authenticity_token'] = session_list[0].text
        #     print(login_data['authenticity_token'])

        soup = BeautifulSoup(session_result.content, 'html5lib')
        login_data['authenticity_token'] = soup.find('input', attrs={'name': 'authenticity_token'})['value']
        print(login_data['authenticity_token'])

        r = session.post(url, data=login_data, headers=headers)
        # print(r.content)

        url = None
        count = 0
        url = 'https://github.com/WeBankFinTech/FATE/stargazers'
        while True:
            result = session.get(url)
            html = etree.HTML(result.content)

            user_list = html.xpath('//*[@class="follow-list-name"]/span/a')
            
            for user_name in user_list:
                if user_name.text in catche_history:
                    continue

                count += 1
                # print(item.text)
                user_page = 'https://github.com/' + user_name.text
                # print(user_page)
                user_page_result = session.get(user_page)
                user_page_html = etree.HTML(user_page_result.content)

                catche_history.append(user_name.text)

                email_list = user_page_html.xpath('//*[@class="u-email "]')
                # print(len(email_list))
                for email in email_list:
                    print(email.text, flush=True)
                    item = {}
                    item['username'] = user_name.text
                    item['email'] = email.text
                    catch_data.append(item)

                # time.sleep(1)    

            button_list = html.xpath('//div[@class="paginate-container"]/div/a')
            # print(len(button_list))

            have_next_page = False
            for button in button_list:
                if button.text == 'Next':
                    have_next_page = True
                    url = button.get('href')
                    print(url)

            if not have_next_page:
                with open("catche_hsitory.p", "wb") as f:
                    pickle.dump(catche_history, f)
                return catch_data

def save_excel(data):
    template_path = 'result.xlsx'
    w_workbook = load_workbook(template_path)
    sheets = w_workbook.sheetnames
    w_sheet = w_workbook[sheets[0]]

    write_row = 1
    for item in data:
        write_row += 1
        w_sheet.cell(row = write_row, column = 1).value = item['username']
        w_sheet.cell(row = write_row, column = 2).value = item['email']

    w_workbook.save('result.xlsx')

result = run('cxn8801@gmail.com', 'cxn8801cxn')
save_excel(result)