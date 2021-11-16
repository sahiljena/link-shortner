from flask import Flask, json, redirect, render_template, request, url_for, jsonify, abort
import pymongo
from bs4 import BeautifulSoup
import pymongo
import requests
import string
import random
import os
import socket
app = Flask(__name__)


# myclient = pymongo.MongoClient(os.environ.get('MONGO_SRV'))
srv = 'mongodb+srv://sahil:Sahil8139@cluster0.5qqak.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl_cert_reqs=CERT_NONE'
myclient = pymongo.MongoClient(srv)
mydb = myclient["URLShortner"]
mycol = mydb["urls"]

def get_num_of_clicks(url):
    x = mycol.find_one({'uid':url})
    clicks = x['cid']
    return clicks
def get_ip():
    hostname = socket.gethostname()   
    IPAddr = socket.gethostbyname(hostname)  
    return IPAddr 

def get_keywords(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    #head_parent = soup.find('head')
    #metas = head_parent.find_all('meta')
    description = soup.find("meta",{"name":"description"})
    try:
        keywords = soup.find("meta",{"name":"keywords"})
    except:
        keywords = ""
    title_og = soup.find("meta",  {"property":"og:title"})
    if not description:
        description = soup.find("meta",  {"property":"og:description"})
    image_og = soup.find("meta",  {"property":"og:image"})
    #print(title['content'])
    resp = {'description':'','keywords':'','title_og':'','image_og':''}
    try:
        resp['description'] = description['content']
    except:
        print("No description found...")
    try:
        resp['keywords'] = keywords['content']
    except:
        print("No keywords found...")
    try:
        resp['title_og'] = title_og['content']
    except:
        print("No title_og found...")
    try:
        resp['image_og'] = image_og['content']
    except:
        print("No image_og found...")
    return resp

@app.route('/track')
def track():
    q = request.args.get('q')
    if q:
        shortcode = q.split('/')
        print(shortcode)
        if shortcode[2] == "linnks.herokuapp.com":
            shortcode = shortcode[3]
            x = mycol.find_one({'uid':shortcode})
            longUrl = x['lurl']
            clicks = x['cid']
            dataCast = [[longUrl,clicks,shortcode]]
            return render_template('search.html',updates=1,dataCast=dataCast,Shortlink=q,error=0)
        else:
            return render_template('search.html',error=1,errorMessage="Please input a valid a url")
    else:
        return render_template('search.html')

@app.route('/<uid>')
def shorten(uid):
    try:
        x = mycol.find_one({'uid':uid})
        longUrl = x['lurl']
        description = x['description']
        title = x['title_og']
        image_og = x['image_og']
        clicks = x['cid']
        filter = { 'uid': uid }
        newvalues = { "$set": { 'cid': clicks+1 } }
        x = mycol.update_one(filter,newvalues)
        return render_template('redirect.html',error=0,message="",longurl=longUrl,description=description,title=title,image_og=image_og)
    except:
        return render_template('404.html')
    

@app.route('/')
def index():
    if request.args.get('url'):
        resp = get_keywords(request.args.get('url'))
        description = resp['description']
        image_og = resp['image_og']
        title_og = resp['title_og']
        keywords = resp['keywords']
        res = ''.join(random.choices(string.ascii_uppercase +string.digits, k = 6))
        data = {'lurl':request.args.get('url'),'image_og':image_og,'description':description,'title_og':title_og,'keywords':keywords,'uid':res,'cid':0,'ip':get_ip()}
        x = mycol.insert_one(data)
        return render_template('index.html',hasUpdates=1,shorturl=res)
    return render_template('index.html')

@app.errorhandler(404) 
def invalid_route(e): 
    return render_template('404.html')

@app.errorhandler(500) 
def invalid_route(e): 
    return render_template('500.html')
if __name__ == "__main__":
    app.run(debug=True)