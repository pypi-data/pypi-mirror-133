from localstack.utils.aws import aws_models
AOCKj=super
AOCKI=None
AOCKr=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  AOCKj(LambdaLayer,self).__init__(arn)
  self.cwd=AOCKI
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.AOCKr.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,AOCKr,env=AOCKI):
  AOCKj(RDSDatabase,self).__init__(AOCKr,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,AOCKr,env=AOCKI):
  AOCKj(RDSCluster,self).__init__(AOCKr,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,AOCKr,env=AOCKI):
  AOCKj(AppSyncAPI,self).__init__(AOCKr,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,AOCKr,env=AOCKI):
  AOCKj(AmplifyApp,self).__init__(AOCKr,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,AOCKr,env=AOCKI):
  AOCKj(ElastiCacheCluster,self).__init__(AOCKr,env=env)
class TransferServer(BaseComponent):
 def __init__(self,AOCKr,env=AOCKI):
  AOCKj(TransferServer,self).__init__(AOCKr,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,AOCKr,env=AOCKI):
  AOCKj(CloudFrontDistribution,self).__init__(AOCKr,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,AOCKr,env=AOCKI):
  AOCKj(CodeCommitRepository,self).__init__(AOCKr,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
