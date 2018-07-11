#!/usr/bin/python
import urllib
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
import xmlrpclib
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import os
import random
import sys
import Adafruit_DHT

sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('usage: sudo ./Adafruit_DHT.py [11|22|2302] GPIOpin#')
    print('example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO #4')
    sys.exit(1)


humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)


if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)



class Custom_WP_XMLRPC:
	def post_article(self,wpUrl,wpUserName,wpPassword,articleTitle, articleCategories, articleContent, articleTags,PhotoUrl):
		self.path=os.getcwd()+"/00000001.jpg"
		self.articlePhotoUrl=PhotoUrl
		self.wpUrl=wpUrl
		self.wpUserName=wpUserName
		self.wpPassword=wpPassword
		#Download File
		f = open(self.path,'wb')
		f.write(urllib.urlopen(self.articlePhotoUrl).read())
		f.close()
		#Upload to WordPress
		client = Client(self.wpUrl,self.wpUserName,self.wpPassword)
		filename = self.path
		# prepare metadata
		data = {'name': 'picture.jpg','type': 'image/jpg',}
		
		# read the binary file and let the XMLRPC library encode it into base64
		with open(filename, 'rb') as img:
			data['bits'] = xmlrpc_client.Binary(img.read())
		response = client.call(media.UploadFile(data))
		attachment_id = response['id']
		#Post
		post = WordPressPost()
		post.title = articleTitle
		post.content = articleContent
		post.terms_names = { 'post_tag': articleTags,'category': articleCategories}
		post.post_status = 'publish'
		post.thumbnail = attachment_id
		post.id = client.call(posts.NewPost(post))
		print 'Post Successfully posted. Its Id is: ',post.id


ariclePhotoUrl='http://i1.tribune.com.pk/wp-content/uploads/2013/07/584065-twitter-1375197036-960-640x480.jpg' 
for XML Server
wpUrl='http://meteopi.ru/xmlrpc.php' 

wpUserName='admin'

wpPassword='password!'

articleTitle='Current weather'
articleContent=' "temperature": {}, "humidity": {}%'.format(temperature, humidity )
articleTags=['temp','humd'] 
articleCategories=['weather','temperature'] 
xmlrpc_object	=	Custom_WP_XMLRPC()
xmlrpc_object.post_article(wpUrl,wpUserName,wpPassword,articleTitle, articleCategories, articleContent, articleTags,ariclePhotoUrl)