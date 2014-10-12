from classlogin import Login
from nova import Nova
from image import Image
from glance import Glance
import sys
import json
from ExceptionHandling.exceptions import *
from error_map import *
#from security_group_creation import Security_group
class Power:
	xAuthToken     = None
	createdImageId = None
	flag           = 0
	logObj         = None
	endPointObj    = None
	tenantId       = None
	imagePath      = None
	instanceId   = None
	def __init__(self):
		try:
			username        = sys.argv[1]
			password        = sys.argv[2]
			self.tenantId   = sys.argv[3]
			self.command    = sys.argv[6]
			self.instanceId = sys.argv[7]
			self.logObj     = Login(username, password, self.tenantId, sys.argv[4], sys.argv[5])
		except:
			sys.stderr.write( "\nuploads the image to openstack cloud")
			sys.stderr.write( "\n\n\t\tUsage : power_control.py <username> <password> <tenantId> <login ip> <port> <Command:terminate, stop, suspend, hardreboot, softreboot, start, <instance id>")
			exit(INVALID_ARGUMENTS)
		try :
			self.endPointObj = self.logObj.login() # generates a token and populateendpoints 
			self.xAuthToken  = self.logObj.get_token()
		except OperationError, e :
			sys.stderr.write( "\n" + str (e))
			exit (INVALID_ARGUMENTS)

def PCmain():
	powerObj = Power()
	nova     = powerObj.endPointObj.nova

	try :
		instanceUrl = nova.list_instances(powerObj.logObj, powerObj.instanceId)
	except OperationError as e :
		sys.stderr.write ("\n" + str(e) + "\n")
		return e.err

	try :
		if  "stop" ==  powerObj.command:
			nova.stop(powerObj.logObj, instanceUrl)
			sys.stderr.write( "\n\tstopped...\n")
		elif  "start" == powerObj.command:
			nova.start(powerObj.logObj,instanceUrl)
			sys.stderr.write( "\n\tstarted..\n")
		elif "terminate" == powerObj.command :
			nova.terminate(powerObj.logObj, instanceUrl)
			sys.stderr.write( "\n\tterminated..\n")
		elif "hardreboot" == powerObj.command :
			nova.hard_reboot(powerObj.logObj, instanceUrl)
			sys.stderr.write( "\n\thard rebooted..\n")
		elif "softreboot" == powerObj.command :
			nova.soft_reboot(powerObj.logObj, instanceUrl)
			sys.stderr.write( "\n\tsoft rebooted..\n")
		elif "suspend" == powerObj.command :
			nova.suspend(powerObj.logObj, instanceUrl)
			sys.stderr.write( "\n\tsuspended..\n")
		elif "resume" == powerObj.command :
			nova.resume(powerObj.logObj, instanceUrl)
			sys.stderr.write("\n\tresumed..\n")
		else : 
			sys.stderr.write("\n\t speciifed action is not supported \n")
			exit(INVALID_ARGUMENTS)	
	except OperationError as e :
		sys.stderr.write( str (e) + "\n")
		return e.err

if  "__main__" == __name__:
	exit (PCmain())
