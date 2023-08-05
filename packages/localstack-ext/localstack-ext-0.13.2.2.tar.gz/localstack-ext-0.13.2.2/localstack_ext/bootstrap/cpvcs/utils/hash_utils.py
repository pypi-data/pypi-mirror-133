import hashlib
NhJQx=str
NhJQu=hex
NhJQB=None
NhJQe=open
NhJQR=Exception
NhJQD=int
NhJQG=map
NhJQU=isinstance
import logging
import os
import random
import zipfile
from typing import Optional
from localstack.utils.common import new_tmp_dir,rm_rf
from localstack_ext.bootstrap.cpvcs.models import Revision,Version
from localstack_ext.bootstrap.cpvcs.utils.common import config_context
from localstack_ext.bootstrap.state_utils import API_STATES_DIR,api_states_traverse
LOG=logging.getLogger(__name__)
def random_hash()->NhJQx:
 return NhJQu(random.getrandbits(160))
def compute_file_hash(file_path:NhJQx,accum=NhJQB)->Optional[NhJQx]:
 try:
  with NhJQe(file_path,"rb")as fp:
   if accum:
    accum.update(fp.read())
   else:
    return hashlib.sha1(fp.read()).hexdigest()
 except NhJQR as e:
  LOG.warning(f"Failed to open file and compute hash for file at {file_path}: {e}")
def compute_version_archive_hash(version_no:NhJQD,state_archive:NhJQx)->NhJQx:
 def _compute_file_hash_func(**kwargs):
  dir_name=kwargs.get("dir_name")
  file_name=kwargs.get("fname")
  accum=kwargs.get("mutables")[0]
  file_path=os.path.join(dir_name,file_name)
  compute_file_hash(file_path,accum)
 tmp_state_dir=new_tmp_dir()
 with zipfile.ZipFile(state_archive)as archive:
  archive.extractall(tmp_state_dir)
 tmp_state_archive_api_states=os.path.join(tmp_state_dir,API_STATES_DIR)
 m=hashlib.sha1()
 api_states_traverse(tmp_state_archive_api_states,_compute_file_hash_func,[m])
 m.update(NhJQx(version_no).encode("utf-8"))
 rm_rf(tmp_state_dir)
 return m.hexdigest()
def compute_revision_hash(cpvcs_node:Revision)->NhJQx:
 if not cpvcs_node.state_files:
  return random_hash()
 state_file_keys=NhJQG(lambda state_file:state_file.hash_ref,cpvcs_node.state_files)
 m=hashlib.sha1()
 for key in state_file_keys:
  try:
   with NhJQe(os.path.join(config_context.get_obj_store_path(),key),"rb")as fp:
    m.update(fp.read())
  except NhJQR as e:
   LOG.warning(f"Failed to open file and compute hash for {key}: {e}")
 if NhJQU(cpvcs_node,Revision):
  m.update(cpvcs_node.rid.encode("utf-8"))
  m.update(NhJQx(cpvcs_node.revision_number).encode("utf-8"))
 elif NhJQU(cpvcs_node,Version):
  m.update(NhJQx(cpvcs_node.version_number).encode("utf-8"))
 return m.hexdigest()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
