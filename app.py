from bottle import route, run, request, abort, static_file
from bs4 import BeautifulSoup
from fsm import TocMachine
from fsm import all_img_urls
from fsm import music_urls
from fsm import author_songs
from fsm import popular_gossiping
from utils import send_text_message
from utils import send_image_url
from utils import send_radio_message

import requests
import time
import re
PTT_URL = 'https://www.ptt.cc'  #PTT mainpage
streetvoice_URL ='https://streetvoice.com'

articles = []
VERIFY_TOKEN = "870825"
machine = TocMachine(
    states=[
        'user','state0',
        'state1','state2',
        'state3','state4',
        'state5','state6',
        'state7','state8',
        'state9','state10',
        'state11'
    ],
    transitions=[
        { #user to 0
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state0',
            'conditions': 'is_going_to_state0'
        },
        { #user to 1
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state1',
            'conditions': 'is_going_to_state1'
        },
        { #user to 2
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state2',
            'conditions': 'is_going_to_state2'
        },
        { #user to 3
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state3',
            'conditions': 'is_going_to_state3'
        },
        { #1 to 4
            'trigger': 'advance',
            'source': 'state1',
            'dest': 'state4',
            'conditions': 'is_going_to_state4'
        },
        { #1 to 5
            'trigger': 'advance',
            'source': 'state1',
            'dest': 'state5',
            'conditions': 'is_going_to_state5'
        },
        { #4 to 11
            'trigger': 'advance',
            'source': 'state4',
            'dest': 'state11',
            'conditions': 'is_going_to_state11'
        },
        { # 5 to 11
            'trigger': 'advance',
            'source': 'state5',
            'dest': 'state11',
            'conditions': 'is_going_to_state11'
        },
        { # 2 to 6
            'trigger': 'advance',
            'source': 'state2',
            'dest': 'state6',
            'conditions': 'is_going_to_state6'
        },
        { #3 to 7
            'trigger': 'advance',
            'source': 'state3',
            'dest': 'state7',
            'conditions': 'is_going_to_state7'
        },
        { #3 to 8
            'trigger': 'advance',
            'source': 'state3',
            'dest': 'state8',
            'conditions': 'is_going_to_state8'
        },
        { #7 to 9
            'trigger': 'advance',
            'source': 'state7',
            'dest': 'state9',
            'conditions': 'is_going_to_state9'
        },
        { #8 to 10
            'trigger': 'advance',
            'source': 'state8',
            'dest': 'state10',
            'conditions': 'is_going_to_state10'
        },
        { # back edge
            'trigger': 'go_back',
            'source': [
                'state0',
                'state6',
                'state9',
                'state10',
                'state11'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)

@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)

@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        machine.advance(event)
        return 'OK'

@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')

def get_web_page(url):   #get all html
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text

def get_articles(dom, date):
    soup = BeautifulSoup(dom, 'html.parser')
    # 取得上一頁的連結
    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']

    articles = []  # 儲存取得的文章資料
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        if d.find('div', 'date').string.strip() == date:  # 發文日期正確
            # 取得推文數
            push_count = 0
            if d.find('div', 'nrec').string:
                try:
                    push_count = int(d.find('div', 'nrec').string)  # 轉換字串為數字
                except ValueError:  # 若轉換失敗，不做任何事，push_count 保持為 0
                    pass

            # 取得文章連結及標題
            if d.find('a'):  # 有超連結，表示文章存在，未被刪除
                href = d.find('a')['href']
                title = d.find('a').string
                articles.append({
                    'title': title,
                    'href': href,
                    'push_count': push_count
                })
    return articles, prev_url


def get_gossiping_article(dom, date):
    soup = BeautifulSoup(dom, 'html.parser')
    # 取得上一頁的連結
    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']
    yesterday = 0

    popular_gossiping = []  # 儲存取得的文章資料
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        dd = d.find('div', 'date').string.strip()
        if dd == date:  # 發文日期正確
            # 取得推文數
            push_count = 0
            if d.find('div', 'nrec').string:
                try:
                    if( d.find('div', 'nrec').string == "爆"):
                        push_count = 101
                except ValueError:  # 若轉換失敗，不做任何事，push_count 保持為 0
                    pass

            # 取得文章連結及標題
            if d.find('a'):  # 有超連結，表示文章存在，未被刪除
                if(push_count > 100):
                    href = d.find('a')['href']
                    title = d.find('a').string
                    popular_gossiping.append(title +"\n"+ PTT_URL +href)
        elif( int( dd[4] ) == int(date[4])-1 ):
            yesterday = 1

    return popular_gossiping, prev_url,yesterday

def parse(dom):   #search all picture's url
    soup = BeautifulSoup(dom, 'html.parser')
    links = soup.find(id='main-content').find_all('a')
    for link in links:
        if re.match(r'^https?://(i.)?(m.)?imgur.com', link['href']):
            all_img_urls.append(link['href'])    #add photo to list
    return all_img_urls   # store all photo url

def get_music(dom):
    soup = BeautifulSoup(dom, 'html.parser')
    paging_div = soup.find('table', 'table-song')
    divs = soup.find_all('h4')
    for d in divs:
        if d.find('a'):
            music_urls.append(streetvoice_URL + d.find('a')['href'])
    return

if __name__ == "__main__":
    #get streetvoice music
    streetvoice_page = get_web_page('https://streetvoice.com/music/charts/24hr/')
    get_music(streetvoice_page)
    print("the number of music",music_urls)
    # get gossiping articles
    gossiping_page = get_web_page(PTT_URL + '/bbs/Gossiping/index.html') #gossiping
    if gossiping_page:
        date = time.strftime("%m/%d").lstrip('0')  #time 08/25 PTT 8/25, date is today
        current_article, prev_url , yesterday = get_gossiping_article(gossiping_page, date)  # 目前頁面的今日文章
        while current_article or yesterday == 0:  #有今日文章則加入 articles
            popular_gossiping += current_article
            gossiping_page = get_web_page(PTT_URL + prev_url)
            current_article, prev_url,yesterday = get_gossiping_article(gossiping_page, date)  #recursive call

    print("the number of gossiping articles",popular_gossiping)

#begin search beauty
    current_page = get_web_page(PTT_URL + '/bbs/Beauty/index.html') #enter beauty
    if current_page:
        date = time.strftime("%m/%d").lstrip('0')  #time 08/25 PTT 8/25, date is today
        current_articles, prev_url = get_articles(current_page, date)  # 目前頁面的今日文章
        while current_articles:  #有今日文章則加入 articles
            articles += current_articles
            current_page = get_web_page(PTT_URL + prev_url)
            current_articles, prev_url = get_articles(current_page, date)  #recursive call
        # 已取得文章列表，開始進入各文章讀圖  
        for article in articles:
            page = get_web_page(PTT_URL + article['href'])  #enter each article
            if page:
                parse(page)
    print("stored photo number is",len(all_img_urls))

    #below is TA'code
    run(host="localhost", port=5000, debug=True, reloader=True)
