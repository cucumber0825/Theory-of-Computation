from transitions.extensions import GraphMachine
import random
from utils import send_text_message
from utils import send_image_url
from utils import send_button_message
from utils import send_audio_message
from utils import send_radio_message
from bs4 import BeautifulSoup
import requests

author_songs = []
all_img_urls = []  #beauty
music_urls = []
popular_gossiping = []
youtube_urls=[
        'https://www.youtube.com/watch?v=DiqLMkw9O8I',
        'https://www.youtube.com/watch?v=jgx-q0jYxwg',
        'https://www.youtube.com/watch?v=JfnQ8qtcDyQ',
        'https://www.youtube.com/watch?v=BRcudpJzy1I',
        'https://www.youtube.com/watch?v=ybfWYpYhTQQ',
        'https://www.youtube.com/watch?v=xqni-C0u-Lk',
        'https://www.youtube.com/watch?v=zbq0rYjizMU',
        'https://www.youtube.com/watch?v=51SOZjKuaaQ',
        'https://www.youtube.com/watch?v=LQOvngM7BRM',
        'https://www.youtube.com/watch?v=M6O5wwNEK30'
]
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )
    def is_going_to_state0(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'hi cucumber'
        return False
    def is_going_to_state1(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == 'button'
        return False
    def is_going_to_state2(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '抽妹子'
        return False
    def is_going_to_state3(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '來首音樂吧'
        return False
    def is_going_to_state4(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '影片'
        return False
    def is_going_to_state5(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '社群網站'
        return False
    def is_going_to_state6(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '對阿'
        return False
    def is_going_to_state7(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '影片'
        return False
    def is_going_to_state8(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '好聽'
        return False
    def is_going_to_state9(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '好阿'
        return False
    def is_going_to_state10(self, event):  #uncertained
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '好阿'
        return False
    def is_going_to_state11(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '好阿'
        return False
        

    def on_enter_state0(self, event):   # begin introduce
        print("I'm entering state0")
        sender_id = event['sender']['id']
        send_text_message(sender_id,"今天想做什麼?\n要來點~button~嗎?\n還是想要~抽妹子~?\n還是~來首音樂吧~")
        self.go_back()
    def on_exit_state0(self):
        print('Leaving state0')

    def on_enter_state1(self, event):  
        print("I'm entering state1")
        sender_id = event['sender']['id']
        send_text_message(sender_id,"你想看~影片~還是要~社群網站~?")
        self.advance()
    def on_exit_state1(self,event):
        print('Leaving state1')

    def on_enter_state2(self, event):  
        print("I'm entering state2")
        sender_id = event['sender']['id']
        if(len(all_img_urls) > 0):
            send_image_url(sender_id, random.choice(all_img_urls) )
        send_text_message(sender_id,"才一張你一定覺得不夠!")
        self.advance()
    def on_exit_state2(self,event):
        print('Leaving state2')

    def on_enter_state3(self, event):  
        print("I'm entering state3")
        sender_id = event['sender']['id']
        send_audio_message(sender_id, random.choice(music_urls) )
        send_text_message(sender_id,"你覺得~好聽~嗎\n還是你想看youtube~影片~?")
        self.advance()
    def on_exit_state3(self,event):
        print('Leaving state3')

    def on_enter_state4(self, event):  
        print("I'm entering state4")
        sender_id = event['sender']['id']
        responese = send_button_message(sender_id,4)
        send_text_message(sender_id,"還是你想看八卦版在討論什麼?")
        self.advance()
    def on_exit_state4(self,event):
        print('Leaving state4')

    def on_enter_state5(self, event):  
        print("I'm entering state5")
        sender_id = event['sender']['id']
        responese = send_button_message(sender_id,5)
        send_text_message(sender_id,"還是你想看八卦版在討論什麼?")
        self.advance()
    def on_exit_state5(self,event):
        print('Leaving state5')

    def on_enter_state6(self, event):  
        print("I'm entering state6")
        sender_id = event['sender']['id']
        send_image_url(sender_id, random.choice(all_img_urls) )
        send_image_url(sender_id, random.choice(all_img_urls) )
        send_image_url(sender_id, random.choice(all_img_urls) )
        send_text_message(sender_id,"看太多了換其他事做吧")
        self.go_back()
    def on_exit_state6(self):
        print('Leaving state6')

    def on_enter_state7(self, event): 
        print("I'm entering state7")
        sender_id = event['sender']['id']
        print(random.choice(youtube_urls))
        send_radio_message(sender_id, random.choice(youtube_urls) )
        send_text_message(sender_id,"想看其他youtube影片嗎?")
        self.advance()
    def on_exit_state7(self,event):
        print('Leaving state7')

    def on_enter_state8(self, event):  
        print("I'm entering state8")
        sender_id = event['sender']['id']
        send_text_message(sender_id,"很好聽齁我也這麼覺得!要不要再一首?")
        self.advance()
    def on_exit_state8(self,event):
        print('Leaving state8')

    def on_enter_state9(self, event):  
        print("I'm entering state9")
        sender_id = event['sender']['id']
        send_radio_message(sender_id, random.choice(youtube_urls) )
        self.go_back()
    def on_exit_state9(self):
        print('Leaving state9')

    def on_enter_state10(self, event):  #抽music
        print("I'm entering state10")
        sender_id = event['sender']['id']
        send_audio_message(sender_id, random.choice(music_urls) )
        send_text_message(sender_id,"聽了這麼多音樂，該換其他事情做了吧!")
        self.go_back()
    def on_exit_state10(self):
        print('Leaving state10')
    
    def on_enter_state11(self, event):  #抽music
        print("I'm entering state11")
        sender_id = event['sender']['id']
        send_text_message(sender_id,"這幾篇在八卦版討論熱烈!")
        if(len(popular_gossiping) > 6):
            for i in range(0,5):
                send_text_message(sender_id,random.choice(popular_gossiping))
        else:
            for i in range(0,len(popular_gossiping)):
                send_text_message(sender_id,random.choice(popular_gossiping))
        self.go_back()
    def on_exit_state11(self):
        print('Leaving state11')