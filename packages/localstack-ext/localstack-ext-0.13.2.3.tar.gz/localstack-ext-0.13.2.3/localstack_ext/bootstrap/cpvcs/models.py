from datetime import datetime
wmxRE=str
wmxRe=int
wmxRU=super
wmxRA=False
wmxRd=isinstance
wmxRV=hash
wmxRM=bool
wmxRB=True
wmxRo=list
wmxRz=map
wmxRW=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:wmxRE):
  self.hash_ref:wmxRE=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:wmxRE,rel_path:wmxRE,file_name:wmxRE,size:wmxRe,service:wmxRE,region:wmxRE):
  wmxRU(StateFileRef,self).__init__(hash_ref)
  self.rel_path:wmxRE=rel_path
  self.file_name:wmxRE=file_name
  self.size:wmxRe=size
  self.service:wmxRE=service
  self.region:wmxRE=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return wmxRA
  if not wmxRd(other,StateFileRef):
   return wmxRA
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return wmxRV((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->wmxRM:
  if not other:
   return wmxRA
  if not wmxRd(other,StateFileRef):
   return wmxRA
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->wmxRM:
  for other in others:
   if self.congruent(other):
    return wmxRB
  return wmxRA
 def metadata(self)->wmxRE:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:wmxRE,state_files:Set[StateFileRef],parent_ptr:wmxRE):
  wmxRU(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:wmxRE=parent_ptr
 def state_files_info(self)->wmxRE:
  return "\n".join(wmxRo(wmxRz(lambda state_file:wmxRE(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:wmxRE,head_ptr:wmxRE,message:wmxRE,timestamp:wmxRE=wmxRE(datetime.now().timestamp()),delta_log_ptr:wmxRE=wmxRW):
  self.tail_ptr:wmxRE=tail_ptr
  self.head_ptr:wmxRE=head_ptr
  self.message:wmxRE=message
  self.timestamp:wmxRE=timestamp
  self.delta_log_ptr:wmxRE=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:wmxRE,to_node:wmxRE)->wmxRE:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:wmxRE,state_files:Set[StateFileRef],parent_ptr:wmxRE,creator:wmxRE,rid:wmxRE,revision_number:wmxRe,assoc_commit:Commit=wmxRW):
  wmxRU(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:wmxRE=creator
  self.rid:wmxRE=rid
  self.revision_number:wmxRe=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(wmxRz(lambda state_file:wmxRE(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:wmxRE,state_files:Set[StateFileRef],parent_ptr:wmxRE,creator:wmxRE,comment:wmxRE,active_revision_ptr:wmxRE,outgoing_revision_ptrs:Set[wmxRE],incoming_revision_ptr:wmxRE,version_number:wmxRe):
  wmxRU(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(wmxRz(lambda stat_file:wmxRE(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
