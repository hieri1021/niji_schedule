import requests as req
import re
from bs4 import BeautifulSoup as bs

class niji_wiki:
    def __init__(self, keyword, username):
        self.url = "https://wikiwiki.jp/nijisanji/配信予定リスト"
        self.res = req.get(self.url)
        self.soup = bs(self.res.text, "html.parser")
        self.elems = self.soup.find_all("div", class_="minicalendar_viewer")
        self.date_list = self.soup.find_all("h3", class_=["date_holiday", "date_weekday", "date_weekend"])
        self.keyword = keyword
        self.username = username


    def create_text(self, num ,message):
        base_message = message
        print(self.username)
        length = len(message) + len(self.username) + 2
        index = 0
        message_list = [message]
        
        for i, elem in enumerate(self.elems[num:num+7]):
            count = 0
            elem2 = elem.select("li")
            date = self.date_list[i+num].get_text().split()

            date = f'{date[-1]}年 {date[-2][0:1]}月 {date[-3]}日\n'
            length += len(date)

            if length >= 500:
                length = len(date) + 1
                index += 1
                message_list.append('\n')
            
            message_list[index] += date
            #print(f'{date[-1]}年 {date[-2][0:1]}月 {date[-3]}日')

            for li in elem2:       
                text = li.get_text().split()
                check_text = ' '.join(text)

                if self.keyword.lower() in check_text.lower():
                    count += 1
                    href_stream = li.find('a', class_='ext', attrs={'href' : [re.compile('https://www.youtube.com/*'), re.compile('https://twitch.tv/*'), re.compile('https://live.nicovideo.jp/*')]})
                    href_twitter = li.find('a', class_='ext', attrs={'href' : re.compile('https://twitter.com/*')})
                    
                    if href_stream:
                        href = href_stream.get('href')
                        href = f'({href})'
                    elif not href_stream and href_twitter:
                        href = href_twitter.get('href')
                        href = f'({href})'
                    else:
                        href = ''

                    if text[1] == '他' or text[1] == '?' or text[1] == '？':
                        text = ' '.join(text)

                        specialChars = '他?？'
                        for specialChar in specialChars:
                            text = text.replace(specialChar, '')
                    else:
                        text = ' '.join(text)

                    length += len(text) + 32 # 32 → URL(25文字) + その他(7文字)
                    #print(len(text) + 32)
                    #print(f'    ・{text} {href}\n')
                    
                    if length <= 500:
                        message_list[index] += f'    ・{text} {href}\n'
                        #print(f'    ・{text} {href}')
                    else:
                        length = len(f'    ・{text} {href}\n') + 1
                        index += 1
                        message_list.append('\n')
                        
                        if count <= 1:
                            length += len(date)
                            message_list[index-1] = message_list[index-1][0:-len(date)]
                            message_list[index] += f'{date}    ・{text} {href}\n'
                        
                        else:
                            message_list[index] += f'    ・{text} {href}\n'
                
            if count == 0:
                message_list[index] = message_list[index][0:-len(date)]
        
        if message_list[index] == base_message:
            message_list[index] += '検索結果：キーワードに関する配信はありませんでした。\n'

        return message_list


    def get_schedule(self):

        message = f'\nkeyword : {self.keyword}\n-----過去の配信-----\n'
        message2 = f'\nkeyword : {self.keyword}\n-----今日以降の配信‐‐‐‐‐\n'

        message = self.create_text(7, message)
        message2 = self.create_text(0, message2)
        
        return message, message2