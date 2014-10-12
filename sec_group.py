import json
from classlogin import *
from nova import Nova
from error_map import *
from ExceptionHandling.exceptions import *

class SecurityGroupFunctions:
	reqUrl = None
	token = None
	createdGroupId = None
	url = None # get nova's public url 

	def create_security_group(self, logObj, tenantid, name, endPointObj):
		self.reqUrl = endPointObj.nova.publicUrl + "/os-security-groups"
		reqJson     = {
                        "security_group": 
                                         {
                                          "name"       : name,# this name should be passsed to launching the instance code , add json field of security group
                                          "description": "a security group"
                                         }
                       }
		header = {'X-Auth-Token': logObj.get_token(), 'Content-type': 'application/json'}
		data   = json.dumps(reqJson)
		try :
			resp2 = logObj.post(data, header, self.reqUrl)
			resp  = json.loads(resp2)
			self.createdGroupId = resp["security_group"]["id"]
			return self.createdGroupId 
		except OperationError, e :
			raise OperationError (FAILED_TO_CREATE_SECURITY_GROUP)
	
	def create_security_group_rule(self, fromPort, toPort, protocol, cidr, logObj, tenantid, parentGroupId, endPointObj):
		self.url  = endPointObj.nova.publicUrl + "/os-security-group-rules" 
		header    = {'X-Auth-Token': logObj.get_token(), 'Content-type': 'application/json'}
		reqJson   = {
                     "security_group_rule": 
                     {
                       "ip_protocol"  : protocol,
                       "from_port"    : fromPort,
					   "to_port"      : toPort,
					   "cidr"         : cidr,
                       "parent_group_id": parentGroupId
                      } 
					 }
	
		data = json.dumps(reqJson)
		try :
			resp = logObj.post(data, header, self.url)
		except OperationError as e :
			raise OperationError (FAILED_TO_CREATE_SECURITY_GROUP_RULE)

	def delete_security_group(self, logObj, tenantid, groupName, endPointObj):
		grpId    = None
		self.url = endPointObj.nova.publicUrl
		header   = {'X-Auth-Token': logObj.get_token(), 'Content-type': 'application/json'}
		
		try :
			getGroups = logObj.get ("", header, self.url + "/os-security-groups")
			data = json.loads(getGroups)
			for group in data ["security_groups"]:
				if group['name'] == groupName:
					grpId = group['id']
					break
			if grpId is None :
				raise OperationError(SECURITY_GROUP_DOESNT_EXIST)
				return 
		except OperationError , e :
			raise OperationError(SECURITY_GROUP_DOESNT_EXIST)

		try :
			logObj.delete("", header, self.url + "/os-security-groups/" + grpId )
			sys.stderr.write("Deleted this security group")
		except OperationError as e:
			raise OperationError (FAILED_TO_DELETE_SECURITY_GROUP) 
