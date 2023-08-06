from .components import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import speech_recognition as sr
import subprocess
import os
import urllib
from time import sleep
try:
	import pyaudio
except:
	raise Exception("Please install pyaudio with pip install pyaudio command. If this give you error, Download pyaudio from 'Unofficial python binaries' website and install manually")



class Recaptcha_Solver:
	"""
	Usage:
		solver = Recaptcha_Solver(driver, ffmpeg_path)
		solver.solve_recaptcha()
	How to use:
		1. Pass your webdriver variable in driver param
		2. Download ffmpeg depending your os
		3. Then add the ffmpeg folder to your OS PATH
		or Copy your ffmpeg path and pass it to ffmpeg_path param
	"""
	def __init__(self,driver,ffmpeg_path='ffmpeg',output=True):
		self.driver=driver
		self.mp3='captcha.mp3'
		self.wav='captcha.wav'
		self.ffmpeg_path=ffmpeg_path
		self.time_to_sleep_after_submit=3
		self.output=output

	def solve_recaptcha(self):
		iframe1=find_until_located(self.driver,By.XPATH,'//*[@title="reCAPTCHA"]')
		self.driver.switch_to.frame(iframe1)
		find_until_clicklable(self.driver,By.CLASS_NAME,'recaptcha-checkbox-border').click()
		self.driver.switch_to.default_content()
		iframe2=find_until_located(self.driver,By.XPATH,'//*[@title="recaptcha challenge expires in two minutes"]')
		self.driver.switch_to.frame(iframe2)
		find_until_clicklable(self.driver,By.ID,'recaptcha-audio-button').click()

		solved=False

		while not solved:
			try:
				if self.output==True:
					print('Solving Captcha...')
				audio_url=find_until_located(self.driver,By.CLASS_NAME,'rc-audiochallenge-tdownload-link').get_attribute('href')
				if self.output==True:
					print('Downloading Audio...')
				urllib.request.urlretrieve(audio_url, self.mp3)
				try:
					if self.output==True:
						print('Processing audio...')
					subprocess.call([self.ffmpeg_path, '-y', '-i', self.mp3, self.wav], stdout = subprocess.DEVNULL, stderr = subprocess.STDOUT)
				except:
					raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.ffmpeg_path,'Please download ffmpeg and pass ffmpeg path to "ffmpeg_path"')

				r=sr.Recognizer()

				def recognize_audio():
					with sr.AudioFile(self.wav) as source:
						r.adjust_for_ambient_noise(source)
						audio=r.listen(source)
						text=r.recognize_google(audio)
						return text

				recognized=False

				while not recognized:
					try:
						if self.output==True:
							print('Recognizing audio...')
						text=recognize_audio()
						recognized=True
					except:
						if self.output==True:
							print('Failed. Trying Again')
						pass

				os.remove(self.mp3)
				os.remove(self.wav)

				find_until_located(self.driver,By.ID,'audio-response').send_keys(text)
				find_until_clicklable(self.driver,By.ID,'recaptcha-verify-button').click()
				sleep(self.time_to_sleep_after_submit)
				msg=find_until_located(self.driver,By.CLASS_NAME,'rc-audiochallenge-error-message').text
				if msg!='':
					find_until_clicklable(self.driver,By.ID,'recaptcha-reload-button').click()
					if self.output==True:
						print('Failed. Trying Again')
					solved=False
				
				if self.output==True:
					print('Successfully Solved')
				self.driver.switch_to.default_content()
				solved=True
			except Exception as e:
				print('[ERROR]',e)
				pass