import json
from image import Image
import os
import sys
import thread
import time
from error_map import *
from ExceptionHandling.exceptions import *

class EnhancedFile(file):
	def __init__(self, *args, **keyws):
		file.__init__(self, *args, **keyws)
	def __len__(self):
		return int(os.fstat(self.fileno())[6])

class Glance:
	adminUrl    = None
	internalUrl = None
	publicUrl   = None
	region      = None
	endPointId  = None
	endpoint    = None
	name        = "glance"
	moduleNames = None
	image       = []
	createdImageId = None
	xAuthToken     = None
	flag = 0
	def __init__(self,logObj):
		self.xAuthToken = logObj.get_token()

	def set_endpoint_values( self, adminUrl, internalUrl, publicUrl, region, endPointId ):
		self.adminUrl    = adminUrl
		self.internalUrl = internalUrl
		self.publicUrl   = publicUrl
		self.region      = region
		self.endPointId  = endPointId
		self.endpoint    = [ adminUrl, internalUrl, publicUrl, region, endPointId  ]

	def populate_image_objects(self, imagesList):
		for image in imagesList['images']:
			imgObj          = Image()
			imgObj.listJson = image
			imgObj.id       = image ['id']
			imgObj.name     = image ['name']
			try:
				imgObj.imageType = image ['image_type']
			except KeyError:
				imgObj.imageType = "image"
			self.image.append(imgObj)

	def get_image_url (self, logObj, id, endPointObj):
		self.list_images(logObj, endPointObj)
		glanced = endPointObj.glance 
		self.xAuthToken = logObj.get_token()
		header = {'X-Auth-Token': self.xAuthToken}
		try:
			imagesListJson = logObj.get ("", header, glanced.publicUrl + "/images")
			imagesList     = json.loads(imagesListJson)
			for image in imagesList['images']:
				if id == image['id']:
					return (self.publicUrl + "/images/" + image["id"])
		except :
				raise OperationError(FAILED_TO_LIST_IMAGES)
		
	def list_images (self, logObj, endPointObj):
		glanced         = endPointObj.glance 
		self.xAuthToken = logObj.get_token()
		header          = {'X-Auth-Token': self.xAuthToken }
		try:
			imagesList     = logObj.get ("", header, glanced.publicUrl + "/images")
			self.publicUrl = glanced.publicUrl
			listImagesData = json.loads(imagesList)
			self.populate_image_objects(json.loads(imagesList))
		except :
			raise OperationError(FAILED_TO_LIST_IMAGES)

	def create_image(self, logObj, imageName, endPointObj, containerFormat, diskFormat ):
		self.list_images(logObj, endPointObj)
		header =  { 'X-Auth-Token': self.xAuthToken ,'Content-type': 'application/json'}
		
		createImageReq = {
                            'name': imageName,
                            'visibility' : "public", 
                            'container_format' : containerFormat,
                            'disk_format' : diskFormat
                         }
		try:
			createImageResp     = logObj.post(json.dumps(createImageReq), header, self.publicUrl + "/images")
			imageInfo           = json.loads( createImageResp )
			imgObj              = Image()
			imgObj.listJson     = imageInfo
			imgObj.id           = imageInfo['id']
			imgObj.name         = imageInfo['name']
			self.createdImageId = imgObj.id
			print "Image Id created: " + str (self.createdImageId) #TBD: debugging message
			return (self.publicUrl + "/images/" + self.createdImageId)
		except :
			raise OperationError(FAILED_TO_CREATE_IMAGE_ID)
		
	def thread_func(self,logObj):
		header =  {'X-Auth-Token':self.xAuthToken,'Content-Type': "application/json"}
		url = self.publicUrl + "/images" # + self.createdImageId
		while self.flag == 0 :
			sys.stderr.write("\nuploading... \n")##TBD: Debugging msg
			time.sleep(5)
		self.flag = 0

	def drive_thread(self,logObj) :
		try :
			thread.start_new_thread( self.thread_func,(logObj,))
		except :
			raise OperationError(THREAD_ERROR)

	def upload_image(self, logObj,imagePath):
		fileName = imagePath
		sys.stderr.write( "\nnow uploading... ")##TBD: Debugging msg
		try :
			header = {'X-Auth-Token' : self.xAuthToken,'Content-Type' : "application/octet-stream","Content-Length" : str(os.path.getsize(imagePath)) }
			fileData  = EnhancedFile(fileName, 'rb')
			self.drive_thread(logObj)
		except  :
			raise OperationError (IMAGE_FILE_DOES_NOT_EXIST_LOCALLY)
		try:
			response =logObj.put(fileData, header, self.publicUrl + "/images/" + self.createdImageId + "/file" )
			fileData.close()
			self.flag = 1
			sys.stderr.write("\n\tupload is successful\n\n")##TBD: Debugging msg
		except:
			raise OperationError(FAILED_TO_UPLOAD_IMAGE)
