# 子供bot

ChatGPTが子供になりきって会話してくれる

今後はプロンプトの種類を増やす予定

## 参考
- PythonでLine botを作ってみた（オウム返し部分）
  
  - https://qiita.com/kro/items/67f7510b36945eb9689b
  
## HOW TO USE

`execute_main.sh` を作成して実行してください．
LINEのチャンネルアクセストークン，APIキー，CatGPTのAPIキーが必要が必要です

```
export CHANNEL_ACCESS_TOKEN="***"
export CHANNEL_SECRET="***"
export CHATGPT_APIKEY="***"

python /home/ubuntu/playground/flask_playground/line_chatgpt_bot/main.py
``` 

## 使用例
![会話画像](https://drive.google.com/uc?export=view&id=1eVZ4IU0jNZCe_q11zyWwVyuvYSve5I_C)
