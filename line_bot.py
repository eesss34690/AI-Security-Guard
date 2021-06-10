from linebot import LineBotApi
from linebot.models import (
    MessageEvent,
    TextSendMessage, TextMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    ImageSendMessage
)
import pyimgur
import http.client as httplib



url = "https://<YOUR OWN NGROK URL>.ngrok.io/smartsecuriy/callback"
CLIENT_ID = "<LINE BOT CLIENT ID>"
PATH = "./1.jpg" #A Filepath to an image on your computer"
title = "Uploaded with PyImgur"
users = ['YOUR USERLIST', '<APPEND LIKE THIS>']
line_bot_api = LineBotApi('<LINE BOT SECRET ID>')

#push message to one user
def send_message(num):
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    print(uploaded_image.title)
    print(uploaded_image.link)
    print(uploaded_image.type)

    line_bot_api.push_message(users[num], 
        TextSendMessage(text='訪客注意!請問是否准許進入'))
    message = ImageSendMessage(
        original_content_url=uploaded_image.link,
        preview_image_url=uploaded_image.link
    )
    line_bot_api.push_message(users[num], message)

    line_bot_api.push_message(  # 回復傳入的訊息文字
                            users[num],
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    title='Menu',
                                    text='請選擇是否進入',
                                    actions=[
                                        MessageTemplateAction(
                                            label='是',
                                            text='是'
                                        ),
                                        MessageTemplateAction(
                                            label='否',
                                            text='否'
                                        )
                                    ]
                                )
                            )
                        )

def receive(num):
    conn = httplib.HTTPConnection("<YOUR OWN NGROK WEBSITE>.ngrok.io")
    conn.request(method="GET",url=url) 
    response = conn.getresponse()
    print(response.read().decode())
    
    signature = conn.request.META['HTTP_X_LINE_SIGNATURE']
    body = conn.request.body.decode('utf-8')
 
    try:
        events = parser.parse(body, signature)  # 傳入的事件
    except InvalidSignatureError:
        return HttpResponseForbidden()
    except LineBotApiError:
        return HttpResponseBadRequest()
    
    return 1
