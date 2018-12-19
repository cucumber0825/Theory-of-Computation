import requests
import os

GRAPH_URL = "https://graph.facebook.com/v2.6"
#ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN = "EAAS1B71tqFcBAENZCOInwL4WfiVTP6LrV7FlraZAs023idJUBulrBTecMjtXjAZBRh0dDGQ7OyaboxHmEn4t4ZAXv1PSVDZC0n9wGjT6AZBPMMEpOL8L4ZCWgZAJuBHupWDcrMUQyjBfzQUc25gZC1qpkfQVmKqoAP3JCJGyMJQuvwyTdfciTVdwk"


def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)  #post = send

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response


def send_image_url(id, img_url):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message":{
            "attachment":{
                "type":"image", 
                "payload":{
                    "url":img_url
                }
            }
        }
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response
    #pass

def send_button_message(id, state):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    if(state == 4):
        payload = {
            "recipient": {"id": id},
            "message":{
                "attachment":{
                    "type":"template",
                    "payload":{
                        "template_type":"button",
                        "text":"Which do you want to visit?",
                        "buttons":[
                            {
                                "type":"web_url",
                                "url":"https://www.pornhub.com/",
                                "title":"Voicetube",
                                "webview_height_ratio": "full"
                            },
                            {
                                "type":"web_url",
                                "url":"https://www.youtube.com/",
                                "title":"Youtube",
                                "webview_height_ratio": "full"
                            }
                        ]
                    }
                }
            }
        }
    elif(state == 5):
        payload = {
            "recipient": {"id": id},
            "message":{
                "attachment":{
                    "type":"template",
                    "payload":{
                        "template_type":"button",
                        "text":"Which do you want to visit?",
                        "buttons":[
                            {
                                "type":"web_url",
                                "url":"https://www.ptt.cc/bbs/index.html",
                                "title":"PTT",
                                "webview_height_ratio": "full"
                            },
                            {
                                "type":"web_url",
                                "url":"https://www.instagram.com/?hl=zh-tw",
                                "title":"Instagram",
                                "webview_height_ratio": "full"
                            },
                            {
                                "type":"web_url",
                                "url":"https://www.dcard.tw/f",
                                "title":"Dcard",
                                "webview_height_ratio": "full"
                            }
                        ]
                    }
                }
            }
        }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response
    #pass

def send_audio_message(id,music):  #random send audio
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"open_graph",
                    "elements":[
                        {
                            "url":music 
                        }
                    ]
                }
            }
        }
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response
    #pass

def send_radio_message(id,radio):  #random send radio
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message":{
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"open_graph",
                    "elements":[
                        {
                            "url":radio   
                        }
                    ]
                }
            }
        }
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response
    #pass