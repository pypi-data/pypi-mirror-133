from localstack.utils.aws import aws_models
hVHDJ=super
hVHDc=None
hVHDp=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  hVHDJ(LambdaLayer,self).__init__(arn)
  self.cwd=hVHDc
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.hVHDp.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,hVHDp,env=hVHDc):
  hVHDJ(RDSDatabase,self).__init__(hVHDp,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,hVHDp,env=hVHDc):
  hVHDJ(RDSCluster,self).__init__(hVHDp,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,hVHDp,env=hVHDc):
  hVHDJ(AppSyncAPI,self).__init__(hVHDp,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,hVHDp,env=hVHDc):
  hVHDJ(AmplifyApp,self).__init__(hVHDp,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,hVHDp,env=hVHDc):
  hVHDJ(ElastiCacheCluster,self).__init__(hVHDp,env=env)
class TransferServer(BaseComponent):
 def __init__(self,hVHDp,env=hVHDc):
  hVHDJ(TransferServer,self).__init__(hVHDp,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,hVHDp,env=hVHDc):
  hVHDJ(CloudFrontDistribution,self).__init__(hVHDp,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,hVHDp,env=hVHDc):
  hVHDJ(CodeCommitRepository,self).__init__(hVHDp,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
