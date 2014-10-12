import urllib2
import json
import time
import sys
import utils
from glance import Glance
from keystone import Keystone
from cinder import Cinder
from quantum import Quantum
from nova import Nova
from ExceptionHandling.exceptions import *
from error_map import *

class Endpoint:
	nova     = None
	glance   = None
	keystone = None
	cinder   = None
	quantum  = None

class Login :
	_username = ""
	_password = ""
	_tenantId = ""
	_hostUrl  = "" 
	_token    = None    # token is generated in login method 
	jsonOfLogin = None
	
	def __init__(self, username, password, tenantId, ip, port = "5000"):
		self._hostUrl  = "http://" + ip + ":" + port + "/v2.0/tokens" 
		self._username = username 
		self._password = password
		self._tenantId = tenantId
	
	def _make_request(self, type, data, header, url):
		req = urllib2.Request(url)
		req.get_method = lambda : type 
		req.add_data( data )
		for k, v in header.items():
			req.add_header ( k, v )
		try :
			f    = urllib2.urlopen (req) #returns HTTP Error class object
			resp = f.read()
			return resp # if resp is JSON object then parse using json.loads in the caller method 
		except urllib2.HTTPError as e :
			data = e.read() #TBD : add to debugging msg
			errorCode = utils.find_error_code (data)
			if errorCode == None:
				raise OperationError (UNKNOWN_ERROR)
				sys.stderr.write("\nUnknown Error\n")
			else :
				raise OperationError(errorCode)
		except Exception as ee :
			sys.stderr.write("\n" + ee.read() + "\n")
			raise OperationError (UNKNOWN_ERROR)

	def post(self,data,header,url):
		try :
			resp = self._make_request( "POST", data, header , url) 
			return resp # return the post data response as it is the handling of response should be done in the caller method
		except OperationError as e:
			raise OperationError (e.err)
			
	def get(self, data, header, url):
		try :
			resp = self._make_request("GET", data, header, url )
			return resp
		except OperationError as e :
			raise OperationError (e.err)

	def delete(self, data, header, url):
		try :
			resp = self._make_request("DELETE", data, header, url)
			return resp
		except OperationError as e :
			raise OperationError (e.err)

	def put(self, data, header, url):
		try :
			resp = self._make_request("PUT", data, header, url)
			return resp
		except OperationError as e :
			raise OperationError (e.err)
	
	def login(self):
		loginData ={
                    "auth":
                           {
                            "passwordCredentials":
                             {
                                "username":  self._username  ,
                                "password":   self._password  
                              },
                             "tenantId":  self._tenantId 
                            }
                    }
		header = {'Content-Type' : 'application/json'}
		data   = json.dumps(loginData) # dict to str 
		try :
			loginResponse = self.post( data, header, self._hostUrl)
		except :
			raise OperationError(FAILED_TO_LOGIN)
		jsonData         = json.loads( loginResponse  )
		self._token      = jsonData['access']['token']['id'] 
		self.jsonOfLogin = jsonData
		sys.stderr.write("\n\tLogin successful\n\n") ##TBD:debugging msg
		self._tenantId = jsonData['access']['token']['tenant']['id']
		endPointObj   = self.populate_endpoint()
		return endPointObj

	def get_token(self) :
		return self._token

	def populate_endpoint(self):
		endPointObj = Endpoint()
		for module in self.jsonOfLogin['access']['serviceCatalog'] :
			if "glance" == module['name']: 
				glanceObj = Glance(self)
				glanceObj.set_endpoint_values(module['endpoints'][0]['adminURL'],module['endpoints'][0]['internalURL'],module['endpoints'][0]['publicURL'], module['endpoints'][0]['region'], module['endpoints'][0]['id'])
				endPointObj.glance = glanceObj
			if "nova" == module['name'] :
				novaObj = Nova()
				novaObj.set_endpoint_values(module['endpoints'][0]['adminURL'],module['endpoints'][0]['internalURL'],module['endpoints'][0]['publicURL'], module['endpoints'][0]['region'], module['endpoints'][0]['id'])
				endPointObj.nova = novaObj
			if "quantum" == module['name']:
				quantumObj = Quantum()
				quantumObj.set_endpoint_values(module['endpoints'][0]['adminURL'],module['endpoints'][0]['internalURL'],module['endpoints'][0]['publicURL'], module['endpoints'][0]['region'], module['endpoints'][0]['id'])
				endPointObj.quantum = quantumObj
			if "cinder" == module['name']:
				cinderObj = Cinder()
				cinderObj.set_endpoint_values(module['endpoints'][0]['adminURL'],module['endpoints'][0]['internalURL'],module['endpoints'][0]['publicURL'], module['endpoints'][0]['region'], module['endpoints'][0]['id'])
				endPointObj.cinder = cinderObj
			if "keystone" == module['name']:
				keystoneObj = Keystone()
				keystoneObj.set_endpoint_values(module['endpoints'][0]['adminURL'],module['endpoints'][0]['internalURL'],module['endpoints'][0]['publicURL'], module['endpoints'][0]['region'], module['endpoints'][0]['id'])
				endPointObj.keystone = keystoneObj
		return endPointObj
