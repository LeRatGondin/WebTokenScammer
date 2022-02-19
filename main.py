import module_qrcode as qr
from flask import Flask,render_template,redirect, url_for,render_template
from colorama import Fore
from PIL import Image
import pathlib , os , pyngrok,json
from threading import Thread
import time

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
	app.run()