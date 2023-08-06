import inspect
RbOWH=bytes
RbOWY=None
RbOWF=isinstance
RbOWd=list
RbOWv=getattr
RbOWX=open
RbOWB=property
RbOWE=Exception
RbOWm=setattr
RbOWu=True
import os.path
import sys
import traceback
from importlib.abc import MetaPathFinder,SourceLoader
from importlib.util import spec_from_file_location
import pyaes
class DecryptionHandler:
 decryption_key:RbOWH
 def __init__(self,decryption_key:RbOWH):
  self.decryption_key=decryption_key
 def decrypt(self,content)->RbOWH:
  cipher=pyaes.AESModeOfOperationCBC(self.decryption_key,iv="\0"*16)
  decrypter=pyaes.Decrypter(cipher)
  decrypted=decrypter.feed(content)
  decrypted+=decrypter.feed()
  decrypted=decrypted.partition(b"\0")[0]
  return decrypted
class EncryptedFileFinder(MetaPathFinder):
 decryption_handler:DecryptionHandler
 def __init__(self,decryption_handler:DecryptionHandler):
  self.decryption_handler=decryption_handler
 def find_spec(self,fullname,path,target=RbOWY):
  if path and not RbOWF(path,RbOWd):
   path=RbOWd(RbOWv(path,"_path",[]))
  if not path:
   return RbOWY
  name=fullname.split(".")[-1]
  file_path=os.path.join(path[0],name+".py")
  enc=file_path+".enc"
  if not os.path.isfile(enc):
   return RbOWY
  if os.path.isfile(file_path):
   return RbOWY
  return spec_from_file_location(fullname,enc,loader=DecryptingLoader(enc,self.decryption_handler))
class DecryptingLoader(SourceLoader):
 decryption_handler:DecryptionHandler
 def __init__(self,encrypted_file,decryption_handler:DecryptionHandler):
  self.encrypted_file=encrypted_file
  self.decryption_handler=decryption_handler
 def get_filename(self,fullname):
  return self.encrypted_file
 def get_data(self,filename):
  with RbOWX(filename,"rb")as f:
   data=f.read()
  data=self.decryption_handler.decrypt(data)
  return data
def init_source_decryption(decryption_handler:DecryptionHandler):
 sys.meta_path.insert(0,EncryptedFileFinder(decryption_handler))
 patch_traceback_lines()
 patch_inspect_findsource()
def patch_traceback_lines():
 if RbOWv(traceback.FrameSummary,"_ls_patch_applied",RbOWY):
  return
 @RbOWB
 def line(self):
  try:
   return line_orig.fget(self)
  except RbOWE:
   self._line=""
   return self._line
 line_orig=traceback.FrameSummary.line
 RbOWm(traceback.FrameSummary,"line",line)
 traceback.FrameSummary._ls_patch_applied=RbOWu
def patch_inspect_findsource():
 if RbOWv(inspect,"_ls_patch_applied",RbOWY):
  return
 def findsource(*args,**kwargs):
  try:
   return findsource_orig(*args,**kwargs)
  except RbOWE:
   return[],0
 findsource_orig=inspect.findsource
 inspect.findsource=findsource
 inspect._ls_patch_applied=RbOWu
# Created by pyminifier (https://github.com/liftoff/pyminifier)
