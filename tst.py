from pywinapi.enclaveapi import *

from pywinapi.kernel32.processthreadsapi import open_process_rw
from pywinapi.kernel32.processthreadsapi import get_current_process_id
from pywinapi.kernel32.errhandlingapi import GetLastError

print("VBS Supported: %s" % true_ish(IsEnclaveTypeSupported(ENCLAVE_TYPE_VBS)))
print("SGX Supported: %s" % true_ish(IsEnclaveTypeSupported(ENCLAVE_TYPE_SGX)))


cpid = get_current_process_id()
print("Current Process ID: %d" % cpid)

res, h_process = open_process_rw(cpid)
if(not res):
    print("OpenProcess Failed: %d" % GetLastError())
    exit(-1)

vci = ENCLAVE_CREATE_INFO_VBS()
vci.Flags = ENCLAVE_VBS_FLAG_DEBUG

from ctypes import * 

import os
dll_path = os.path.abspath("testdrop.dll")


lperr = DWORD(0)
enclave_addr = CreateEnclave(h_process,None,1024*1024*2,0,ENCLAVE_TYPE_VBS,byref(vci),sizeof(ENCLAVE_CREATE_INFO_VBS),byref(lperr))

if(not enclave_addr):
    print("Create Enclave Failed: %d %d" % (GetLastError(),lperr.value))
    exit(-1)

print("Create Enclave OK!")    
print("Enclave Addr: %08X" % enclave_addr)



if(not LoadEnclaveImageW(enclave_addr,dll_path)):
    print("LoadEnclaveImageW Error: %d" % GetLastError())
    exit(-1)
print("Loaded Enclave DLL!")

vii = ENCLAVE_INIT_INFO_VBS()
vii.Length = sizeof(ENCLAVE_INIT_INFO_VBS)
vii.ThreadCount = 1

if(not InitializeEnclave(h_process,enclave_addr,byref(vii),sizeof(ENCLAVE_INIT_INFO_VBS),byref(lperr))):
    print("InitializeEnclave Failed: %d %d" % (GetLastError(),lperr.value))
    exit(-1)
    
print("InitializeEnclave OK!")