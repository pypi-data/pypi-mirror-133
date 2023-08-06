from datetime import datetime
cGxNg=str
cGxNC=int
cGxNf=super
cGxNQ=False
cGxNJ=isinstance
cGxNA=hash
cGxNy=bool
cGxNd=True
cGxNO=list
cGxNz=map
cGxNu=None
from enum import Enum
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
from localstack_ext.bootstrap.state_utils import API_STATES_DIR,DYNAMODB_DIR,KINESIS_DIR
class CPVCSObj:
 def __init__(self,hash_ref:cGxNg):
  self.hash_ref:cGxNg=hash_ref
class Serialization(Enum):
 MAIN=API_STATES_DIR
 DDB=DYNAMODB_DIR
 KINESIS=KINESIS_DIR
 serializer_root_lookup={cGxNg(MAIN):API_STATES_DIR,cGxNg(DDB):DYNAMODB_DIR,cGxNg(KINESIS):KINESIS_DIR}
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:cGxNg,rel_path:cGxNg,file_name:cGxNg,size:cGxNC,service:cGxNg,region:cGxNg,serialization:Serialization):
  cGxNf(StateFileRef,self).__init__(hash_ref)
  self.rel_path:cGxNg=rel_path
  self.file_name:cGxNg=file_name
  self.size:cGxNC=size
  self.service:cGxNg=service
  self.region:cGxNg=region
  self.serialization:Serialization=serialization
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path,serialization=self.serialization)
 def __eq__(self,other):
  if not other:
   return cGxNQ
  if not cGxNJ(other,StateFileRef):
   return cGxNQ
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return cGxNA((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->cGxNy:
  if not other:
   return cGxNQ
  if not cGxNJ(other,StateFileRef):
   return cGxNQ
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->cGxNy:
  for other in others:
   if self.congruent(other):
    return cGxNd
  return cGxNQ
 def metadata(self)->cGxNg:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:cGxNg,state_files:Set[StateFileRef],parent_ptr:cGxNg):
  cGxNf(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:cGxNg=parent_ptr
 def state_files_info(self)->cGxNg:
  return "\n".join(cGxNO(cGxNz(lambda state_file:cGxNg(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:cGxNg,head_ptr:cGxNg,message:cGxNg,timestamp:cGxNg=cGxNg(datetime.now().timestamp()),delta_log_ptr:cGxNg=cGxNu):
  self.tail_ptr:cGxNg=tail_ptr
  self.head_ptr:cGxNg=head_ptr
  self.message:cGxNg=message
  self.timestamp:cGxNg=timestamp
  self.delta_log_ptr:cGxNg=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:cGxNg,to_node:cGxNg)->cGxNg:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:cGxNg,state_files:Set[StateFileRef],parent_ptr:cGxNg,creator:cGxNg,rid:cGxNg,revision_number:cGxNC,assoc_commit:Commit=cGxNu):
  cGxNf(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:cGxNg=creator
  self.rid:cGxNg=rid
  self.revision_number:cGxNC=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(cGxNz(lambda state_file:cGxNg(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:cGxNg,state_files:Set[StateFileRef],parent_ptr:cGxNg,creator:cGxNg,comment:cGxNg,active_revision_ptr:cGxNg,outgoing_revision_ptrs:Set[cGxNg],incoming_revision_ptr:cGxNg,version_number:cGxNC):
  cGxNf(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(cGxNz(lambda stat_file:cGxNg(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
