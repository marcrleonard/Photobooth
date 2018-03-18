# import RPi.GPIO as GPIO
# import time
#
# butPin = 6 # Broadcom pin 17 (P1 pin 11)
#
# GPIO.setmode(GPIO.BCM) # Broadco
# GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# while True:
#	 output = GPIO.input(butPin)
#	 print(output)
#	 time.sleep(.1)

from tkinter import *
import threading
from time import sleep
import flickrapi
import flickrapi.shorturl
from twilio.rest import Client
import requests
import os
import xmltodict
import json
from time import sleep
import threading
import datetime
import glob
import shutil
import RPi.GPIO as GPIO


import flickrapi.sockutil

button_pin = 6
led_pin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(False)

GPIO.setup(led_pin,GPIO.OUT)


class Window(Frame):

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.init_window()

	#Creation of init_window
	def init_window(self):

		#twilio api
		self.account_sid = 'AC9fc5ddd0d2f0f09f3239c765791188ba'
		self.auth_token = '1401496bd9d480ad0f8999345e5475cf'

		self.api_key = '6dd63d0e6c60b2cf4ebf14ab4ba8870c'
		self.secret = '492ed2533f0fc70f'

		# changing the title of our master widget
		self.master.title("GUI")

		# allowing the widget to take the full space of the root window
		# self.pack(fill=BOTH, expand=1)

		self.master.grid_columnconfigure(0, weight=2)

		for row in range(5):
			self.master.grid_rowconfigure(row, weight=1)

		self.row0 = StringVar()
		self.row0_grid = Label(self.master, textvariable=self.row0, font=("Helvetica", 50, "bold"), bg='black', fg='white')


		self.row1 = StringVar()
		self.row1_grid = Label(self.master, textvariable=self.row1, font=("Helvetica", 40, "bold"), bg='black', fg='white')


		self.row2_entry = Entry(self.master)
		self.row2_entry.configure(bg='black', fg='white', highlightcolor='black', selectborderwidth=0, borderwidth=0, insertbackground='white', justify=CENTER, font=("Helvetica", 40, "bold"))


		self.row2_label = StringVar()
		self.row2_grid = Label(self.master, textvariable=self.row2_label, font=("Helvetica", 70, "bold"), bg='black', fg='white')


		self.row2_label_large = StringVar()
		self.row2_grid_large = Label(self.master, textvariable=self.row2_label_large, font=("Helvetica", 300, "bold"), bg='black',
		                       fg='white')


		self.row3 = StringVar()
		self.row3_grid = Label(self.master, textvariable=self.row3, font=("Helvetica", 40, "bold"), bg='black', fg='white')


		self.row4 = StringVar()
		self.row4_grid = Label(self.master, textvariable=self.row4, font=("Helvetica", 40, "bold"), bg='black', fg='white')


		run_thread = threading.Thread(target=self.main)
		run_thread.start()

	def upload_image(self, api_key, secret, filename):
		flickr = flickrapi.FlickrAPI(api_key=api_key, secret=secret,
									 token_cache_location='')
		# flickr.authenticate_via_browser(perms='write')
		resp = flickr.upload(filename=filename, format='rest')

		resp_dict = dict(xmltodict.parse(resp.decode('utf=8')))

		photo_id = resp_dict['rsp']['photoid']
		return photo_id

	def blink_led(self):
		self.blink_led = True
		while True:
			if self.blink_led:
				GPIO.output(led_pin, GPIO.HIGH)
				sleep(.5)
				GPIO.output(led_pin, GPIO.LOW)
				sleep(.5)

	def get_original_url(self, photo_id):
		url = (
		'https://api.flickr.com/services/rest/?&method=flickr.photos.getInfo&api_key={}&photo_id={}&format=json&nojsoncallback=1'.format(
			self.api_key, photo_id))
		resp = requests.get(url)
		resp_json = json.loads((resp.content).decode('utf-8'))

		server_id = resp_json['photo']['server']
		id = resp_json['photo']['id']
		farm_id = resp_json['photo']['farm']
		originalsecret = resp_json['photo']['originalsecret']

		url = 'https://farm{farm_id}.staticflickr.com/{server_id}/{id}_{originalsecret}_o.jpg'.format(farm_id=farm_id,
																									  server_id=server_id,
																									  id=id,
																									  originalsecret=originalsecret)
		return url

	def send_image_message(self, image_url, phone_number):

		client = Client(self.account_sid, self.auth_token)
		client.messages.create(
			to="+1{}".format(phone_number),
			from_="+14066624097 ",
			body='<3 you!\n  -Meghan and Marc',
			media_url=image_url,
		)

	def validate_number(self, number):
		validated = True
		msg = ''

		if isinstance(number, int):
			number = str(number)

		if '-' in number:
			number = ''.join(number.split('-'))

		if len(number) != 10:
			msg = "Not valid! 10 digit numbers only."
			validated = False

		return {'number': number, 'validated': validated, 'msg': msg}

	def hide_main(self):
		self.row0_grid.grid_remove()
		self.row1_grid.grid_remove()
		self.row2_entry.grid_remove()
		self.row3_grid.grid_remove()
		self.row4_grid.grid_remove()

	def show_main(self):
		self.row0_grid.grid_remove()
		self.row1_grid.grid_remove()
		self.row2_grid.grid(row=2, column=0)
		self.row3_grid.grid_remove()
		self.row4_grid.grid_remove()

	def main(self):
		try:

			os.system('pkill -f gvfs')
			os.system('pkill -f PTPCamera')

			blink_led_thread = threading.Thread(target=self.blink_led)
			blink_led_thread.start()


			GPIO.output(led_pin,GPIO.HIGH)



			while True:
				self.blink_led = True

				self.row0_grid.grid(row=0, column=0)
				self.row0.set('Welcome to the Photobooth!')

				self.row1_grid.grid(row=1, column=0)
				self.row1.set('1. Enter your phumber on the keypad!')

				self.row2_entry.focus_set()
				self.row2_entry.grid(row=2, column=0)

				self.row3_grid.grid(row=3, column=0)
				self.row3.set('2. Press the blinking red button!')

				self.row4_grid.grid(row=4, column=0)
				self.row4.set('3. Run back and pose for 3 photos!')

				while True:
					pin_output = GPIO.input(button_pin)
					if pin_output == 0:
						raw_phone_number = self.row2_entry.get()
						print(raw_phone_number)
						valid_return = self.validate_number(raw_phone_number)
						if valid_return['validated']:
							phone_number = valid_return['number']

							self.blink_led = False

							break

						else:
							continue
					sleep(.06)


				timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H%M%S')
				timestamp_folder = timestamp + '/'

				os.makedirs(timestamp_folder)

				#begin countdown
				self.hide_main()
				self.row2_grid_large.grid(row=2, column=0)
				self.row2_label_large.set('5')
				sleep(1)
				self.row2_label_large.set('4')
				sleep(1)
				self.row2_label_large.set('3')
				sleep(1)
				self.row2_label_large.set('2')
				sleep(1)
				self.row2_label_large.set('1')
				sleep(1)
				self.row2_grid_large.grid_forget()
				self.row2_grid.grid(row=2, column=0)
				self.row2_label.set('POSE!')
				sleep(1)

				GPIO.output(led_pin, GPIO.LOW)
				sleep(.2)
				GPIO.output(led_pin, GPIO.HIGH)
				sleep(.2)
				GPIO.output(led_pin, GPIO.LOW)

				os.system('gphoto2 --capture-image')
				sleep(1)

				GPIO.output(led_pin, GPIO.LOW)
				sleep(.2)
				GPIO.output(led_pin, GPIO.HIGH)
				sleep(.2)
				GPIO.output(led_pin, GPIO.LOW)

				os.system('gphoto2 --capture-image')
				sleep(1)

				GPIO.output(led_pin, GPIO.LOW)
				sleep(.2)
				GPIO.output(led_pin, GPIO.HIGH)
				sleep(.2)
				GPIO.output(led_pin, GPIO.LOW)

				os.system('gphoto2 --capture-image')

				self.row2_label.set('PROCESSING')
				os.system('gphoto2 --get-all-files')


				cwd = os.getcwd() + '/'

				print(cwd)
				all_images = glob.glob(cwd + '*.JPG')
				for image in all_images:
					print(image)
					shutil.move(image, timestamp_folder)

				print('done moving')

				new_location = glob.glob(cwd + timestamp_folder + '*.JPG')

				image_1 = new_location[0]
				image_2 = new_location[1]
				image_3 = new_location[2]

				final_image = timestamp_folder + 'final_' + timestamp + '.jpg'

				time_start = datetime.datetime.utcnow()
				call = 'convert ' + image_1 + ' '+ image_2 + ' ' + image_3 + ' -append -resize 50% -quality 60 ' + final_image
				os.system(call)
				time_end = datetime.datetime.utcnow()
				print('time: {}'.format((time_end - time_start).total_seconds()))

				time_start = datetime.datetime.utcnow()
				thumb = timestamp_folder + 'thumb.gif'
				call = 'convert ' + final_image + ' -resize 17% -fuzz 50 ' + thumb
				os.system(call)
				time_end = datetime.datetime.utcnow()

				print('time: {}'.format((time_end-time_start).total_seconds()))

				self.row2_label.set('TEXTING IMAGE...')

				photo = PhotoImage(file=thumb)
				label_photo = Label(image=photo)
				label_photo.image = photo  # keep a reference!
				label_photo.grid(row=3, column=0)

				# filename = '/Users/marcleonard/Desktop/banner copy.jpg'

				photo_id = self.upload_image(self.api_key, self.secret, final_image)
				print('Photoid: {}'.format(photo_id))
				url = self.get_original_url(photo_id)
				print('URL: {}'.format(url))
				self.send_image_message(url, phone_number)

				self.row2_label.set('SENT!')
				sleep(4)

				os.system('gphoto2 --delete-all-files --recurse')
				self.row2_grid.grid_forget()
				self.row2_entry.grid(row=2, column=0)
				self.row2_entry.delete(0, last=END)
				label_photo.grid_forget()

		except Exception as e:
			print(e)
			raise

		finally:
			GPIO.cleanup()







root = Tk()

#size of the window
root.geometry("1280x720")
root.configure(background='black')
app = Window(root)
root.mainloop()