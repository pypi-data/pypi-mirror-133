from datetime import datetime
zUbFq=str
zUbFm=int
zUbFW=super
zUbFB=False
zUbFl=isinstance
zUbFg=hash
zUbFw=bool
zUbFH=True
zUbFX=list
zUbFo=map
zUbFs=None
from enum import Enum
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
from localstack_ext.bootstrap.state_utils import API_STATES_DIR,DYNAMODB_DIR,KINESIS_DIR
class CPVCSObj:
 def __init__(self,hash_ref:zUbFq):
  self.hash_ref:zUbFq=hash_ref
class Serialization(Enum):
 MAIN=API_STATES_DIR
 DDB=DYNAMODB_DIR
 KINESIS=KINESIS_DIR
 serializer_root_lookup={zUbFq(MAIN):API_STATES_DIR,zUbFq(DDB):DYNAMODB_DIR,zUbFq(KINESIS):KINESIS_DIR}
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:zUbFq,rel_path:zUbFq,file_name:zUbFq,size:zUbFm,service:zUbFq,region:zUbFq,serialization:Serialization):
  zUbFW(StateFileRef,self).__init__(hash_ref)
  self.rel_path:zUbFq=rel_path
  self.file_name:zUbFq=file_name
  self.size:zUbFm=size
  self.service:zUbFq=service
  self.region:zUbFq=region
  self.serialization:Serialization=serialization
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path,serialization=self.serialization)
 def __eq__(self,other):
  if not other:
   return zUbFB
  if not zUbFl(other,StateFileRef):
   return zUbFB
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return zUbFg((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->zUbFw:
  if not other:
   return zUbFB
  if not zUbFl(other,StateFileRef):
   return zUbFB
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->zUbFw:
  for other in others:
   if self.congruent(other):
    return zUbFH
  return zUbFB
 def metadata(self)->zUbFq:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:zUbFq,state_files:Set[StateFileRef],parent_ptr:zUbFq):
  zUbFW(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:zUbFq=parent_ptr
 def state_files_info(self)->zUbFq:
  return "\n".join(zUbFX(zUbFo(lambda state_file:zUbFq(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:zUbFq,head_ptr:zUbFq,message:zUbFq,timestamp:zUbFq=zUbFq(datetime.now().timestamp()),delta_log_ptr:zUbFq=zUbFs):
  self.tail_ptr:zUbFq=tail_ptr
  self.head_ptr:zUbFq=head_ptr
  self.message:zUbFq=message
  self.timestamp:zUbFq=timestamp
  self.delta_log_ptr:zUbFq=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:zUbFq,to_node:zUbFq)->zUbFq:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:zUbFq,state_files:Set[StateFileRef],parent_ptr:zUbFq,creator:zUbFq,rid:zUbFq,revision_number:zUbFm,assoc_commit:Commit=zUbFs):
  zUbFW(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:zUbFq=creator
  self.rid:zUbFq=rid
  self.revision_number:zUbFm=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(zUbFo(lambda state_file:zUbFq(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:zUbFq,state_files:Set[StateFileRef],parent_ptr:zUbFq,creator:zUbFq,comment:zUbFq,active_revision_ptr:zUbFq,outgoing_revision_ptrs:Set[zUbFq],incoming_revision_ptr:zUbFq,version_number:zUbFm):
  zUbFW(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(zUbFo(lambda stat_file:zUbFq(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
