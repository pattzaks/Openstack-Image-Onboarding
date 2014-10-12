from classlogin import Login
from nova import Nova
from image import Image
from glance import Glance
import sys
import json
from error_map import *
from ExceptionHandling.exceptions import *
#from security_group_creation import Security_group
class Launch:
	xAuthToken 	    = None
	createdImageId  = None
	flag 			= 0
	logObj 		    = None
	endPointObj	    = None
	tenantId        = None
	imagePath       = None
	instanceName    = None
	imageId         = None
	flavor          = None
	securityGroupName = None
	def __init__(self):
		try:
			username          = sys.argv[1]
			password          = sys.argv[2]
			self.tenantId     = sys.argv[3]
			self.logObj       = Login(username, password, self.tenantId, sys.argv[4], sys.argv[5])
			self.imageId      = sys.argv[6]
			self.instanceName = sys.argv[7]
			self.flavor	      = sys.argv[8]
			try :
				self.securityGroupName = sys.argv[9]
			except :
				self.securityGroupName = "default"
		except:
			sys.stderr.write("\nLaunches the instance in OpenStack cloud\n")
			sys.stderr.write("\nUsage : launch.py <username> <password> <tenantId> <login url> <port> <image-id> <user-defined-instance-name> <flavor> security-group\n")
			sys.stderr.write("\narguments error\n")
			exit(INVALID_ARGUMENTS)
		try:
			self.endPointObj = self.logObj.login() # generates a token and populateendpoints 
			self.xAuthToken  = self.logObj.get_token()
		except OperationError, e :
			sys.stderr.write( "\n" + str(e.err) + "\n")
			exit (e.err)

def Launchmain():	
	drive     = Launch()
	glanceObj = Glance(drive.logObj)
	choiceId  = drive.imageId
	try:
		imageUrl = glanceObj.get_image_url(drive.logObj, choiceId, drive.endPointObj)
	except OperationError, e :
		sys.stderr.write( "\n" + str (e) + "\n")
		return e.err	
	nova = drive.endPointObj.nova 
	if (imageUrl == None):
		sys.stderr.write("\nNo image exists for given image ID\n") #TBD
		return (IMAGE_NAME_NOT_FOUND)
	else:
		try :
			createdInstanceId = nova.launch_server(drive.logObj, imageUrl, drive.tenantId, drive.instanceName, drive.flavor, drive.securityGroupName)
			sys.stderr.write("\nlaunch successful\n")#TBD debugging message
			sys.stderr.write("\n" + "created instance Id: "+ str (createdInstanceId) + "\n\n")
		except OperationError as e :
			sys.stderr.write("\n" + str (e) + "\n")
			return e.err
	
if "__main__" == __name__:
	exit (Launchmain())
