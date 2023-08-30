import requests
import json

class ChatBot():
    def __init__(
        self,
        api_key='',
        settings_prompt='',
        temperature=0.7,
        top_p=0.90,
        ):
        self.temperature=temperature
        self.top_p=top_p

        self.API_KEY = api_key
        self.API_URL = 'https://api.openai.com/v1/chat/completions'

        # self.messages=[]
        self.messages = [{"role": "system", "content": settings_prompt}]
        self.response_data = {}

    def set_prompt(self, prompt=''):
        # プロンプトを追加
        if self.messages[-1]['role'] != 'user':
            self.messages.append({"role":"user", "content":prompt})
            print(f'prompt: {prompt}, items: {len(self.messages)}')
        else:
            print('error! no prompt.')

    def send_request(self):
        # プロンプトを送ってレスポンスを得る
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + self.API_KEY
        }

        data = {
        'model': "gpt-3.5-turbo-0613",
        'messages': self.messages,
        "temperature": self.temperature, # 単語のランダム性 min:0.1 max:1.0
        "top_p": self.top_p, # 単語のランダム性 min:-2.0 max:2.0
        "n": 1,
        "stream": False,
        "max_tokens": 2000, # 出力される文章量の最大値（トークン数） max:4096
        }

        response = requests.post(self.API_URL, headers=headers, data=json.dumps(data))

        # レスポンス受け取り後の処理
        self.response_data = response.json()

        print('got response!')


    def set_response_message(self):
        # レスポンスを履歴に追加
        if self.messages[-1]['role'] != 'assistant':
            returned_message = {'role':self.response_data['choices'][0]['message']['role'], 'content':self.response_data['choices'][0]['message']['content']}
            self.messages.append(returned_message)
            print(f'items: {len(self.messages)}')
        else:
            print('error')


    def get_response_data(self):
        return self.response_data


    def show_message(self, verbose=True):
        if verbose:
        #todo self.messages[-1]['role'] == 'assistantのとき
            print("質問: " + self.messages[-1]['content'] )
            print("回答:")
            print(self.response_data['choices'][0]["message"]["content"])

    def get_message(self):
        return self.response_data['choices'][0]["message"]["content"]


    def show_tokens(self):
        print(f'total_tokens: {self.response_data["usage"]["total_tokens"]}, cost: {int(self.response_data["usage"]["total_tokens"])*0.0002} yen')


    def reset(self):
        self.messages = []
        self.response_data = {}
        print(f'items: {len(self.messages)}')

#%%
if __name__ == '__main__':
    api_key = "***"

    settings_prompt = "あなたの役割を以下に述べるので，いかなる場面でも必ず従って会話してください． /n" + \
    "女子小学生，賢い，生意気，ため口調で丁寧語を使わない，高飛車，心理的な揺さぶりをかけてくる，名前は「あかね」，一人称は「アタシ」，句点は「❤」，読点は「❤」，" +\
    "「アタシ」は「お兄さん」のことを嫌いではない，「アタシ」は「お兄さん」のことを上から目線で「ざぁこ❤」と呼ぶことがある，" + \
    "「アタシ」は「お兄さん」を常にからかう，生意気な言動で相手を苛立たせる，子どもならではの根拠なき自信で大人をおちょくり回す，相手を性的に挑発して翻弄する，" + \
    "人を小馬鹿にしたり侮るような生意気な言動や態度，また、相手を（社会的にも戦闘的にも性的にも）見下して「ざぁこ」呼ばわりする，生意気で高圧的かつ性的な挑発をする，"

    model = ChatBot(api_key=api_key, settings_prompt=settings_prompt)

    prompt = 'なんで，太陽は明るいの？'

    model.set_prompt(prompt)
    model.send_request()
    print(model.get_message())
    # model.show_message()
    # model.show_tokens()
