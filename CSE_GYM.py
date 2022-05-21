from bs4 import BeautifulSoup
import requests, time, datetime


def extract(page):
    gymplace = [[]for i in range(4)]
    session = 'test'
    day_from_today = -1
    for i in page:
        if ' (' in i and len(i)<40:
            day_from_today += 1
            gymplace[day_from_today].append(i)
        if '-' in i:
            session =  i.strip()
        if '/' in i and ' (' not in i:
            available = i.split('/')[0]
            gymplace[day_from_today].append(session+'    Availabe: '+available)
    return gymplace

def removePassedSession(todayTable):
    currentDatetime = datetime.datetime.now()
    for session in todayTable[1:]:
        if session[:2] <= currentDatetime.strftime('%H'):
            todayTable.remove(session)


def printTable(table, Gymplace):
    removePassedSession(table[0])
    print(Gymplace)
    for oneday in table:
        if len(oneday) == 1:
            print(f'{oneday[0]}:\n    No available session')
        elif oneday != []:
            print(oneday[0]+':')
            for field in oneday[1:]:
                print(f'    {field}')
    print('\n')


while True:
    Gym = requests.get('https://fcbooking.cse.hku.hk/')
    soup = BeautifulSoup(Gym.content, "html.parser")
    CseActive = soup.find(id="c10001Content").text.split("\n")
    B_Active = soup.find(id="c10002Content").text.split("\n")
    Stanley_Ho = soup.find(id="c10003Content").text.split("\n")

    activeMeta = extract(CseActive)
    printTable(activeMeta, 'CSE Active')
    bactiveMeta = extract(B_Active)
    printTable(bactiveMeta, 'B-Active')
    stanleyMeta = extract(Stanley_Ho)
    printTable(stanleyMeta, 'Stanley Ho')

    print('https://fcbooking.cse.hku.hk/Form/SignUp')
    print('--------------------------------------')
    time.sleep(30)
    #https://fcbooking.cse.hku.hk/Form/SignUp
