import json
from classlogin import *
from nova import Nova
import sys
from error_map import *
from ExceptionHandling.exceptions import *
from sec_group import *

class SecurityGroup:
	xAuthToken    = None
	createdImageId = None
	flag          = 0
	logObj        = None
	endPointObj   = None
	tenantId      = None
	portsCount    = None
	ports         = []
	action        = None
	flavor        = None
	name          = None
	tcpList       = None
	udpList       = None
	icmpList      = None
	tcpProtcol    = None
	udpProtocol   = None
	icmpProtocol  = None
	tcpFromPort   = []
	tcpToPort     = []
	tcpCidr       = []
	udpFromPort   = []
	udpToPort     = []
	udpCidr       = []
	icmpFromPort  = []
	icmpToPort    = []
	icmpCidr      = []
	usage         =  "\ncreates/deletes the security group to openstack cloud\n" + "\n\n\t\tUsage : security_group_operations.py <username> <password> <tenantId> <login ip> <port>  <action: create/delete> <name> [tcp::port,port,cidr:..] [udp::ports,port,cidr,..::][icmp::port, port, cidr,..:]  \n\n"
	def __init__(self):
		try:
			username      = sys.argv[1]
			password      = sys.argv[2]
			self.tenantId = sys.argv[3]
			self.logObj   = Login(username, password, self.tenantId, sys.argv[4], sys.argv[5])
			self.action   = sys.argv[6]
			self.name     = sys.argv[7]
			
			if "create" == self.action :
				count = 0 ;
				while (count < (len(sys.argv) - 8)):
					if "tcp::" in sys.argv[count + 8]:
						self.tcpList     = sys.argv[count + 8]
						self.tcpProtocol = 1
					elif "udp::" in sys.argv[count + 8]:
						self.udpList     = sys.argv[count + 8]
						self.udpProtocol = 1
					elif "icmp::" in sys.argv[count + 8]:
						self.icmpList     = sys.argv[count + 8]
						self.icmpProtocol = 1
					count = count + 1
 				
				self.fill_rules_list(self.tcpList, self.udpList, self.icmpList)
		
			elif "delete" == self.action  :
				pass
			else :
				sys.stderr.write( "\n\tinvalid action")
				exit(INVALID_ACTION)
					
		except Exception, e:
			sys.stderr.write("\n" + str (e))
			sys.stderr.write("\n" + self.usage)
			exit (INVALID_ARGUMENTS)
		try:
			self.endPointObj = self.logObj.login() # generates a token and populateendpoints 
			self.xAuthToken  = self.logObj.get_token()
		except OperationError, e :
			sys.stderr.write( "\n" + str (e))
			exit (e.err)

	def fill_rules_list(self, tcpData, udpData, icmpData):
		if 1 == self.tcpProtocol:
			tempData = tcpData[5:]
			tempData = tempData.split(':', tempData.count(':') + 1)
			count = 0
			while (count < len(tempData)):
				port = tempData[count].split(',', 3)
				self.tcpFromPort.append(port[0])
				self.tcpToPort.append(port[1])
				self.tcpCidr.append(port[2])
				count = count + 1

		if 1 == self.udpProtocol:
			tempData = udpData[5:]
			tempData = tempData.split(':', tempData.count(':') + 1)
			count = 0
			while (count < len(tempData)):
				port = tempData[count].split(',', 3)
				self.udpFromPort.append(port[0])
				self.udpToPort.append(port[1])
				self.udpCidr.append(port[2])
				count = count + 1

		if 1 == self.icmpProtocol:
			tempData = icmpData[6:]
			tempData = tempData.split(':', tempData.count(':') + 1)
			count = 0
			while (count < len(tempData)):
				port = tempData[count].split(',', 3)
				self.icmpFromPort.append(port[0])
				self.icmpToPort.append(port[1])
				self.icmpCidr.append(port[2])
				count = count + 1

def SGmain(): 
	obj = SecurityGroup()
	createDelete = SecurityGroupFunctions() 
	if "create" == obj.action  :
		try :
			parentGroupId = createDelete.create_security_group( obj.logObj, obj.tenantId, obj.name, obj.endPointObj)
			sys.stderr.write( "\n\nsucessfully created group with Id: " + parentGroupId + "\n\n") #TBD : debugging msg
			
			if 1 == obj.tcpProtocol:
				count = 0
				while (count < len(obj.tcpToPort)) :
					createDelete.create_security_group_rule( obj.tcpFromPort[count],  obj.tcpToPort[count], "tcp", obj.tcpCidr[count], obj.logObj, obj.tenantId, parentGroupId, obj.endPointObj )
					count = count + 1
			
			if 1 == obj.udpProtocol:
				count = 0
				while (count < len (obj.udpToPort)):
					createDelete.create_security_group_rule( obj.udpFromPort[count], obj.udpToPort[count], "udp", obj.udpCidr[count], obj.logObj, obj.tenantId, parentGroupId, obj.endPointObj )
					count = count + 1
				
			if 1 == obj.icmpProtocol:
				count = 0
				while (count < len (obj.icmpToPort)):
					createDelete.create_security_group_rule( obj.icmpFromPort[count],  obj.icmpToPort[count], "icmp", obj.icmpCidr[count], obj.logObj, obj.tenantId, parentGroupId, obj.endPointObj )
					count = count + 1
		
			sys.stderr.write("\n\tScript exited Successfully\n\n") #TBD: debugging msg
		except OperationError as e :
			sys.stderr.write("\n" + str (e))
			return e.err

	if  "delete" == obj.action:
		try :
			createDelete.delete_security_group( obj.logObj, obj.tenantId, obj.name, obj.endPointObj )
			sys.stderr.write( "\n\tDeleted the group sucessfully\n\n")
		except OperationError as e :
			sys.stderr.write("\n" + str(e))
			return e.err

if  "__main__" == __name__ :
	exit (SGmain())
