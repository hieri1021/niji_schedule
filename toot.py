from mastodon import Mastodon
import niji_schedule

keyword = input('> ',)

instanse = niji_schedule.niji_wiki(keyword)
text = instanse.get_schedule()
#print(text[1])

mastodon = Mastodon(
    client_id="app_key.txt", 
    access_token="user_key.txt", 
    api_base_url = "https://mstdn.soine.site")

mastodon.toot(text[0])
mastodon.toot(text[1])
