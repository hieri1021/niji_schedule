from mastodon import Mastodon, StreamListener
import niji_schedule as niji
import datetime
from time import sleep

class Stream(StreamListener):
    def __init__(self): #継承
        super(Stream, self).__init__()

    def on_notification(self,notif): #通知が来た時に呼び出されます
        if notif['type'] == 'mention': #通知の内容がリプライかチェック
            content = notif['status']['content'] #リプライの本体です
            id = notif['status']['account']['username']
            st = notif['status']
            notif_stream(content, st, id)


def notif_stream(content,st,id):
    index = -2

    while True:
        req = content.rsplit(">")[index].split("<")[0].strip() #リプライの本体から余分な情報を削ります
        if req != "":
            break
        index -= 1

    keyword = req

    try:
        instanse = niji.niji_wiki(keyword, id)
        resr,resr2 = instanse.get_schedule()
    except IndexError as Error: #データが未登録の場合はエラー吐かせて対応します
        resr = Error
    
    for message in reversed(resr):
        print(message)
        mastodon.status_reply(st, message, id, visibility='direct') #未収載

    if resr2:
        for message in reversed(resr2):
            print(message)
            mastodon.status_reply(st, message, id, visibility='direct') #未収載


def notif_past():
    notif = mastodon.notifications() #通知を取得
    count = 0

    while True:
        if notif[count]['type'] == 'mention':
            if notif[count]['status']['replies_count'] == 0: #リプライが既にされてないのかの確認
                content = notif[count]['status']['content']
                id = notif[count]['status']['account']['username']
                st = notif[count]['status']
                notif_stream(content, st, id)
                count += 1

            else:
                break

        else:
            count += 1
        

if __name__ == '__main__':
    
    mastodon = Mastodon(
    client_id = "app_key.txt",
    access_token = "user_key.txt",
    api_base_url = "https://mstdn.soine.site") #インスタンス

    notif_past()

    print('サーバーとの通信を開始します')

    while True:
        try:
            mastodon.stream_user(Stream()) #ストリームの起動

        except KeyboardInterrupt:
            print('終了します')
            break
        
        except Exception as e:
            time = datetime.datetime.now()

            print(f'{time}:サーバーが通信を停止しました')
            print(e)
            print('-----------------------------------------')
            
            sleep(30)
            
            notif_past()
