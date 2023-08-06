from localstack.utils.aws import aws_models
YGNiu=super
YGNiF=None
YGNil=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  YGNiu(LambdaLayer,self).__init__(arn)
  self.cwd=YGNiF
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.YGNil.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,YGNil,env=YGNiF):
  YGNiu(RDSDatabase,self).__init__(YGNil,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,YGNil,env=YGNiF):
  YGNiu(RDSCluster,self).__init__(YGNil,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,YGNil,env=YGNiF):
  YGNiu(AppSyncAPI,self).__init__(YGNil,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,YGNil,env=YGNiF):
  YGNiu(AmplifyApp,self).__init__(YGNil,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,YGNil,env=YGNiF):
  YGNiu(ElastiCacheCluster,self).__init__(YGNil,env=env)
class TransferServer(BaseComponent):
 def __init__(self,YGNil,env=YGNiF):
  YGNiu(TransferServer,self).__init__(YGNil,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,YGNil,env=YGNiF):
  YGNiu(CloudFrontDistribution,self).__init__(YGNil,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,YGNil,env=YGNiF):
  YGNiu(CodeCommitRepository,self).__init__(YGNil,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
