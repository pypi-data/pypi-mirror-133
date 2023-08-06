from datetime import datetime
IljxK=str
Iljxq=int
IljxD=super
IljxJ=False
IljxS=isinstance
Iljxf=hash
Iljxw=bool
IljxT=True
IljxA=list
IljxV=map
Iljxz=None
from enum import Enum
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
from localstack_ext.bootstrap.state_utils import API_STATES_DIR,DYNAMODB_DIR,KINESIS_DIR
class CPVCSObj:
 def __init__(self,hash_ref:IljxK):
  self.hash_ref:IljxK=hash_ref
class Serialization(Enum):
 MAIN=API_STATES_DIR
 DDB=DYNAMODB_DIR
 KINESIS=KINESIS_DIR
 serializer_root_lookup={IljxK(MAIN):API_STATES_DIR,IljxK(DDB):DYNAMODB_DIR,IljxK(KINESIS):KINESIS_DIR}
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:IljxK,rel_path:IljxK,file_name:IljxK,size:Iljxq,service:IljxK,region:IljxK,serialization:Serialization):
  IljxD(StateFileRef,self).__init__(hash_ref)
  self.rel_path:IljxK=rel_path
  self.file_name:IljxK=file_name
  self.size:Iljxq=size
  self.service:IljxK=service
  self.region:IljxK=region
  self.serialization:Serialization=serialization
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path,serialization=self.serialization)
 def __eq__(self,other):
  if not other:
   return IljxJ
  if not IljxS(other,StateFileRef):
   return IljxJ
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return Iljxf((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->Iljxw:
  if not other:
   return IljxJ
  if not IljxS(other,StateFileRef):
   return IljxJ
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->Iljxw:
  for other in others:
   if self.congruent(other):
    return IljxT
  return IljxJ
 def metadata(self)->IljxK:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:IljxK,state_files:Set[StateFileRef],parent_ptr:IljxK):
  IljxD(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:IljxK=parent_ptr
 def state_files_info(self)->IljxK:
  return "\n".join(IljxA(IljxV(lambda state_file:IljxK(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:IljxK,head_ptr:IljxK,message:IljxK,timestamp:IljxK=IljxK(datetime.now().timestamp()),delta_log_ptr:IljxK=Iljxz):
  self.tail_ptr:IljxK=tail_ptr
  self.head_ptr:IljxK=head_ptr
  self.message:IljxK=message
  self.timestamp:IljxK=timestamp
  self.delta_log_ptr:IljxK=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:IljxK,to_node:IljxK)->IljxK:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:IljxK,state_files:Set[StateFileRef],parent_ptr:IljxK,creator:IljxK,rid:IljxK,revision_number:Iljxq,assoc_commit:Commit=Iljxz):
  IljxD(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:IljxK=creator
  self.rid:IljxK=rid
  self.revision_number:Iljxq=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(IljxV(lambda state_file:IljxK(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:IljxK,state_files:Set[StateFileRef],parent_ptr:IljxK,creator:IljxK,comment:IljxK,active_revision_ptr:IljxK,outgoing_revision_ptrs:Set[IljxK],incoming_revision_ptr:IljxK,version_number:Iljxq):
  IljxD(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(IljxV(lambda stat_file:IljxK(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
