from localstack.utils.aws import aws_models
Kijwe=super
Kijwc=None
Kijwn=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  Kijwe(LambdaLayer,self).__init__(arn)
  self.cwd=Kijwc
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.Kijwn.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,Kijwn,env=Kijwc):
  Kijwe(RDSDatabase,self).__init__(Kijwn,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,Kijwn,env=Kijwc):
  Kijwe(RDSCluster,self).__init__(Kijwn,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,Kijwn,env=Kijwc):
  Kijwe(AppSyncAPI,self).__init__(Kijwn,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,Kijwn,env=Kijwc):
  Kijwe(AmplifyApp,self).__init__(Kijwn,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,Kijwn,env=Kijwc):
  Kijwe(ElastiCacheCluster,self).__init__(Kijwn,env=env)
class TransferServer(BaseComponent):
 def __init__(self,Kijwn,env=Kijwc):
  Kijwe(TransferServer,self).__init__(Kijwn,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,Kijwn,env=Kijwc):
  Kijwe(CloudFrontDistribution,self).__init__(Kijwn,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,Kijwn,env=Kijwc):
  Kijwe(CodeCommitRepository,self).__init__(Kijwn,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
