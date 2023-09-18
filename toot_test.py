import niji_schedule

keyword = input('> ',)

instanse = niji_schedule.niji_wiki(keyword, 'hieri')
text = instanse.get_schedule()

for i in text[0]:
    print(i)
    print('---')

for i in text[1]:
    print(i)
    print('---')