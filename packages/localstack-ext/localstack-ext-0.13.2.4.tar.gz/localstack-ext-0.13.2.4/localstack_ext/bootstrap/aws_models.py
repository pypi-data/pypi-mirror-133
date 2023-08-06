from localstack.utils.aws import aws_models
NWLxF=super
NWLxn=None
NWLxP=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  NWLxF(LambdaLayer,self).__init__(arn)
  self.cwd=NWLxn
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.NWLxP.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,NWLxP,env=NWLxn):
  NWLxF(RDSDatabase,self).__init__(NWLxP,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,NWLxP,env=NWLxn):
  NWLxF(RDSCluster,self).__init__(NWLxP,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,NWLxP,env=NWLxn):
  NWLxF(AppSyncAPI,self).__init__(NWLxP,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,NWLxP,env=NWLxn):
  NWLxF(AmplifyApp,self).__init__(NWLxP,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,NWLxP,env=NWLxn):
  NWLxF(ElastiCacheCluster,self).__init__(NWLxP,env=env)
class TransferServer(BaseComponent):
 def __init__(self,NWLxP,env=NWLxn):
  NWLxF(TransferServer,self).__init__(NWLxP,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,NWLxP,env=NWLxn):
  NWLxF(CloudFrontDistribution,self).__init__(NWLxP,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,NWLxP,env=NWLxn):
  NWLxF(CodeCommitRepository,self).__init__(NWLxP,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
