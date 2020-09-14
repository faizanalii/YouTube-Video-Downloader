from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtWinExtras import QWinTaskbarButton,QWinTaskbarProgress
from PyQt5.QtGui import *
import youtube_dl
from youtube_dl import YoutubeDL,extractor
import urllib
import time 
import math
from Downloader import *
class MyWindow(QMainWindow):
	def __init__(self):
		super(MyWindow,self).__init__()
		self.setStyleSheet('background-color:black;Background:black;color:white;')
		self.setWindowTitle('C Downloader')
		self.setWindowIcon(QtGui.QIcon('logo2.png'))
		self.taskbar=QWinTaskbarButton(self)
		self.taskbar.clearOverlayIcon()
		self.taskbar.overlayIcon()
		self.taskbar.setOverlayIcon(QIcon("icon.ico"))
		# Create the tray
		self.tray = QSystemTrayIcon()
		self.tray.setIcon(QIcon('icon.ico'))
		self.tray.setVisible(True)
		self.setGeometry(200,100,1280,720)
		self.initUI()
	def initUI(self):
		#Downloading Icon 
		self.label=QLabel(self)
		self.label.setPixmap(QtGui.QPixmap('icon.ico'))
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setStyleSheet('color:white;')
		self.label.setFont(QFont('Arial',20))
		self.label.resize(300,300)
		self.label.move(20,150)
		#URL Field
		self.urlfield=QLineEdit(self)
		self.urlfield.move(320,100)
		self.urlfield.setFont(QFont('Arial',15))
		self.urlfield.setStyleSheet('border:2px solid orange;border-radius:20px;background-color:black;color:white')
		self.urlfield.setFixedWidth(800)
		self.urlfield.setFixedHeight(40)
		self.urlfield.setAlignment(QtCore.Qt.AlignCenter)
		self.urlfield.setPlaceholderText('Enter URL')
		self.urlfield.setText('')	

		#Buttons
		self.button=QPushButton(self)
		self.button.setText('Proceed')
		self.button.setFont(QFont('Arial',12,QFont.Bold))
		self.button.setStyleSheet('color:white;border:2px solid orange;border-radius:20px;')
		self.button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button.move(1140,100)
		self.button.setFixedHeight(40)
		self.button.clicked.connect(self.click)
	
		#Format Buttons
		self.button4k=QPushButton(self)
		self.button1440=QPushButton(self)
		self.button1080=QPushButton(self)
		self.button720=QPushButton(self)
		self.button480=QPushButton(self)
		self.button360=QPushButton(self)
		self.button240=QPushButton(self)
		self.button144=QPushButton(self)
		self.buttonaudio=QPushButton(self)
		
		#Youtube DL 
		self.downloader=QYoutubeDL()
		self.progress_lbl=QLabel(self)
		self.progress_lbl.move(320,630)
		self.progress_lbl.setStyleSheet('color:white;')
		self.progress_lbl.setFont(QFont('Arial',10))
		self.progress_lbl.resize(520,15)
		self.download_pgb=QProgressBar(self)
		self.download_pgb.setGeometry(320,650,700,20)
		self.download_pgb.setStyleSheet('color:white;border:2px solid white;border-radius:10px;text-align:center;background-color:orange;')
		self.download_pgb.setFont(QFont('Arial',12))
		self.download_pgb.hide()
	#Checking URL
	def click(self):
		print(self.urlfield.text())
		if len(self.urlfield.text())>1:
			if 'youtube' in str(self.urlfield.text()) or 'youtu.be' in str(self.urlfield.text()):
				print("Youtube Link")
				if len(self.urlfield.text())>45:
					self.fromplaylist()
				else:
					self.format_selection()
			else:
				msg=QMessageBox(self)
				msg.setIcon(QMessageBox.Warning)
				msg.setText("Only YouTube links allowed")
				msg.setWindowTitle("Link Error")
				msg.show()
				print("Link Must be from Youtube ")
	def format_selection(self):
		self.extracting_info={}
		self.formats_list=[]
		if len(self.urlfield.text())>1:
			with youtube_dl.YoutubeDL(self.extracting_info) as ydl:
				self.info_get=ydl.extract_info('{}'.format(self.urlfield.text()),download=False)
				for i in range(len(self.info_get['formats'])):
					if self.info_get['formats'][i]['format_note'] in self.formats_list:
						continue
					else:
						self.formats_list.append(self.info_get['formats'][i]['format_note'])
						size=(self.info_get['formats'][i]['filesize'])/1000000.0
						if size>=1024.0:
							size=size/1024.0
							self.formats_list.append(str(math.ceil(size))+'GB')
						else:	
							self.formats_list.append(str(math.ceil(size))+'MB')
		else:
			print("None")
		print(self.formats_list)
		self.titlevideo()
		self.videothumbnail()
		self.videoformatslist()
	def fromplaylist(self):
		self.extracting_info={}
		self.formats_list=[]
		if len(self.urlfield.text())>1:
			with youtube_dl.YoutubeDL(self.extracting_info) as ydl:
				self.info_get=ydl.extract_info('{}'.format(str(self.urlfield.text()).split('&')[0]),download=False)
				for i in range(len(self.info_get['formats'])):
					if self.info_get['formats'][i]['format_note'] in self.formats_list:
						continue
					else:
						self.formats_list.append(self.info_get['formats'][i]['format_note'])
						size=(self.info_get['formats'][i]['filesize'])/1000000.0
						if size>=1024.0:
							size=size/1024.0
							self.formats_list.append(str(math.ceil(size))+'GB')
						else:	
							self.formats_list.append(str(math.ceil(size))+'MB')
		else:
			print("None")
		print(self.formats_list)
		self.titlevideo()
		self.videothumbnail()
		self.videoformatslist()

		#Title Of Video
	def titlevideo(self):
		self.title=QLabel(self)
		if len(self.info_get['title'])>72:
			self.info_get['title']=self.info_get['title'][0:72]+'...'
		else:
			self.info_get['title']=self.info_get['title']
		self.title.setText('{}'.format(self.info_get['title']))
		self.title.setStyleSheet('color:white;border-bottom:2px solid orange;')
		self.title.setFont(QFont('Arial',15))
		self.title.resize(700,50)
		self.title.move(320,550)
		self.title.show()
	#Video ThumbNail
	def videothumbnail(self):
		self.thumbnail_url=self.info_get['thumbnails'][0]['url'].split('?')[0]
		self.pic_data=urllib.request.urlopen(self.thumbnail_url).read()
		self.thumbnail_image=QtGui.QImage()
		self.thumbnail_image.loadFromData(self.pic_data)
		self.pic_label=QLabel(self)
		self.pic_label.setPixmap(QtGui.QPixmap(self.thumbnail_image))
		self.pic_label.setScaledContents(True)
		self.pic_label.resize(250,200)
		self.pic_label.move(320,330)
		self.pic_label.show()
	def videoformatslist(self):
		print(self.formats_list)
		for i in self.formats_list:
			if i=='tiny' or i=='mp3' or i=='webm' or i=='wav':
				self.size_index_audio=self.formats_list[self.formats_list.index(i)+1]
				self.Audio()
			elif i=='144p' or i=='144p60 HDR' or i=='144p60':
				self.size_index_144=self.formats_list[self.formats_list.index(i)+1]
				self.p144()
			elif i=='240p' or i=='240p60 HDR' or i=='240p60':
				self.size_index_240=self.formats_list[self.formats_list.index(i)+1]
				self.p240()
			elif i=='360p' or i=='360p60 HDR' or i=='360p60':
				self.size_index_360=self.formats_list[self.formats_list.index(i)+1]
				self.p360()
			elif i=='480p' or i=='480p60 HDR' or i=='480p60':
				self.size_index_480=self.formats_list[self.formats_list.index(i)+1]
				self.p480()
			elif i=='720p' or i=='720p60' or i=='720p60 HDR':
				self.size_index_720=self.formats_list[self.formats_list.index(i)+1]
				self.p720()
			elif i=='1080p' or i=='1080p60' or i=='1080p60 HDR':
				self.size_index_1080=self.formats_list[self.formats_list.index(i)+1]
				self.p1080()
			elif i=='1440p' or i=='1440p60' or i=='1440p60 HDR':
				self.size_index_1440=self.formats_list[self.formats_list.index(i)+1]
				self.p1440()
			elif i=='2160p' or i=='2160p60' or i=='2160p60 HDR':
				self.size_index_4k=self.formats_list[self.formats_list.index(i)+1]
				self.k4()
			else:
				print("Not Found")
	def k4(self):
		self.button4k.setText('4K {}'.format(self.size_index_4k))
		self.button4k.setFont(QFont('Arial',12,QFont.Bold))
		self.button4k.setFixedHeight(40)
		self.button4k.setFixedWidth(130)
		self.button4k.setStyleSheet('color:white;border:2px solid orange;border-radius:20px;')
		self.button4k.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button4k.move(320,200)
		self.button4k.show()
		self.button4k.clicked.connect(self.download4ks)
	def p1440(self):
		self.button1440.setText('1440p {}'.format(self.size_index_1440))
		self.button1440.setFont(QFont('Arial',12,QFont.Bold))
		self.button1440.setFixedHeight(40)
		self.button1440.setFixedWidth(130)
		self.button1440.setStyleSheet('color:white;border:2px solid orange;border-radius:20px;')
		self.button1440.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button1440.move(470,200)
		self.button1440.show()
		self.button1440.clicked.connect(self.download1440)
	def p1080(self):
		self.button1080.setText('1080p {}'.format(self.size_index_1080))
		self.button1080.setFont(QFont('Arial',12,QFont.Bold))
		self.button1080.setFixedHeight(40)
		self.button1080.setFixedWidth(130)
		self.button1080.setStyleSheet('color:white;border:2px solid orange;border-radius:20px;width:10px;')
		self.button1080.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button1080.move(620,200)
		self.button1080.show()
		self.button1080.clicked.connect(self.download1080)
	def p720(self):
		self.button720.setText('720p {}'.format(self.size_index_720))
		self.button720.setFont(QFont('Arial',12,QFont.Bold))
		self.button720.setFixedHeight(40)
		self.button720.setFixedWidth(130)
		self.button720.setStyleSheet('color:white;border:2px solid orange;border-radius:20px;')
		self.button720.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button720.move(770,200)
		self.button720.show()
		self.button720.clicked.connect(self.download720)
	def p480(self):
		self.button480.setText('480p {}'.format(self.size_index_480))
		self.button480.setFont(QFont('Arial',12,QFont.Bold))
		self.button480.setFixedHeight(40)
		self.button480.setFixedWidth(130)
		self.button480.setStyleSheet('color:white;border:2px solid orange;border-radius:20px;')
		self.button480.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button480.move(920,200)
		self.button480.show()
		self.button480.clicked.connect(self.download480)
	def p360(self):
		self.button360.setText('360p {}'.format(self.size_index_360))
		self.button360.setFont(QFont('Arial',12,QFont.Bold))
		self.button360.setFixedHeight(40)
		self.button360.setFixedWidth(130)
		self.button360.setStyleSheet('color:white;border:2px solid orange;border-radius:20px;')
		self.button360.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button360.move(1070,200)
		self.button360.show()
		self.button360.clicked.connect(self.download360)
	def p240(self):
		self.button240.setText('240p {}'.format(self.size_index_240))
		self.button240.setFont(QFont('Arial',12,QFont.Bold))
		self.button240.setFixedHeight(40)
		self.button240.setFixedWidth(130)
		self.button240.setStyleSheet('color:white;border:2px solid orange;border-radius:20px;')
		self.button240.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button240.move(320,270)
		self.button240.show()
		self.button240.clicked.connect(self.download240)
	def p144(self):
		self.button144.setText('144p {}'.format(self.size_index_144))
		self.button144.setFont(QFont('Arial',12,QFont.Bold))
		self.button144.setFixedHeight(40)
		self.button144.setFixedWidth(130)
		self.button144.setStyleSheet('color:white;border:2px solid orange;border-radius:20px;')
		self.button144.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.button144.move(470,270)
		self.button144.show()
		self.button144.clicked.connect(self.download144)
	def Audio(self):
		self.buttonaudio.setText('Audio {}'.format(self.size_index_audio))
		self.buttonaudio.setFont(QFont('Arial',12,QFont.Bold))
		self.buttonaudio.setFixedHeight(40)
		self.buttonaudio.setFixedWidth(130)
		self.buttonaudio.setStyleSheet('color:white;border:2px solid orange;border-radius:20px;')
		self.buttonaudio.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
		self.buttonaudio.move(620,270)
		self.buttonaudio.show()
		self.buttonaudio.clicked.connect(self.Audiomp3)


	#Downloading 
	def download4ks(self):
		self.url=self.urlfield.text()
		myhook=QHook()
		mylogger=QLogger()
		print("4k")
		options={'format':'bestvideo[height>1440]+bestaudio/best','noplaylist':True,'postprocessors':[{'key':'FFmpegMetadata'}]
		,'noprogress':True,'progress_hooks':[myhook],'logger':mylogger}
		self.downloader.download([self.urlfield.text()],options)
		myhook.infoChanged.connect(self._info_changed)
		self.download_pgb.show()
		self.download_pgb.setRange(0, 1)
	def download1440(self):
		self.url=self.urlfield.text()
		myhook=QHook()
		mylogger=QLogger()
		print("1440p")
		options={'format':'bestvideo[height=1440]+bestaudio/best','noplaylist':True,'postprocessors':[{'key':'FFmpegMetadata'}]
		,'noprogress':True,'progress_hooks':[myhook],'logger':mylogger}
		self.downloader.download([self.urlfield.text()],options)
		smyhook.infoChanged.connect(self._info_changed)
		self.download_pgb.show()
		self.download_pgb.setRange(0, 1)
	
	def download1080(self):
		self.url=self.urlfield.text()
		myhook=QHook()
		mylogger=QLogger()
		print("1080p")
		options={'format':'bestvideo[height=1080]+bestaudio/best','noplaylist':True,'merge_output_format':'mp4','postprocessors':[{'key':'FFmpegMetadata'}]
		,'noprogress':True,'progress_hooks':[myhook],'logger':mylogger}
		self.downloader.download([self.urlfield.text()],options)
		myhook.infoChanged.connect(self._info_changed)
		self.download_pgb.show()
		self.download_pgb.setRange(0, 1)
		
	def download720(self):
		self.url=self.urlfield.text()
		myhook=QHook()
		mylogger=QLogger()
		print("720p")
		options={'format':'bestvideo[height=720]+bestaudio/best','noplaylist':True,'postprocessors':[{'key':'FFmpegMetadata'}]
		,'noprogress':True,'progress_hooks':[myhook],'logger':mylogger}
		self.downloader.download([self.urlfield.text()],options)
		myhook.infoChanged.connect(self._info_changed)
		self.download_pgb.show()
		self.download_pgb.setRange(0, 1)

	def download480(self):
		self.url=self.urlfield.text()
		myhook=QHook()
		mylogger=QLogger()
		print("480p")
		options={'format':'bestvideo[height=480]+bestaudio/best','noplaylist':True,'postprocessors':[{'key':'FFmpegMetadata'}]
		,'noprogress':True,'progress_hooks':[myhook],'logger':mylogger}
		self.downloader.download([self.urlfield.text()],options)
		myhook.infoChanged.connect(self._info_changed)
		self.download_pgb.show()
		self.download_pgb.setRange(0, 1)

	def download360(self):
		self.url=self.urlfield.text()
		myhook=QHook()
		mylogger=QLogger()
		print("360p")
		options={'format':'bestvideo[height=360]+bestaudio/best','noplaylist':True,'postprocessors':[{'key':'FFmpegMetadata'}]
		,'noprogress':True,'progress_hooks':[myhook],'logger':mylogger}
		self.downloader.download([self.urlfield.text()],options)
		myhook.infoChanged.connect(self._info_changed)
		self.download_pgb.show()
		self.download_pgb.setRange(0, 1)

	def download240(self):
		self.url=self.urlfield.text()
		myhook=QHook()
		mylogger=QLogger()
		print("240p")
		options={'noprogress':True,'progress_hooks':[myhook],'logger':mylogger,'format':'bestvideo[height=240]+bestaudio/best'
		,'noplaylist':True,'postprocessors':[{'key':'FFmpegMetadata'}]}
		self.downloader.download([self.urlfield.text()],options)
		myhook.infoChanged.connect(self._info_changed)
		self.download_pgb.show()
		self.download_pgb.setRange(0, 1)

	def download144(self):
		self.url=self.urlfield.text()
		myhook=QHook()
		mylogger=QLogger()
		print("144p")
		options={'format':'bestvideo[height=144]+bestaudio/best','noplaylist':True,'postprocessors':[{'key':'FFmpegMetadata'}]
		,'noprogress':True,'progress_hooks':[myhook],'logger':mylogger}

		self.downloader.download([self.urlfield.text()],options)
		myhook.infoChanged.connect(self._info_changed)
		self.download_pgb.show()
		self.download_pgb.setRange(0, 1)
	def Audiomp3(self):
		self.url=self.urlfield.text()
		myhook=QHook()
		mylogger=QLogger()
		print("Audio")
		options={'format':'bestaudio','noplaylist':True,'postprocessors':[{'key':'FFmpegMetadata'}]
		,'noprogress':True,'progress_hooks':[myhook],'logger':mylogger}
		self.downloader.download([self.urlfield.text()],options)
		myhook.infoChanged.connect(self._info_changed)
		self.download_pgb.show()
		self.download_pgb.setRange(0, 1)
	def _info_changed(self,d):
		self.progress_lbl.show()
		if d['status']=='finished':
			self.progress_lbl.setText('Completed {}'.format(self.info_get['title']))
		if d['status']=='downloading':
			try:
				total = d["total_bytes"]
			except:
				total=d['total_bytes_estimate']

			downloaded = d["downloaded_bytes"]
			speed=d['speed']/1000
			elapsed=d['elapsed']
			if total>=1048576:
				total=total/1048576.0
				downloaded=downloaded/1048576.0
				self.progress_lbl.setText("Downloaded: {} MB of {} MB, Time Remaining: {}s, Speed: {} KiB/s"
					.format(round(downloaded,2), round(total,2),time.strftime('%Hh%Mm%S',time.gmtime(d['eta'])),round(speed,2)))
			self.download_pgb.setMaximum(total)
			self.download_pgb.setValue(downloaded)            				
if __name__=='__main__':
	app=QApplication(sys.argv)
	win=MyWindow()
	win.show()
	sys.exit(app.exec_())
