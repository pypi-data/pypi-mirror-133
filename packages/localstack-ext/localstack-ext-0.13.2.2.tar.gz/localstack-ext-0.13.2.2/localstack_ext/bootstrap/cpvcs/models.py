from datetime import datetime
HBXKJ=str
HBXKG=int
HBXKa=super
HBXKP=False
HBXKo=isinstance
HBXKL=hash
HBXKq=bool
HBXKp=True
HBXKb=list
HBXKS=map
HBXKn=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:HBXKJ):
  self.hash_ref:HBXKJ=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:HBXKJ,rel_path:HBXKJ,file_name:HBXKJ,size:HBXKG,service:HBXKJ,region:HBXKJ):
  HBXKa(StateFileRef,self).__init__(hash_ref)
  self.rel_path:HBXKJ=rel_path
  self.file_name:HBXKJ=file_name
  self.size:HBXKG=size
  self.service:HBXKJ=service
  self.region:HBXKJ=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return HBXKP
  if not HBXKo(other,StateFileRef):
   return HBXKP
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return HBXKL((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->HBXKq:
  if not other:
   return HBXKP
  if not HBXKo(other,StateFileRef):
   return HBXKP
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->HBXKq:
  for other in others:
   if self.congruent(other):
    return HBXKp
  return HBXKP
 def metadata(self)->HBXKJ:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:HBXKJ,state_files:Set[StateFileRef],parent_ptr:HBXKJ):
  HBXKa(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:HBXKJ=parent_ptr
 def state_files_info(self)->HBXKJ:
  return "\n".join(HBXKb(HBXKS(lambda state_file:HBXKJ(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:HBXKJ,head_ptr:HBXKJ,message:HBXKJ,timestamp:HBXKJ=HBXKJ(datetime.now().timestamp()),delta_log_ptr:HBXKJ=HBXKn):
  self.tail_ptr:HBXKJ=tail_ptr
  self.head_ptr:HBXKJ=head_ptr
  self.message:HBXKJ=message
  self.timestamp:HBXKJ=timestamp
  self.delta_log_ptr:HBXKJ=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:HBXKJ,to_node:HBXKJ)->HBXKJ:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:HBXKJ,state_files:Set[StateFileRef],parent_ptr:HBXKJ,creator:HBXKJ,rid:HBXKJ,revision_number:HBXKG,assoc_commit:Commit=HBXKn):
  HBXKa(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:HBXKJ=creator
  self.rid:HBXKJ=rid
  self.revision_number:HBXKG=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(HBXKS(lambda state_file:HBXKJ(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:HBXKJ,state_files:Set[StateFileRef],parent_ptr:HBXKJ,creator:HBXKJ,comment:HBXKJ,active_revision_ptr:HBXKJ,outgoing_revision_ptrs:Set[HBXKJ],incoming_revision_ptr:HBXKJ,version_number:HBXKG):
  HBXKa(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(HBXKS(lambda stat_file:HBXKJ(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
