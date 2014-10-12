import json
import sys
from error_map import *
from ExceptionHandling.exceptions import *

class Nova:
	adminUrl        = None
	internalUrl     = None
	publicUrl       = None
	region          = None
	endPointId      = None
	endpoint        = None
	token           = None
	name            = "nova"
	flavorListJson  = None
	createdServerUrl= None # has tenantId in it .. used for performing start and stop
	createdServerId = None 

	def set_endpoint_values( self, adminUrl, internalUrl, publicUrl, region,endPointId ):
		self.adminUrl    = adminUrl
		self.internalUrl = internalUrl
		self.publicUrl   = publicUrl
		self.region      = region
		self.endPointId  = endPointId
		self.endpoint    = [ adminUrl, internalUrl, publicUrl, region, endPointId  ]

	def list_instances(self, logObj, instanceId):
	    #v2/{tenant_id}/servers
		self.token       = logObj.get_token()
		header           = {'X-Auth-Token': self.token, 'Content-type': 'application/json'}
		instanceListJson = logObj.get("", header, self.publicUrl + "/servers")
		data             = json.loads(instanceListJson)
		#JSON returns an array thats why  FOR loop 
		for server in data['servers']:
			if instanceId == server['id']:
				return server['links'][0]['href']
		raise OperationError (INSTANCE_NOT_FOUND) 
		''' this method returns url'''

	def list_flavor(self,logObj):
		self.token = logObj.get_token() 
		header     = {'X-Auth-Token': self.token, 'Content-type': 'application/json'}
		try :
			self.flavorListJson = logObj.get("",header,self.publicUrl + "/flavors")
		except :
			raise OperationError(FAILED_TO_LIST_IMAGES)
		
	def launch_server (self, logObj, createdImageUrl, tenantId, instanceName, flavor, securityGroupName):
		self.list_flavor(logObj)
		flavorName = flavor # choice is of user
		serverName = instanceName
		flavor     = json.loads(self.flavorListJson)
		try :
			for flavorData in flavor['flavors'] :
				if flavorData["name"]  == flavorName:
					flavorUrl  = flavorData["links"][0]["href"]
			imageUrl      = createdImageUrl 
			serverReqJson = {
                              "server" : {
                                           "name"      : serverName,
                                           "flavorRef" : flavorUrl,
                                           "imageRef"  : imageUrl,
								           "security_groups" : [{"name":securityGroupName}]		
                                         }
                             } 
			ser    = json.dumps(serverReqJson)
			header = {'X-Auth-Token': logObj.get_token(), 'Content-type': 'application/json'}
		except :
			raise OperationError (FLAVOR_NOT_FOUND)
		try :
			serverResp            = logObj.post(ser, header, self.publicUrl +  "/servers")
			serverRespData        = json.loads(serverResp)
			self.createdServerUrl = serverRespData['server']['links'][0]['href']
			self.createdServerId  = serverRespData['server']['id']
			return self.createdServerId
		except OperationError as  e:
			raise OperationError (e.err)
	
	def start(self, logObj, instanceUrl):
		header  = {'X-Auth-Token': logObj.get_token(), 'Content-type': 'application/json'}
		reqData =  json.dumps({'os-start': None})
		reqUrl  = instanceUrl + "/action"
		try:
			logObj.post(reqData, header, reqUrl)
			sys.stderr.write( "\n\tstart successful\n")
		except:
			raise OperationError(FAILED_TO_START)

	def stop(self, logObj, instanceUrl):
		header  = {'X-Auth-Token':logObj.get_token(), 'Content-type': 'application/json'}
		reqData =  json.dumps({'os-stop': None})
		reqUrl  = instanceUrl + "/action"
		try:
			logObj.post(reqData, header, reqUrl)
			sys.stderr.write( "\n\tstop successful\n")
		except:
			raise OperationError (FAILED_TO_STOP )
	
	def terminate (self, logObj, instanceUrl):
		header = {'X-Auth-Token': logObj.get_token(), 'Content-type': 'application/json'}
		reqUrl = instanceUrl
		try:
			logObj.delete("", header, reqUrl)
		except :
			raise OperationError ( FAILED_TO_TERMINATE  )

	def suspend (self, logObj, instanceUrl):
		header  = {'X-Auth-Token' :  logObj.get_token(), 'Content-type': 'application/json'}
		reqData =  json.dumps({'suspend': None})
		reqUrl  = instanceUrl + "/action"
		try:
			logObj.post(reqData, header, reqUrl)
		except:
			raise OperationError (FAILED_TO_SUSPEND)

	def resume (self, logObj, instanceUrl):
		header  = {'X-Auth-Token' : logObj.get_token(), 'Content-type' : 'application/json'}
		reqData =  json.dumps({'resume': None})
		reqUrl  = instanceUrl  + "/action"
		try:
			logObj.post(reqData, header, reqUrl)
		except:
			raise OperationError(FAILED_TO_RESUME)

	def get_power_state(self, logObj, instanceUrl):
		header = {'X-Auth-Token':logObj.get_token(), 'Content-type': 'application/json'}
		reqUrl = instanceUrl
		try :
			jsonResp = logObj.get("", header, reqUrl)
			data     = json.loads(jsonResp)
		except :
			raise OperationError( FAILED_TO_GET_POWER_STATE )
		try:
			powerState = data["server"]["OS-EXT-STS:power_state"]
			return powerState
		except KeyError as e :
			sys.stderr.write( str(e) + "\n" )

	def get_status(self, logObj, instanceUrl):
		header = {'X-Auth-Token': logObj.get_token(), 'Content-type': 'application/json'}
		reqUrl = instanceUrl
		try:
			jsonResp = logObj.get("", header, reqUrl)
			data     = json.loads(jsonResp)
		except :
			raise OperationError (FAILED_TO_GET_STATUS)
		try :
			status = data["server"]["OS-EXT-STS:vm_state"]
			return status
		except KeyError as e :
			sys.stderr.write( str(e) + "\n" )

	def hard_reboot(self, logObj, instanceUrl):
		header  = {'X-Auth-Token': logObj.get_token(), 'Content-type': 'application/json'}
		reqData =  json.dumps({'reboot':{"type":"HARD"}})
		reqUrl  = instanceUrl + "/action"
		try:
			logObj.post(reqData, header, reqUrl)
			sys.stderr.write("\n\thard reboot successful\n")
		except :
			raise OperationError (FAILED_TO_HARD_REBOOT)
		
	def soft_reboot(self, logObj, instanceUrl):
		header  = {'X-Auth-Token': logObj.get_token(), 'Content-type': 'application/json'}
		reqData =  json.dumps({'reboot':{"type":"SOFT"}})
		reqUrl  = instanceUrl  + "/action"
		try:
			logObj.post(reqData, header, reqUrl)
			sys.stderr.write( "\n\tsoft reboot successful\n")
		except :
			raise OperationError (FAILED_TO_SOFT_REBOOT)
