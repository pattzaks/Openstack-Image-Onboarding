FAILED_TO_LOGIN             = 10
FAILED_TO_CREATE_IMAGE_ID   = 11
FAILED_TO_LIST_IMAGES       = 12
FAILED_TO_UPLOAD_IMAGE      = 13
FAILED_TO_LIST_IMAGES       = 14 
INVALID_ARGUMENTS_IN_UPLOAD = 20
FAILED_TO_GET_FLAVORREF     = 21
FAILED_TO_GET_IMAGEREF      = 22
FAILED_TO_LAUNCH            = 23
QUOTA_EXCEEDED_CPU          = 24
QUOTA_EXCEEDED_RAM          = 44
QUOTA_EXCEEDED_DISK         = 45
FAILED_TO_STOP              = 25
FAILED_TO_START             = 26
FAILED_TO_TERMINATE         = 27
FAILED_TO_SOFT_REBOOT       = 28
FAILED_TO_HARD_REBOOT       = 29
FAILED_TO_GET_POWER_STATE   = 30
FAILED_TO_GET_STATUS        = 31
FAILED_TO_RESUME            = 32
FAILED_TO_SUSPEND           = 33
UNKNOWN_ERROR               = 70
POST_FAILED                 = 4
REQUEST_FAILED              = 80
INVALID_ARGS_TO_UPLOAD      = 81
IMAGE_NOT_FOUND             = 15
IMAGE_FILE_DOES_NOT_EXIST_LOCALLY = 17
THREAD_ERROR                = 67
INSTANCE_NOT_FOUND          = 35
INVALID_ARGUMENTS           = 9 
FAILED_TO_CREATE_SECURITY_GROUP      = 40
FAILED_TO_CREATE_SECURITY_GROUP_RULE = 41
FAILED_TO_DELETE_SECURITY_GROUP      = 42 
SECURITY_GROUP_DOESNT_EXIST          = 43 
VM_ALREADY_STARTED = 34
QUOTA_EXCEEDED_FOR_SECURITY_GROUP    = 81
TOO_MANY_REQUESTS_IN_A_MINUTE = 82 
IMAGE_NAME_NOT_FOUND = 16
INVALID_ACTION = 55   
FAILED_TO_SOFT_REBOOT  = 73
FAILED_TO_HARD_REBOOT  = 74
FAILED_TO_SUSPEND	   = 75
FAILED_TO_RESUME	   = 76
FLAVOR_NOT_FOUND       = 77
SPECIFIED_SECURITY_GROUP_DOESNT_EXIST = 78
ErrorMap = {

    SPECIFIED_SECURITY_GROUP_DOESNT_EXIST : "specified security group is not present",
	FLAVOR_NOT_FOUND             : 'Specified flavor is not available',
	FAILED_TO_LOGIN              : 'Failed to Login to Keystone API',
	FAILED_TO_CREATE_IMAGE_ID    : 'Failed to create Image ID on OpenStack',
	FAILED_TO_LIST_IMAGES        : 'Failed to list images',
	FAILED_TO_UPLOAD_IMAGE       : 'Failed to upload images',
	INVALID_ARGUMENTS_IN_UPLOAD  : 'Invalid arguments to upload',
	FAILED_TO_GET_FLAVORREF      : 'Failed to get requested Flavor reference from nova module',
	FAILED_TO_GET_IMAGEREF       : 'Failed to get Image requested image reference from glance module ',
	FAILED_TO_LIST_IMAGES        : 'Failed to list images from glance',
	FAILED_TO_LAUNCH             : 'Failed to launch image',
	QUOTA_EXCEEDED_CPU           : 'Failed to launch because CPU quota exceeded',
	QUOTA_EXCEEDED_RAM           : 'Failed to launch because RAM quota exceeded',
	QUOTA_EXCEEDED_DISK          : 'Failed to launch because Disk quota exceeded', 
	FAILED_TO_STOP               : 'Failed to stop',
	FAILED_TO_START              : 'Failed to start , instance already in running state',
	FAILED_TO_TERMINATE          : 'Failed to terminate',
	FAILED_TO_SOFT_REBOOT        : 'Failed to soft reboot',
	FAILED_TO_HARD_REBOOT        : 'Failed to hard reboot',
	FAILED_TO_GET_STATUS         : 'Failed to get status of VM',
	FAILED_TO_GET_POWER_STATE    : 'Failed to get power state of VM',
	FAILED_TO_RESUME             : 'Failed to resume',
	FAILED_TO_SUSPEND            : 'Failed to suspend',
	UNKNOWN_ERROR                : 'Unknown error has occured',
	POST_FAILED                  : 'POST request failed',
	REQUEST_FAILED               : 'HTTP request failed',
	INVALID_ARGS_TO_UPLOAD       : 'Invalid arguments to upload ',
	IMAGE_NOT_FOUND              : 'The specified image was not found',
	THREAD_ERROR                 : 'Thread creation Error',
	INSTANCE_NOT_FOUND           : 'Specified instance not found',
	INVALID_ARGUMENTS            : 'Invalid arguments',
	FAILED_TO_CREATE_SECURITY_GROUP      : 'Failed to create security group',
	FAILED_TO_CREATE_SECURITY_GROUP_RULE : 'Failed to create security group rule',
	FAILED_TO_DELETE_SECURITY_GROUP      : 'Failed to delete security group',
	SECURITY_GROUP_DOESNT_EXIST          : 'The specified security group doesnt exist',
	VM_ALREADY_STARTED                   : 'Cannot start. specified VM is already in running state',
	QUOTA_EXCEEDED_FOR_SECURITY_GROUP    : 'The server is incapable of performing the requested operation',
	TOO_MANY_REQUESTS_IN_A_MINUTE        : 'Only 10 requests are allowed per minute',
	IMAGE_NAME_NOT_FOUND                 : 'Specified Image name not found',
	IMAGE_FILE_DOES_NOT_EXIST_LOCALLY    : 'The specified path for local image is not valid, image does not exist locally on this path',
	INVALID_ACTION                       : 'Action specified is invalid',
	FAILED_TO_SOFT_REBOOT                : 'Failed to do a soft reboot operation',
	FAILED_TO_HARD_REBOOT				 : 'Failed to do a hard reboot operation',
	FAILED_TO_SUSPEND					 : 'Failed to suspend an instance ',
	FAILED_TO_RESUME					 : 'Failed to resume and instance' 
}
