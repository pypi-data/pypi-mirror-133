from localstack.utils.aws import aws_models
XNaAC=super
XNaAm=None
XNaAk=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  XNaAC(LambdaLayer,self).__init__(arn)
  self.cwd=XNaAm
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.XNaAk.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,XNaAk,env=XNaAm):
  XNaAC(RDSDatabase,self).__init__(XNaAk,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,XNaAk,env=XNaAm):
  XNaAC(RDSCluster,self).__init__(XNaAk,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,XNaAk,env=XNaAm):
  XNaAC(AppSyncAPI,self).__init__(XNaAk,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,XNaAk,env=XNaAm):
  XNaAC(AmplifyApp,self).__init__(XNaAk,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,XNaAk,env=XNaAm):
  XNaAC(ElastiCacheCluster,self).__init__(XNaAk,env=env)
class TransferServer(BaseComponent):
 def __init__(self,XNaAk,env=XNaAm):
  XNaAC(TransferServer,self).__init__(XNaAk,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,XNaAk,env=XNaAm):
  XNaAC(CloudFrontDistribution,self).__init__(XNaAk,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,XNaAk,env=XNaAm):
  XNaAC(CodeCommitRepository,self).__init__(XNaAk,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
