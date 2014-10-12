from error_map import * 

def find_error_code(data):
	if "Quota exceeded for core" in data:
		return (QUOTA_EXCEEDED_CPU)
	if "Quota exceeded for" in data :
		return (QUOTA_EXCEEDED_RAM)
	if "Cannot start while the instance is in this state" in data :
		return (VM_ALREADY_STARTED)
	if "server has either erred or is incapable of performing the requested operation" in data :
		return (SERVER_ERROR)
	if " This request was rate-limited	" in data :
		return (TOO_MANY_REQUESTS_IN_A_MINUTE)
	if "Unable to find security_group with name" in data :
		return (SPECIFIED_SECURITY_GROUP_DOESNT_EXIST)
											
	#return (REQUEST_FAILED)
