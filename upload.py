import sys
import json
from classlogin import Login
from nova import Nova
from image import Image
from glance import Glance
from error_map import *
from ExceptionHandling.exceptions import *

class Upload:
	xAuthToken     = None
	createdImageId = None
	flag           = 0
	logObj         = None
	endPointObj    = None
	tenantId       = None
	imagePath      = None
	imageName      = None
	containerFormat= None
	diskFormat     = None

	def __init__(self):
		try:
			username       = sys.argv[1]
			password       = sys.argv[2]
			self.tenantId  = sys.argv[3]
			self.imagePath = sys.argv[6]
			self.imageName = sys.argv[7]
			self.logObj    = Login(username, password, self.tenantId, sys.argv[4], sys.argv[5])
			try :
				self.containerFormat = sys.argv[8]
			except :
				sys.stderr.write("\n Container format not specified\n")
				exit(INVALID_ARGUMENTS)
			try :
				self.diskFormat = sys.argv[9]
			except:
				sys.stderr.write("\n disk format not specified\n")
				exit(INVALID_ARGUMENTS)
		except:
			sys.stderr.write( "\n uploads the image to openstack cloud\n")
			sys.stderr.write( "\n Usage : upload.py <username> <password> <tenantId> <login_url> <port> <imagePath> <imageName> <container-format> <disk-format>\n\n")
			raise InvalidArgumentsException(INVALID_ARGS_TO_UPLOAD)
			exit(INVALID_ARGS_TO_UPLOAD)
	
		try: 
			self.endPointObj = self.logObj.login() # generates a token and populateendpoints
			self.xAuthToken  = self.logObj.get_token()
			print str(self.endPointObj)
		except OperationError, e :
			sys.stderr.write( "\n" + str(e.err))
			exit(e.err)

def Uploadmain ():
	try :
		drive = Upload()
	except InvalidArgumentsException ,e:
		sys.stderr.write("\narguments error\n")
		return e.value
	glanceObj = Glance(drive.logObj)
	
	try :
		createdImageUrl = glanceObj.create_image(drive.logObj, drive.imageName, drive.endPointObj, drive.containerFormat, drive.diskFormat)
		print "Created Image Url: " + createdImageUrl # TBD : debugging message 
	except OperationError, e:
		sys.stderr.write( "\n" + str (e.err))
		return  (e.err)
	
	try:
		glanceObj.upload_image(drive.logObj, drive.imagePath)
	except OperationError, e:
		sys.stderr.write("\n" + str(e.err))
		return (e.err)
	return (0)

if "__main__" ==  __name__ :
	exit(Uploadmain())
