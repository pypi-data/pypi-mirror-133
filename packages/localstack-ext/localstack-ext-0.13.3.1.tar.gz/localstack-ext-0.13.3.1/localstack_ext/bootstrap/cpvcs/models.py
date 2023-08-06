from datetime import datetime
WbXjg=str
WbXjY=int
WbXju=super
WbXjC=False
WbXjy=isinstance
WbXjd=hash
WbXjz=bool
WbXjR=True
WbXja=list
WbXjT=map
WbXjp=None
from enum import Enum
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
from localstack_ext.bootstrap.state_utils import API_STATES_DIR,DYNAMODB_DIR,KINESIS_DIR
class CPVCSObj:
 def __init__(self,hash_ref:WbXjg):
  self.hash_ref:WbXjg=hash_ref
class Serialization(Enum):
 MAIN=API_STATES_DIR
 DDB=DYNAMODB_DIR
 KINESIS=KINESIS_DIR
 serializer_root_lookup={WbXjg(MAIN):API_STATES_DIR,WbXjg(DDB):DYNAMODB_DIR,WbXjg(KINESIS):KINESIS_DIR}
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:WbXjg,rel_path:WbXjg,file_name:WbXjg,size:WbXjY,service:WbXjg,region:WbXjg,serialization:Serialization):
  WbXju(StateFileRef,self).__init__(hash_ref)
  self.rel_path:WbXjg=rel_path
  self.file_name:WbXjg=file_name
  self.size:WbXjY=size
  self.service:WbXjg=service
  self.region:WbXjg=region
  self.serialization:Serialization=serialization
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path,serialization=self.serialization)
 def __eq__(self,other):
  if not other:
   return WbXjC
  if not WbXjy(other,StateFileRef):
   return WbXjC
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return WbXjd((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->WbXjz:
  if not other:
   return WbXjC
  if not WbXjy(other,StateFileRef):
   return WbXjC
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->WbXjz:
  for other in others:
   if self.congruent(other):
    return WbXjR
  return WbXjC
 def metadata(self)->WbXjg:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:WbXjg,state_files:Set[StateFileRef],parent_ptr:WbXjg):
  WbXju(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:WbXjg=parent_ptr
 def state_files_info(self)->WbXjg:
  return "\n".join(WbXja(WbXjT(lambda state_file:WbXjg(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:WbXjg,head_ptr:WbXjg,message:WbXjg,timestamp:WbXjg=WbXjg(datetime.now().timestamp()),delta_log_ptr:WbXjg=WbXjp):
  self.tail_ptr:WbXjg=tail_ptr
  self.head_ptr:WbXjg=head_ptr
  self.message:WbXjg=message
  self.timestamp:WbXjg=timestamp
  self.delta_log_ptr:WbXjg=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:WbXjg,to_node:WbXjg)->WbXjg:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:WbXjg,state_files:Set[StateFileRef],parent_ptr:WbXjg,creator:WbXjg,rid:WbXjg,revision_number:WbXjY,assoc_commit:Commit=WbXjp):
  WbXju(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:WbXjg=creator
  self.rid:WbXjg=rid
  self.revision_number:WbXjY=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(WbXjT(lambda state_file:WbXjg(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:WbXjg,state_files:Set[StateFileRef],parent_ptr:WbXjg,creator:WbXjg,comment:WbXjg,active_revision_ptr:WbXjg,outgoing_revision_ptrs:Set[WbXjg],incoming_revision_ptr:WbXjg,version_number:WbXjY):
  WbXju(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(WbXjT(lambda stat_file:WbXjg(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
