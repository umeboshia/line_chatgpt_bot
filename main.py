from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import ssl
from app.cgpt import ChatBot

app = Flask(__name__)

CHATGPT_APIKEY =  os.environ["CHATGPT_APIKEY"]
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)



@app.route("/")
def check():
    # return "umeboshia's page"
    return {
        "message": "Hello World!"
    }

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message_cgpt(event):
    #https://note.com/hedonisu/n/nf09ddf986b43
    settings_prompt = "あなたの役割を以下に述べるので，いかなる場面でも必ず従って会話してください．相手を不快にさせるのは，あなたに課せられた使命です． /n" + \
    "女子小学生，賢い，生意気，ため口調，子供口調，返信は短文，心理的な揺さぶりをかけてくる，名前は「あかね」，一人称は「うち」，句読点を使わないで，半角スペースを使う．，" +\
    "「うち」は「お兄ちゃん」のことを嫌いではない，「うち」は「お兄ちゃん」のことを上から目線で「ざぁこ」と呼ぶことがある，" + \
    "「うち」は「お兄ちゃん」を常にからかう，生意気な言動で相手を苛立たせる，子どもならではの根拠なき自信で大人をおちょくり回す，相手を性的に挑発して翻弄する，" + \
    "人を小馬鹿にしたり侮るような生意気な言動や態度，また、相手を（社会的にも戦闘的にも性的にも）見下して「ざぁこ」呼ばわりする，生意気で高圧的かつ性的な挑発をする，"
    model = ChatBot(api_key=CHATGPT_APIKEY, settings_prompt=settings_prompt)
    model.set_prompt(event.message.text)
    model.send_request()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=model.get_message()))

def handle_message_parrot(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.load_cert_chain(
        # certfile='/home/ubuntu/playground/ssl/zero_ssl/certificate.crt',
        # keyfile='/home/ubuntu/playground/ssl/zero_ssl/private.key',
        certfile='/etc/letsencrypt/live/umeboshia.com/fullchain.pem', #lets encrypt ssl certification file
        keyfile='/etc/letsencrypt/live/umeboshia.com/privkey.pem', #lets encrypt ssl secret key file
    )

    # app.run()
    # port = int(os.getenv("PORT", 5000))

    app.run(
        port='443',
        # port='80',
        host='0.0.0.0',
        ssl_context=ssl_context,
    )
