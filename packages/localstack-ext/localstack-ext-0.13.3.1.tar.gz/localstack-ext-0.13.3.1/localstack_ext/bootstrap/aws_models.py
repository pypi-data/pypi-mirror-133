from localstack.utils.aws import aws_models
stnBF=super
stnBb=None
stnBQ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  stnBF(LambdaLayer,self).__init__(arn)
  self.cwd=stnBb
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.stnBQ.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,stnBQ,env=stnBb):
  stnBF(RDSDatabase,self).__init__(stnBQ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,stnBQ,env=stnBb):
  stnBF(RDSCluster,self).__init__(stnBQ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,stnBQ,env=stnBb):
  stnBF(AppSyncAPI,self).__init__(stnBQ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,stnBQ,env=stnBb):
  stnBF(AmplifyApp,self).__init__(stnBQ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,stnBQ,env=stnBb):
  stnBF(ElastiCacheCluster,self).__init__(stnBQ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,stnBQ,env=stnBb):
  stnBF(TransferServer,self).__init__(stnBQ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,stnBQ,env=stnBb):
  stnBF(CloudFrontDistribution,self).__init__(stnBQ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,stnBQ,env=stnBb):
  stnBF(CodeCommitRepository,self).__init__(stnBQ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
