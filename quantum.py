class Quantum:
	adminUrl    = None
	internalUrl = None
	publicUrl   = None
	region      = None
	endPointId  = None
	endpoint    = None
	login_token = None
	name        = "quantum"
	def set_endpoint_values( self, adminUrl, internalUrl, publicUrl, region,endPointId ):
		self.adminUrl    = adminUrl
		self.internalUrl = internalUrl
		self.publicUrl   = publicUrl
		self.region      = region
		self.endPointId  = endPointId
		self.endpoint    = [ adminUrl,internalUrl,publicUrl,region,endPointId  ]
