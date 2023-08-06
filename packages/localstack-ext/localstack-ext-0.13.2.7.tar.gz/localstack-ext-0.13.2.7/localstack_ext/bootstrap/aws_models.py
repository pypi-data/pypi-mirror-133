from localstack.utils.aws import aws_models
MYsic=super
MYsiX=None
MYsiU=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  MYsic(LambdaLayer,self).__init__(arn)
  self.cwd=MYsiX
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.MYsiU.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,MYsiU,env=MYsiX):
  MYsic(RDSDatabase,self).__init__(MYsiU,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,MYsiU,env=MYsiX):
  MYsic(RDSCluster,self).__init__(MYsiU,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,MYsiU,env=MYsiX):
  MYsic(AppSyncAPI,self).__init__(MYsiU,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,MYsiU,env=MYsiX):
  MYsic(AmplifyApp,self).__init__(MYsiU,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,MYsiU,env=MYsiX):
  MYsic(ElastiCacheCluster,self).__init__(MYsiU,env=env)
class TransferServer(BaseComponent):
 def __init__(self,MYsiU,env=MYsiX):
  MYsic(TransferServer,self).__init__(MYsiU,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,MYsiU,env=MYsiX):
  MYsic(CloudFrontDistribution,self).__init__(MYsiU,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,MYsiU,env=MYsiX):
  MYsic(CodeCommitRepository,self).__init__(MYsiU,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
