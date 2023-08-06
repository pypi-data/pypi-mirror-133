import inspect
utdyj=bytes
utdyB=None
utdyc=isinstance
utdyX=list
utdyR=getattr
utdyw=open
utdyT=property
utdyN=Exception
utdyi=setattr
utdyH=True
import os.path
import sys
import traceback
from importlib.abc import MetaPathFinder,SourceLoader
from importlib.util import spec_from_file_location
import pyaes
class DecryptionHandler:
 decryption_key:utdyj
 def __init__(self,decryption_key:utdyj):
  self.decryption_key=decryption_key
 def decrypt(self,content)->utdyj:
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
 def find_spec(self,fullname,path,target=utdyB):
  if path and not utdyc(path,utdyX):
   path=utdyX(utdyR(path,"_path",[]))
  if not path:
   return utdyB
  name=fullname.split(".")[-1]
  file_path=os.path.join(path[0],name+".py")
  enc=file_path+".enc"
  if not os.path.isfile(enc):
   return utdyB
  if os.path.isfile(file_path):
   return utdyB
  return spec_from_file_location(fullname,enc,loader=DecryptingLoader(enc,self.decryption_handler))
class DecryptingLoader(SourceLoader):
 decryption_handler:DecryptionHandler
 def __init__(self,encrypted_file,decryption_handler:DecryptionHandler):
  self.encrypted_file=encrypted_file
  self.decryption_handler=decryption_handler
 def get_filename(self,fullname):
  return self.encrypted_file
 def get_data(self,filename):
  with utdyw(filename,"rb")as f:
   data=f.read()
  data=self.decryption_handler.decrypt(data)
  return data
def init_source_decryption(decryption_handler:DecryptionHandler):
 sys.meta_path.insert(0,EncryptedFileFinder(decryption_handler))
 patch_traceback_lines()
 patch_inspect_findsource()
def patch_traceback_lines():
 if utdyR(traceback.FrameSummary,"_ls_patch_applied",utdyB):
  return
 @utdyT
 def line(self):
  try:
   return line_orig.fget(self)
  except utdyN:
   self._line=""
   return self._line
 line_orig=traceback.FrameSummary.line
 utdyi(traceback.FrameSummary,"line",line)
 traceback.FrameSummary._ls_patch_applied=utdyH
def patch_inspect_findsource():
 if utdyR(inspect,"_ls_patch_applied",utdyB):
  return
 def findsource(*args,**kwargs):
  try:
   return findsource_orig(*args,**kwargs)
  except utdyN:
   return[],0
 findsource_orig=inspect.findsource
 inspect.findsource=findsource
 inspect._ls_patch_applied=utdyH
# Created by pyminifier (https://github.com/liftoff/pyminifier)
