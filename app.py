from bs4 import  BeautifulSoup
import random
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import time
import uuid
from selenium import webdriver
from threading import Thread
from flask_pymongo import PyMongo
import os



app = Flask(__name__)
CORS(app)
app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/test'
mongo = PyMongo(app)


bot_1_runnning = 1
bot_2_runnning = 1
bot_3_runnning = 1
bot_4_runnning = 1
bot_5_runnning = 1


bot = 0
driver_1 = None
fixed_bot = [1,2,3,4,5]
bots = []
free_bots = []

def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))


def selenium_google_results(keywords, tags, bot):
    if bot is 1:
        global bot_1_runnning 
        while bot_1_runnning is 1:
            kw = random.choice(keywords)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            global driver_1
            #driver_1 = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'/usr/lib/chromium-browser/chromedriver')
            driver_1 = webdriver.Chrome(chrome_options=chrome_options, executable_path= os.environ.get("CHROMEDRIVER_PATH"))

            google_url = "https://www.google.com/search?q=" + kw+ "&num=" + str(3)
            driver_1.get(google_url)
            time.sleep(2)
            soup = BeautifulSoup(driver_1.page_source,'lxml')
            result_div = soup.find_all('div', attrs={'class': 'g'})
            google_ads_div = soup.findAll('div', attrs={'class': 'uEierd'})
            ads_length = len(google_ads_div)
            items = []
            if ads_length >= 6:
                items = google_ads_div[0:3]
            
            if ads_length == 3:
                items = google_ads_div

            if ads_length < 3:
                items = google_ads_div

            for ads_link in items:
                if bot_1_runnning is 1:
                    link = ads_link.find('a', href=True)['href']
                    title = ads_link.find('a').contents[1].text
                    #l=driver_1.find_element_by_partial_link_text(title)
                    #l.click()
                    #time.sleep(1)
                    #driver_1.execute_script("window.history.go(-1)")
                    print(tags)
                    for tag in tags:
                        print(tag)
                        if tag in link:
                            print('found')
                        else:
                            print('not found')
                            try:
                                l=driver_1.find_element_by_partial_link_text(title)
                                l.click()
                                time.sleep(1)
                                driver_1.execute_script("window.history.go(-1)")
                            except Exception as e :
                                print(e)
                                continue
                else:
                    driver_1.quit()
                    break
            driver_1.close()


    if bot is 2:
        global bot_2_runnning 
        while bot_2_runnning is 1:
            kw = random.choice(keywords)
            chrome_options = webdriver.ChromeOptions()
            global driver_2
            driver_2 = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'/usr/lib/chromium-browser/chromedriver')
            google_url = "https://www.google.com/search?q=" + kw+ "&num=" + str(3)
            driver_2.get(google_url)
            time.sleep(2)
            soup = BeautifulSoup(driver_2.page_source,'lxml')
            result_div = soup.find_all('div', attrs={'class': 'g'})
            google_ads_div = soup.findAll('div', attrs={'class': 'uEierd'})
            ads_length = len(google_ads_div)
            items = []
            if ads_length >= 6:
                items = google_ads_div[0:3]
            
            if ads_length == 3:
                items = google_ads_div

            if ads_length < 3:
                items = google_ads_div

            for ads_link in items:
                if bot_2_runnning is 1:
                    link = ads_link.find('a', href=True)['href']
                    title = ads_link.find('a').contents[1].text
                    #l=driver_1.find_element_by_partial_link_text(title)
                    #l.click()
                    #time.sleep(1)
                    #driver_1.execute_script("window.history.go(-1)")
                    print(tags)
                    for tag in tags:
                        print(tag)
                        if tag in link:
                            print('found')
                        else:
                            print('not found')
                            try:
                                l=driver_2.find_element_by_partial_link_text(title)
                                l.click()
                                time.sleep(1)
                                driver_2.execute_script("window.history.go(-1)")
                            except Exception as e :
                                print(e)
                                continue
                else:
                    driver_2.quit()
                    break
            driver_2.close()
 
    

def manual_run(k,t,b):
    global bot
    if bot is 1:
        t_1 = Thread(target=selenium_google_results(keywords=k, tags=t, bot=b))
        t_1.start()
    if bot is 2:
        t_2 = Thread(target=selenium_google_results(keywords=k, tags=t, bot=b))
        t_2.start()
    if bot is 3:
        t_3 = Thread(target=selenium_google_results(keywords=k, tags=t, bot=b))
        t_3.start()
    if bot is 4:
        t_4 = Thread(target=selenium_google_results(keywords=k, tags=t, bot=b))
        t_4.start()
    if bot is 3:
        t_5 = Thread(target=selenium_google_results(keywords=k, tags=t, bot=b))
        t_5.start()
    return jsonify({'status': 200})


@app.route('/start', methods=['PUT'])
def start():
    data = request.json
    global bot
    global bots
    global fixed_bot
    global free_bots
    free_bots = Diff(fixed_bot,bots)

    if len(bots) < 5:
        bot = free_bots[0]
        bots.append(bot)
    else:
        return jsonify({'status': 401})
    free_bots = Diff(fixed_bot,bots)
    print(bots)
    print(free_bots)
    print('running bot = {}'.format(bot))
    if bot is 1:
        global bot_1_runnning
        bot_1_runnning = 1
    if bot is 2:
        global bot_2_runnning
        bot_2_runnning = 1


    k = uuid.uuid4().hex
    data['id'] = k
    data['bot'] = bot
    search = mongo.db.search
    search.insert(data)
    keywords = []
    tags = []
    keywords = data['keywords'].split('\n')
    tags = data['tags'].split(',')
    
    return Response(manual_run(keywords,tags, bot), mimetype="text/json")


@app.route('/restart', methods=['PUT'])
def restart():
    data = request.json
    global bot
    bot = data['bot']
    k = data['id']
    if bot is 1:
        global bot_1_runnning
        bot_1_runnning = 1
    if bot is 2:
        global bot_2_runnning
        bot_2_runnning = 1
    search = mongo.db.search
    search.update({'id': k},  {'$set': data}) 
    keywords = []
    tags = []
    keywords = data['keywords'].split('\n')
    tags = data['tags'].split(',')
    return Response(manual_run(keywords,tags, bot), mimetype="text/json")




@app.route('/stop', methods=['POST'])
def stop():
    data = request.json
    print(data)
    global bot 
    bot = data['bot']
    k = data['id']
    global bot_1_runnning
    global bot_2_runnning

    if bot is 1:
        bot_1_runnning = 0
        search = mongo.db.search
        search.update({'id': k},  {'$set': data}) 

    if bot is 2:
        bot_2_runnning = 0
        search = mongo.db.search
        search.update({'id': k},  {'$set': data}) 
        
    return 'ok'



@app.route('/search', methods=['GET'])
def get_all():
  search = mongo.db.search
  output = []
  for s in search.find():
    output.append({'active' : s['active'], 'bot': s['bot'], 'id': s['id'], 'label' : s['label'], 'keywords': s['keywords'], 'tags': s['tags'], 'createdAt': s['createdAt']})
  return jsonify(output)



@app.route('/delete', methods=['POST'])
def delete_one():
    data = request.json
    query = {'id': data['id']}
    search = mongo.db.search
    search.delete_one(query)
    return 'delete'




if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000, debug=True)



