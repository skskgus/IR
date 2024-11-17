import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import os

#차원축소에 필요
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

#모델 불러올때에 필요
import joblib

#---------바꿔야 하는 값---------#

# 프로젝트 루트 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 입력 데이터셋 위치
input_dir = os.path.join(BASE_DIR, 'outputs', 'outputs.csv')




#총 원핫 인코딩 열 이름 리스트
#아래 코드 결과 여기에 복붙해 사용 - 아래가 복붙한 값임.
col_checklist = ['file_name', 'Entropy', 'ATT&CK Tactic', 'ATT&CK Technique', 'MBC Objective', 'MBC Behavior', 'Namespace', 'Capability', 'Y',
                  'ATT_Tactic_Collection','ATT_Tactic_Command and Control', 'ATT_Tactic_Credential Access', 'ATT_Tactic_Defense Evasion',
                 'ATT_Tactic_Discovery', 'ATT_Tactic_Execution', 'ATT_Tactic_Impact', 'ATT_Tactic_Persistence', 'ATT_Tactic_Privilege Escalation',
                 'ATT_Technique_T1027.005', 'ATT_Technique_T1056.001', 'ATT_Technique_T1053.002', 'ATT_Technique_T1057', 'ATT_Technique_T1129',
                 'ATT_Technique_T1547.005', 'ATT_Technique_T1071.001', 'ATT_Technique_T1123', 'ATT_Technique_T1070', 'ATT_Technique_T1546.002',
                 'ATT_Technique_T1564.003', 'ATT_Technique_T1564.005', 'ATT_Technique_T1134.001', 'ATT_Technique_T1033', 'ATT_Technique_T1105',
                 'ATT_Technique_T1555.004', 'ATT_Technique_T1490', 'ATT_Technique_T1531', 'ATT_Technique_T1569.002', 'ATT_Technique_T1027', 'ATT_Technique_T1565.002',
                 'ATT_Technique_T1560.002', 'ATT_Technique_T1614.001', 'ATT_Technique_T1070.006', 'ATT_Technique_T1140', 'ATT_Technique_T1134', 'ATT_Technique_T1562',
                 'ATT_Technique_T1518', 'ATT_Technique_T1497.001', 'ATT_Technique_T1055.003', 'ATT_Technique_T1016', 'ATT_Technique_T1112', 'ATT_Technique_T1518.001',
                 'ATT_Technique_T1564', 'ATT_Technique_T1055.001', 'ATT_Technique_T1087', 'ATT_Technique_T1012', 'ATT_Technique_T1547.001', 'ATT_Technique_T1542.001',
                 'ATT_Technique_T1562.001', 'ATT_Technique_T1548.002', 'ATT_Technique_T1053.005', 'ATT_Technique_T1213', 'ATT_Technique_T1546.010', 'ATT_Technique_T1010',
                 'ATT_Technique_T1505.004', 'ATT_Technique_T1055.002', 'ATT_Technique_T1482', 'ATT_Technique_T1555.003', 'ATT_Technique_T1027.002', 'ATT_Technique_T1055',
                 'ATT_Technique_T1547.004', 'ATT_Technique_T1496', 'ATT_Technique_T1115', 'ATT_Technique_T1547.014', 'ATT_Technique_T1497', 'ATT_Technique_T1059', 'ATT_Technique_T1027.004',
                 'ATT_Technique_T1134.004', 'ATT_Technique_T1561.002', 'ATT_Technique_T1069', 'ATT_Technique_T1614', 'ATT_Technique_T1574', 'ATT_Technique_T1137.006', 'ATT_Technique_T1016.001',
                 'ATT_Technique_T1070.004', 'ATT_Technique_T1070.001', 'ATT_Technique_T1059.006', 'ATT_Technique_T1505.002', 'ATT_Technique_T1059.003', 'ATT_Technique_T1007', 'ATT_Technique_T1055.004',
                 'ATT_Technique_T1615', 'ATT_Technique_T1652', 'ATT_Technique_T1113', 'ATT_Technique_T1547.009', 'ATT_Technique_T1059.001', 'ATT_Technique_T1529', 'ATT_Technique_T1222', 'ATT_Technique_T1135',
                 'ATT_Technique_T1197', 'ATT_Technique_T1082', 'ATT_Technique_T1543.003', 'ATT_Technique_T1553.005', 'ATT_Technique_T1125', 'ATT_Technique_T1047', 'ATT_Technique_T1622', 'ATT_Technique_T1546',
                 'ATT_Technique_T1098', 'ATT_Technique_T1040', 'ATT_Technique_T1499', 'ATT_Technique_T1620', 'ATT_Technique_T1055.012', 'ATT_Technique_T1136', 'ATT_Technique_T1497.002', 'ATT_Technique_T1555',
                 'ATT_Technique_T1083', 'ATT_Technique_T1562.009', 'MBC_obj_Anti-Behavioral Analysis', 'MBC_obj_Anti-Static Analysis', 'MBC_obj_Collection', 'MBC_obj_Command and Control', 'MBC_obj_Communication',
                 'MBC_obj_Cryptography', 'MBC_obj_Data', 'MBC_obj_Defense Evasion', 'MBC_obj_Discovery', 'MBC_obj_Execution', 'MBC_obj_File System', 'MBC_obj_Hardware', 'MBC_obj_Impact', 'MBC_obj_Memory',
                 'MBC_obj_Operating System', 'MBC_obj_Persistence', 'MBC_obj_Process', 'MBC_Behavior_F0001.008', 'MBC_Behavior_C0042', 'MBC_Behavior_C0066', 'MBC_Behavior_C0002.011', 'MBC_Behavior_F0012',
                 'MBC_Behavior_C0001.004', 'MBC_Behavior_C0037.001', 'MBC_Behavior_B0022.001', 'MBC_Behavior_B0032.020', 'MBC_Behavior_F0004.008', 'MBC_Behavior_C0044', 'MBC_Behavior_C0032.002',
                 'MBC_Behavior_B0030.003', 'MBC_Behavior_B0042.001', 'MBC_Behavior_C0027', 'MBC_Behavior_C0052', 'MBC_Behavior_C0001.014', 'MBC_Behavior_E1510', 'MBC_Behavior_C0001.007', 'MBC_Behavior_C0065',
                 'MBC_Behavior_C0047', 'MBC_Behavior_C0002.010', 'MBC_Behavior_C0002.017', 'MBC_Behavior_C0002.012', 'MBC_Behavior_C0002.009', 'MBC_Behavior_E1113', 'MBC_Behavior_C0036.005',
                 'MBC_Behavior_C0036.002', 'MBC_Behavior_C0025.002', 'MBC_Behavior_C0001.003', 'MBC_Behavior_C0043', 'MBC_Behavior_B0013.001', 'MBC_Behavior_C0001.001', 'MBC_Behavior_C0058',
                 'MBC_Behavior_C0002.015', 'MBC_Behavior_C0039', 'MBC_Behavior_B0009.025', 'MBC_Behavior_C0037', 'MBC_Behavior_C0038', 'MBC_Behavior_C0002.006', 'MBC_Behavior_B0009.029', 'MBC_Behavior_C0031',
                 'MBC_Behavior_C0018', 'MBC_Behavior_E1027.m02', 'MBC_Behavior_C0002.013', 'MBC_Behavior_F0002.001', 'MBC_Behavior_C0029', 'MBC_Behavior_C0045', 'MBC_Behavior_C0055', 'MBC_Behavior_C0025.003',
                 'MBC_Behavior_C0063', 'MBC_Behavior_C0036.004', 'MBC_Behavior_E1113.m01', 'MBC_Behavior_E1485.m04', 'MBC_Behavior_E1059', 'MBC_Behavior_C0002.018', 'MBC_Behavior_C0002.005', 'MBC_Behavior_C0034',
                 'MBC_Behavior_C0032.001', 'MBC_Behavior_C0029.003', 'MBC_Behavior_C0035', 'MBC_Behavior_C0001.010', 'MBC_Behavior_C0003.004', 'MBC_Behavior_B0042.002', 'MBC_Behavior_C0003.003', 'MBC_Behavior_C0029.005',
                 'MBC_Behavior_B0001.036', 'MBC_Behavior_E1083.m01', 'MBC_Behavior_B0001.005', 'MBC_Behavior_B0001.032', 'MBC_Behavior_C0001.008', 'MBC_Behavior_B0009.034', 'MBC_Behavior_C0064', 'MBC_Behavior_B0001.035',
                 'MBC_Behavior_F0005', 'MBC_Behavior_B0032', 'MBC_Behavior_F0001', 'MBC_Behavior_C0051', 'MBC_Behavior_B0001.024', 'MBC_Behavior_F0001.011', 'MBC_Behavior_F0002.002', 'MBC_Behavior_C0060', 'MBC_Behavior_C0003.001',
                 'MBC_Behavior_B0001.025', 'MBC_Behavior_B0009.012', 'MBC_Behavior_E1027.m05', 'MBC_Behavior_C0053.001', 'MBC_Behavior_C0041', 'MBC_Behavior_C0002.014', 'MBC_Behavior_C0008', 'MBC_Behavior_B0001.002',
                 'MBC_Behavior_C0034.001', 'MBC_Behavior_C0023.001', 'MBC_Behavior_C0026.001', 'MBC_Behavior_E1010', 'MBC_Behavior_B0043', 'MBC_Behavior_C0002.004', 'MBC_Behavior_B0003.003', 'MBC_Behavior_C0040',
                 'MBC_Behavior_B0004', 'MBC_Behavior_C0011.001', 'MBC_Behavior_C0002.016', 'MBC_Behavior_C0001.005', 'MBC_Behavior_C0036.007', 'MBC_Behavior_C0002.003', 'MBC_Behavior_C0030', 'MBC_Behavior_C0027.011',
                 'MBC_Behavior_C0014.002', 'MBC_Behavior_C0030.006', 'MBC_Behavior_F0001.002', 'MBC_Behavior_C0031.001', 'MBC_Behavior_C0017', 'MBC_Behavior_C0030.001', 'MBC_Behavior_C0003.002', 'MBC_Behavior_C0004.001',
                 'MBC_Behavior_C0016', 'MBC_Behavior_C0021', 'MBC_Behavior_E1082', 'MBC_Behavior_B0009', 'MBC_Behavior_C0024', 'MBC_Behavior_F0004.005', 'MBC_Behavior_F0007.001', 'MBC_Behavior_F0014', 'MBC_Behavior_C0029.002',
                 'MBC_Behavior_C0002', 'MBC_Behavior_B0046.002', 'MBC_Behavior_E1055', 'MBC_Behavior_C0002.008', 'MBC_Behavior_C0001.011', 'MBC_Behavior_C0029.001', 'MBC_Behavior_F0004.007', 'MBC_Behavior_C0001.006', 'MBC_Behavior_B0012',
                 'MBC_Behavior_C0059', 'MBC_Behavior_C0003', 'MBC_Behavior_C0027.009', 'MBC_Behavior_C0019', 'MBC_Behavior_C0049', 'MBC_Behavior_B0001.034', 'MBC_Behavior_E1055.m04', 'MBC_Behavior_B0030.001', 'MBC_Behavior_C0025',
                 'MBC_Behavior_B0001.019', 'MBC_Behavior_F0015.006', 'MBC_Behavior_B0025.007', 'MBC_Behavior_B0030.002', 'MBC_Behavior_C0054', 'MBC_Behavior_C0036.006', 'MBC_Behavior_B0001.010', 'MBC_Behavior_E1083', 'MBC_Behavior_B0002',
                 'MBC_Behavior_B0023', 'MBC_Behavior_C0032.005', 'MBC_Behavior_B0046.001', 'MBC_Behavior_C0061', 'MBC_Behavior_C0031.010', 'MBC_Behavior_C0048', 'MBC_Behavior_C0028.001', 'MBC_Behavior_B0001.012', 'MBC_Behavior_C0007',
                 'MBC_Behavior_C0046', 'MBC_Behavior_C0001.009', 'MBC_Behavior_F0001.009', 'MBC_Behavior_C0057.001', 'MBC_Behavior_C0001.012', 'MBC_Behavior_C0030.005', 'MBC_Behavior_C0026', 'MBC_Behavior_C0033', 'MBC_Behavior_E1027.m03',
                 'MBC_Behavior_F0015.003', 'MBC_Behavior_C0050', 'MBC_Behavior_C0028', 'MBC_Behavior_F0001.010', 'MBC_Behavior_C0025.001', 'MBC_Behavior_C0036.001', 'MBC_Behavior_C0029.004', 'MBC_Behavior_B0001', 'MBC_Behavior_C0017.003',
                 'MBC_Behavior_C0021.003', 'MBC_Behavior_B0001.033', 'MBC_Behavior_B0001.016', 'namespace_persistence', 'namespace_linking', 'namespace_compiler', 'namespace_targeting', 'namespace_executable', 'namespace_collection',
                 'namespace_communication', 'namespace_load-code', 'namespace_anti-analysis', 'namespace_data-manipulation', 'namespace_internal', 'compiled to the .NET platform', 'contain loop', 'manipulate console buffer',
                 'check if directory exists', 'check if file exists', 'access .NET resource', 'packed with UPX', 'packed with generic packer', 'Packed samples have often been obfuscated to hide their logic.',
                 'resolve function by parsing PE exports', 'delay execution', 'create or open file', 'get OS version', 'terminate process', 'link function at runtime on Windows', 'parse PE header', 'accept command line arguments',
                 'enumerate PE sections', 'inspect section memory permissions', 'check OS version', 'print debug messages', 'encode data using XOR', 'calculate modulo 256 via x86 assembly', 'no capabilities found',
                 'query environment variable', 'get system information on Windows', 'get file attributes', 'set registry value', 'read file via mapping', 'get token membership', 'query or enumerate registry value',
                 'create process on Windows', 'open process', 'delete file', 'get common file path', 'check mutex', 'create or open registry key', 'check HTTP status code', 'listen for remote procedure calls', 'PEB access',
                 'hide graphical window', 'reference analysis tools strings', 'enumerate files on Windows', 'write file on Windows', 'get file size', 'create new key via CryptAcquireContext', 'hash data with MD5',
                 'enumerate files recursively', 'access PEB ldr_data', 'hash data via WinCrypt', 'reference SQL statements', 'initialize hashing via WinCrypt', 'contain obfuscated stackstrings', 'delete registry key',
                 'encode data using Base64', 'query or enumerate registry key', 'decompress data using QuickLZ', 'allocate thread local storage', 'get HTTP document via IWebBrowser2', 'get token privileges', 'create thread',
                 'enumerate processes via NtQuerySystemInformation', 'access the Windows event log', 'load .NET assembly', 'read data from Internet', 'download URL', 'suspend thread', 'receive data', 'set HTTP header',
                 'contains PDB path', 'manipulate network credentials in .NET', 'read HTTP header', 'set environment variable', 'find graphical window', 'get service handle', 'get geographical location', 'get graphical window text',
                 'change memory protection', 'start service', 'copy file', 'read file on Windows', 'query service status', 'get hostname', 'modify access privileges', 'check for time delay via GetTickCount', 'write and execute a file',
                 'unmanaged call', 'get OS version in .NET', 'find process by name', 'set thread local storage value', 'create device object', 'terminate thread', 'set file attributes', 'hash data via BCrypt', 'attach user process memory',
                 'delete directory', 'move file', 'get socket status', 'create directory', 'interact with driver via control codes', 'create pipe', 'get memory capacity', 'reference anti-VM strings targeting VirtualBox',
                 'encrypt data using RC4 PRGA', 'delete registry value', 'initialize Winsock library', 'resume thread', 'get session user name', 'create process suspended', 'execute command', 'resolve DNS', 'stop service',
                 'query service configuration', 'modify service', 'allocate or change RWX memory', 'execute shellcode via indirect call', 'contain a thread local storage', 'get thread local storage value', 'persist via Windows service',
                 'link many functions at runtime', 'create service', 'delete service', 'run as service', 'check mutex and exit', 'read .ini file', 'get file version info', 'bypass UAC via ICMLuaUtil', 'create mutex',
                 'reference Base64 string', 'set current directory', 'shutdown system', 'persist via Run registry key', 'check Internet connectivity via WinINet', 'allocate memory', 'extract resource via kernel32 functions',
                 'enumerate gui resources', 'create HTTP request', 'identify system language via API', 'get keyboard layout', 'allocate or change RW memory', 'encrypt data using RC4 KSA', 'send data', 'create process memory minidump',
                 'connect to HTTP server', 'send file via HTTP', 'reference anti-VM strings targeting Xen', 'manipulate unmanaged memory in .NET', 'get CPU information', 'find data using regex in .NET', 'reference anti-VM strings',
                 'save image in .NET', 'terminate process by name in .NET', 'allocate unmanaged memory in .NET', 'read clipboard data', 'execute anti-debugging instructions', 'create or open section object', 'map section object',
                 'hash data with CRC32', 'log keystrokes', 'capture webcam image', 'linked against ZLIB', 'generate random numbers using a Mersenne Twister', 'connect to WMI namespace via WbemLocator', 'compute adler32 checksum',
                 'parse credit card information', 'generate random numbers using the Delphi LCG', 'hash data using fnv', 'enumerate processes', 'check for software breakpoints', 'generate random numbers via WinAPI',
                 'acquire credentials from Windows Credential Manager', 'hash data using SHA1', 'start minifilter driver', 'register minifilter driver', 'load XML in .NET', 'reference anti-VM strings targeting Parallels',
                 'hash data using CRC32b', 'linked against CPP regex library', 'get session integrity level', 'open thread', 'switch active desktop', 'manipulate boot configuration', 'acquire debug privileges', 'linked against OpenSSL',
                 'linked against CPP standard library', 'write clipboard data', 'open clipboard', 'get file system object information', 'compare security identifiers', 'get Program Files directory', 'swap mouse buttons',
                 'lock the desktop', 'get session information', 'log keystrokes via polling', 'connect network resource', 'set application hook', 'log keystrokes via application hook', 'get disk information', 'hash data using SHA384',
                 'encrypt or decrypt data via BCrypt', 'hash data using SHA512', 'hash data using SHA256', 'hash data using djb2', 'hash data using murmur3', 'parse URL', 'create mailslot', 'enumerate process modules',
                 'read from mailslot', 'create a process with modified I/O handles and window', 'validate payment card number using luhn algorithm with no lookup table', 'validate payment card number using luhn algorithm',
                 'enumerate threads', 'send HTTP request', 'get disk size', 'compress data via ZLIB inflate or deflate', 'get domain information', 'add user account', 'list user accounts', 'prompt user for credentials',
                 'delete user account from group', 'add user account to group', 'get inbound credentials handle via CredSSP', 'enumerate services', 'delete user account', 'get domain controller name', 'get domain trust relationships',
                 'linked against sqlite3', 'send ICMP echo request', 'list domain servers', 'receive data on socket', 'send data on socket', 'read and send data from client to server', 'get user security identifier',
                 'decrypt data using AES via x86 extensions', 'reference processor manufacturer constants', 'reference AES constants', 'encrypt data using AES', 'encrypt data using AES via x86 extensions',
                 'hash data using sha256 via x86 extensions', 'compiled with Go', 'create shortcut via IShellLink', 'set console window title', 'impersonate user', 'encrypt data using DPAPI', 'encrypt data using AES via WinAPI',
                 'encrypt or decrypt via WinCrypt', 'access PE header', 'check for PEB BeingDebugged flag', 'get kernel32 base address', 'inject thread', 'write process memory', 'list TCP connections and listeners',
                 'get local IPv4 addresses', 'execute syscall instruction', 'hash data using SHA224', 'encode data using ADD XOR SUB operations', 'get ntdll base address', 'get process heap flags',
                 'get COMSPEC environment variable', 'set socket configuration', 'connect to URL', 'self delete', 'connect pipe', 'get MAC address on Windows', 'generate random numbers via RtlGenRandom',
                 'get storage device properties', 'inspect load icon resource', 'enumerate disk volumes', 'write pipe', 'hash data using SHA1 via WinCrypt', 'register network filter via WFP API', 'get UEFI variable',
                 'get number of processors', 'find process by PID', 'decode data using Base64 via WinAPI', 'check for time delay via QueryPerformanceCounter', 'timestomp file', 'bypass UAC via RPC', 'encrypt data using DES',
                 'move directory', 'get process image filename', 'enumerate files in .NET', 'receive HTTP response', 'initialize WinHTTP library', 'prepare HTTP request', 'hook routines via microsoft detours', 'change the wallpaper',
                 'enumerate device drivers on Windows', 'reference anti-VM strings targeting VMWare', 'pause service', 'get HTTP content length', 'read pipe', 'check file extension in .NET', 'reference cryptocurrency strings',
                 'migrate process to active window station', 'debug build', 'authenticate HMAC', 'enumerate network shares', 'get startup folder', 'get socket information', 'create two anonymous pipes', 'empty recycle bin quietly',
                 'empty the recycle bin', 'reference absolute stream path on Windows', 'execute shell command via Windows Remote Management', 'compress data via WinAPI', 'manipulate console window', 'hash data using sha1 via x86 extensions',
                 'enumerate processes that use resource', 'create Restart Manager session', 'embed dependencies as resources using Fody/Costura', 'install driver', 'capture microphone audio', 'get installed programs', 'forwarded export',
                 'check for unmoving mouse cursor', 'find taskbar', 'check for foreground window switch', 'reference screen saver executable', 'persist via Winlogon Helper DLL registry key', 'get system firmware table',
                 'invoke .NET assembly method', 'persist via GinaDLL registry key', 'copy network traffic', 'reference HTTP User-Agent string', 'encrypt data using blowfish', 'start HTTP server',
                 'block operations on executable memory pages using Arbitrary Code Guard', 'get outbound credentials handle via CredSSP', 'capture screenshot', 'get routing table', 'get Windows directory from KUSER_SHARED_DATA',
                 'resolve path using msvcrt', 'linked against XZip', 'get logon sessions', 'encrypt data using RC4 via WinAPI', 'encrypt data using Salsa20 or ChaCha', 'check SystemKernelDebuggerInformation', 'reference the VMWare IO port',
                 'create UDP socket', 'encrypt data using Curve25519', 'spoof parent PID', 'manipulate user privileges', 'encode data using Base64 via WinAPI', 'execute via timer in .NET', 'spawn thread to RWX shellcode',
                 'reference WMI statements', 'enumerate processes on remote desktop session host', 'check for sandbox username or hostname', 'load Windows Common Language Runtime', 'contain an embedded PE file',
                 'get remote cert context via SChannel', 'encrypt data using XTEA', 'obtain TransmitPackets callback function via WSAIoctl', 'query remote server for available data', 'add user account group', 'schedule task via ITaskScheduler',
                 'receive and write data from server to client', 'download and write a file', 'check for debugger via API', 'set UEFI variable', 'manipulate safe mode programs', 'use process replacement', 'mixed mode', 'encrypt data using RSA',
                 'get system web proxy', 'generate random numbers in .NET', 'decode data using Base64 in .NET', 'set web proxy in .NET', 'encrypt data using AES via .NET', 'generate random bytes in .NET', 'decrypt data using RSA',
                 'log keystrokes via Input Method Manager', 'persist via AppInit_DLLs registry key', 'change user account password', 'check ProcessDebugFlags', 'get client handle via SChannel', 'schedule task via at',
                 'reference anti-VM strings targeting Qemu', 'compiled with exe4j', 'continue service', 'enumerate internet cache', 'query or enumerate registry value via StdRegProv', 'check for OutputDebugString error',
                 'access firewall settings via INetFwMgr', 'check for sandbox and av modules', 'get process heap force flags', 'send HTTP request with Host header', 'send TCP data via WFP API', 'execute via asynchronous task in .NET',
                 'compiled with cx_Freeze', 'get Explorer PID', 'generate method via reflection in .NET', 'access WMI data in .NET', 'create raw socket', 'hash data using tiger', 'convert IP address from string', 'linked against libcurl',
                 'register raw input devices', 'reference anti-VM strings targeting VirtualPC', 'monitor local IPv4 address changes', 'receive HTTP request', 'send HTTP response', 'create TCP socket', 'persist via Active Setup registry key',
                 'use .NET library Newtonsoft.Json', 'compress data using GZip in .NET', 'generate random filename in .NET', 'read raw disk data', 'list user accounts for group', 'delete user account group', 'list user account groups',
                 'encrypt data using DES via WinAPI', 'get networking parameters', 'act as TCP client', 'decode data using Base64 via dword translation table', 'list groups for user account', 'import public key', 'delete internet cache',
                 'hijack thread execution', 'bypass Windows File Protection', 'compiled with AutoIt', 'AutoIt is a freeware BASIC-like scripting language designed for automating the Windows GUI.', 'list drag and drop files',
                 'encrypt data using HC-128', 'reference startup folder', 'inject dll', 'deserialize JSON in .NET', 'serialize JSON in .NET', 'list UDP connections and listeners', 'enumerate drives', 'patch process command line',
                 'manually build AES constants', 'create zip archive in .NET', 'extract zip archive in .NET', 'compress data using LZO', 'decompress data using LZO', 'get networking interfaces', 'enumerate devices by category',
                 'clear Windows event logs', 'get OS information via KUSER_SHARED_DATA', 'get proxy', 'capa cannot handle installers well. This means the results may be misleading or incomplete.', 'packaged as a NSIS installer',
                 'packaged as an InstallShield installer', 'set global application hook', 'contain pusha popa sequence', 'start TCP server', 'check ProcessDebugPort', 'compiled with Borland Delphi', 'check for PEB NtGlobalFlag flag',
                 'compiled with MinGW for Windows', 'Single-file deployment allows all the application-dependent files to be bundled into a single binary.', 'packaged as single-file .NET application', 'packaged as an IExpress self-extracting archive',
                 'Visual Basic is a Microsoft programming language that can be compiled to native code or an intermediate', 'compiled from Visual Basic', 'packed with ASPack', 'packaged as an Inno Setup installer', 'send file using FTP',
                 'encrypt data using OpenSSL RSA', 'hash data using RIPEMD320', 'encrypt data using twofish', 'linked against CPP JSON library', 'connect TCP socket', 'check for VM using instruction VPCEXT', 'create reverse shell',
                 'execute .NET assembly', 'encrypt data using Camellia', 'run PowerShell expression', 'compiled with py2exe', 'gather firefox profile information', 'compiled with perl2exe', 'packed with petite', 'encrypt data using OpenSSL ECDSA',
                 'encrypt data using OpenSSL DSA', 'send keystrokes', 'send request in .NET', 'hash data using Whirlpool', 'packed with Pepack', 'check for protected handle exception', 'decode data using URL encoding',
                 'check for trap flag exception', 'gather chrome based browser login information', 'schedule task via ITaskService', 'create virtual file system in .NET', 'linked against Crypto++', 'reference Cloudflare DNS server',
                 'set HTTP User-Agent in .NET', 'hash data using murmur2', 'compile .NET assembly', 'compile CSharp in .NET', 'contain anti-disasm techniques', 'hide thread from debugger', 'free user process memory',
                 'register HTTP server URL', 'get kernel version', 'allocate user process RWX memory', 'execute VBScript Javascript or JScript in memory', 'hash data using SHA512Managed in .NET', 'set HTTP cookie',
                 'initialize IWebBrowser2', 'reference public RSA key', 'write file to startup folder', 'obfuscated with Dotfuscator', 'hash data using RIPEMD128', 'encrypt data using AES MixColumns step', 'hash data using MD4',
                 'execute SQLite statement in .NET', 'terminate process by name', 'bypass Mark of the Web', 'decrypt data via SSPI', 'encrypt data via SSPI', 'clear clipboard data', 'get MAC address in .NET', 'linked against wolfSSL',
                 'check clipboard data', 'create BITS job', 'send data to Internet', 'enumerate browser history', 'display service notification message box', 'get HTTP response content encoding', 'set TCP connection state',
                 'write file on Linux', 'create process via WMI in .NET', 'check if process is running under wine', 'linked against CppSQLite3', 'linked against PolarSSL/mbed TLS', 'decrypt data using TEA', 'read file on Linux',
                 'enumerate system firmware tables', 'encrypt data using Sosemanuk', 'encrypt data using RC6', 'linked against libsodium', 'linked against Microsoft Detours', 'reference OpenDNS DNS server', 'encrypt data using TEA',
                 'check process job object', 'encrypt data using skipjack', 'decompress data using aPLib', 'packed with TSULoader', 'hide the Windows taskbar', 'create File Compression Interface context on Windows',
                 'create File Decompression Interface context on Windows', 'capture process snapshot data', 'packed with VMProtect', 'capture screenshot via keybd event', 'get number of processor cores', 'send email in .NET',
                 'packed with Shrinker', 'decompress data using UCL', 'packaged as a Wise installer', 'power down monitor', 'inject APC', 'packaged as a WinZip self-extracting archive', 'implement COM DLL', 'obfuscated with SmartAssembly',
                 'references logon banner', 'packed with Mpress', 'monitor clipboard content', 'check for unexpected memory writes', 'create VMCI socket', 'act as Security Support Provider DLL', 'persist via ISAPI extension',
                 'reference Quad9 DNS server', 'validate payment card number using luhn algorithm with lookup table', 'linked against Go registry library', 'packed with Themida', 'compiled with AutoHotKey',
                 'AutoHotkey is a free, open-source scripting language for Windows that allows users to easily create scripts.', 'resolve function by hash', 'execute shell command and capture output', 'linked against aPLib',
                 'schedule task via schtasks', 'packed with Confuser', 'extract HTTP body', 'encrypt data using XXTEA', 'simulate CTRL ALT DEL', 'capture screenshot in Go', 'linked against Go WMI library', 'rebuild import table',
                 'make an HTTP request with a Cookie', 'reference Google Public DNS server', '64-bit execution via heavens gate', 'execute shellcode via Windows callback function', 'disable automatic Windows recovery features',
                 'set registry value via StdRegProv', 'log keystrokes via raw input data', 'enumerate minifilter drivers', 'packed with PECompact', 'get HTTP request URI', 'persist via IIS module', 'packed with PESpin', 'obfuscated with Yano',
                 'compiled with ps2exe', 'compiled with Nim', 'reference NCR ATM library routines', 'load NCR ATM library', 'encrypt data using RC4 via SystemFunction032', 'packed with rlpack', 'decompress data via IEncodingFilterFactory',
                 'delete volume shadow copies', 'obfuscated with Babel Obfuscator', 'obfuscated with Spices.Net Obfuscator', 'reference Base58 string', 'packed with enigma', 'packed with nspack', 'act as Excel XLL add-in',
                 'discover Group Policy via gpresult', 'hash data using rshash', 'bypass UAC via token manipulation', 'manipulate CD-ROM drive', 'gather cuteftp information', 'act as Exchange transport agent', 'gather netdrive information',
                 'gather 3d-ftp information', 'gather total-commander information', 'gather global-downloader information', 'gather robo-ftp information', 'gather ffftp information', 'gather direct-ftp information', 'gather frigate3 information',
                 'gather cyberduck information', 'gather nova-ftp information', 'gather classicftp information', 'gather ftpinfo information', 'gather blazeftp information', 'gather softx-ftp information', 'gather coreftp information',
                 'gather bulletproof-ftp information', 'gather turbo-ftp information', 'gather nexusfile information', 'gather ftpshell information', 'gather leapftp information', 'gather bitkinex information', 'gather ftp-explorer information',
                 'gather filezilla information', 'gather southriver-webdrive information', 'gather goftp information', 'gather ftprush information', 'capture public ip', 'compiled from EPL', 'packed with upack', 'inject pe',
                 'create registry key via StdRegProv', 'delete registry key via StdRegProv', 'query or enumerate registry key via StdRegProv', 'delete registry value via StdRegProv', 'linked against CPP HTTP library', 'delete Windows backup catalog',
                 'gather winscp information', 'resolve function by FNV-1a hash', 'packed with Neolite', 'hash data using RIPEMD256', 'packed with Simple Pack', 'packed with pebundle', 'compile Visual Basic in .NET', 'overwrite Master Boot Record',
                 'hash data using jshash', 'packed with MaskPE', 'packaged as a CreateInstall installer', 'impersonate file version information', 'read process memory', 'packed with Perplex', 'reference 114DNS DNS server',
                 'obfuscated with DeepSea Obfuscator', 'gather flashfxp information', 'gather directory-opus information', 'gather freshftp information', 'gather faststone-browser information', 'gather ws-ftp information',
                 'gather ftp-commander information', 'gather ftp-voyager information', 'gather wise-ftp information', 'gather winzip information', 'gather ftpgetter information', 'gather smart-ftp information', 'gather alftp information',
                 'gather securefx information', 'gather ftpnow information', 'gather fling-ftp information', 'gather xftp information', 'gather expandrive information', 'gather ultrafxp information', 'gather staff-ftp information',
                 'gather fasttrack-ftp information', 'extract Cabinet on Windows', 'unmanaged call via dynamic PInvoke in .NET', 'packed with y0da crypter', 'rebuilt by ImpRec', 'encrypt data using RC4 with custom key via WinAPI',
                 'compiled with rust', 'protect spawned processes with mitigation policies', 'check for process debug object', 'enumerate PE sections in .NET', 'bypass UAC via scheduled task environment variable',
                 'disable AppInit_DLLs code signature enforcement', 'check for minimum number of windows on screen', 'enumerate disk properties', 'check for hardware breakpoints', 'get Linux distribution', 'ATT_Tactic_pca1',
                 'ATT_Tactic_pca2', 'ATT_Tech_pca1', 'ATT_Tech_pca2', 'ATT_Tech_pca3', 'ATT_Tech_pca4', 'ATT_Tech_pca5', 'ATT_Tech_pca6', 'MBC_obj_pca1', 'MBC_obj_pca2', 'MBC_behave_pca1', 'MBC_behave_pca2', 'MBC_behave_pca3',
                 'MBC_behave_pca4', 'MBC_behave_pca5', 'MBC_behave_pca6', 'MBC_behave_pca7', 'capability_pca1', 'capability_pca2', 'capability_pca3', 'capability_pca4', 'capability_pca5', 'capability_pca6', 'capability_pca7',
                 'capability_pca8']

#저장한 차원축소 모델 불러오기
# PCA 모델 경로
pca_models_dir = os.path.join(BASE_DIR, 'pca_models', 'pca_models_2024.07.06.pkl')

pca1_dir = os.path.join(BASE_DIR, 'pca_models', 'pcaTactic.pkl')
pca2_dir = os.path.join(BASE_DIR, 'pca_models', 'pcaTech.pkl')
pca3_dir = os.path.join(BASE_DIR, 'pca_models', 'pcaObj.pkl')
pca4_dir = os.path.join(BASE_DIR, 'pca_models', 'pcaBehave.pkl')
pca5_dir = os.path.join(BASE_DIR, 'pca_models', 'pcaCapability.pkl')

# 예측에 사용할 모델의 경로
model_dir = os.path.join(BASE_DIR, 'pca_models', 'model.pkl')


#학습 데이터셋 열 - 모델 보낼 때 각 모델과 함께 이 값을 보내겠습니다.
Model_train_col = ['Entropy','ATT_Tech_pca1', 'ATT_Tech_pca2', 'ATT_Tech_pca3', 'ATT_Tech_pca4', 'ATT_Tech_pca5', 'ATT_Tech_pca6',
                   'ATT_Tactic_pca1', 'ATT_Tactic_pca2','MBC_obj_pca1', 'MBC_obj_pca2','MBC_behave_pca1', 'MBC_behave_pca2',
                   'MBC_behave_pca3', 'MBC_behave_pca4', 'MBC_behave_pca5', 'MBC_behave_pca6', 'MBC_behave_pca7','namespace_persistence',
                   'namespace_linking', 'namespace_compiler', 'namespace_targeting', 'namespace_executable', 'namespace_collection',
                   'namespace_communication', 'namespace_load-code', 'namespace_anti-analysis', 'namespace_data-manipulation', 'namespace_internal',
                   'capability_pca1', 'capability_pca2', 'capability_pca3', 'capability_pca4', 'capability_pca5', 'capability_pca6', 'capability_pca7',
                   'capability_pca8']

#------------예측 데이터셋을 따로 저장하고 싶다면 사용-------------#
'''
#예측 데이터셋 저장할 파일 이름
newFileName="csvProcessingFinal.csv"

#저장 경로 변경에 필요한 라이브러리
import shutil

#현재 경로/newFileName
source_path = '/content/csvProcessingFinal.csv'

#옮길 위치
destination_path = '/content/drive/MyDrive/github2/Git-Study'
'''

#작업경로변경
#os.chdir(f"{work_dir}")

input_df = pd.read_csv(f'{input_dir}',index_col=0) #입력 데이터 불러오기
input_df.reset_index(drop=True,inplace=True) #file_name 열 삭제

if sum(input_df['Entropy'].isna()) : #entropy에 결측치 존재
  print("capa-rule 처리가 비정상적으로 종료하였습니다.")
  raise FileNotFoundError #오류 출력 및 종료

#구현해야할 원핫 인코딩 열 가져오기

ATT_Technique_col = list(filter(lambda x: ('ATT_Technique_' in x),col_checklist))
ATT_Tactic_col = list(filter(lambda x: ('ATT_Tactic_' in x) and (not ('_pca' in x)),col_checklist))
MBC_Object_col = list(filter(lambda x: ('MBC_obj_' in x) and (not ('_pca' in x)),col_checklist))
MBC_Behavior_col = list(filter(lambda x: ('MBC_Behavior_' in x),col_checklist))
namespace_col= list(filter(lambda x: ('namespace_' in x),col_checklist))

capability_col = col_checklist[325:1026]

def process_tactic_column(input_df, ATT_Tactic_col):
    # 결과를 저장할 데이터프레임 초기화
    result_df = pd.DataFrame(0, index=input_df.index, columns=ATT_Tactic_col)
    if not sum(input_df['ATT&CK Tactic'].isna()) :
      for index, row in input_df.iterrows():
          if 'ATT&CK Tactic' in row:
              tactics = row['ATT&CK Tactic'].split(';')
              tactics = [tactic.strip() for tactic in tactics]

              for tactic in tactics:
                  col_name = f'ATT_Tactic_{tactic}'
                  if col_name in ATT_Tactic_col:
                      result_df.at[index, col_name] = 1

    return result_df

#대괄호 안의 항목을 추출하는 함수
def extract_bracket_content(s):
    return re.findall(r'\[([^\]]+)\]', s)

def process_tech_column(input_df, ATT_Tactic_col):
    # 결과를 저장할 데이터프레임 초기화
    result_df = pd.DataFrame(0, index=input_df.index, columns=ATT_Tactic_col)
    for index, row in input_df.iterrows():
        if pd.notna(row['ATT&CK Technique']):
            tactics = row['ATT&CK Technique'].split(';')
            tactics = [tactic.strip() for tactic in tactics]

            for tactic in tactics:
                techniques = extract_bracket_content(tactic)
                for technique in techniques:
                    col_name = f'ATT_Technique_{technique.strip()}'
                    if col_name in ATT_Tactic_col:
                        result_df.at[index, col_name] = 1

    return result_df

def process_obj_column(input_df, ATT_Tactic_col):
    # 결과를 저장할 데이터프레임 초기화
    result_df = pd.DataFrame(0, index=input_df.index, columns=ATT_Tactic_col)
    if not sum(input_df['MBC Objective'].isna()) :
      for index, row in input_df.iterrows():
          if 'MBC Objective' in row:
              tactics = row['MBC Objective'].split(';')
              tactics = [tactic.strip() for tactic in tactics]

              for tactic in tactics:
                  col_name = f'MBC_obj_{tactic}'
                  if col_name in ATT_Tactic_col:
                      result_df.at[index, col_name] = 1

    return result_df

def process_behave_column(input_df, ATT_Tactic_col):
    # 결과를 저장할 데이터프레임 초기화
    result_df = pd.DataFrame(0, index=input_df.index, columns=ATT_Tactic_col)
    for index, row in input_df.iterrows():
        if pd.notna(row['MBC Behavior']):
            tactics = row['MBC Behavior'].split(';')
            tactics = [tactic.strip() for tactic in tactics]

            for tactic in tactics:
                techniques = extract_bracket_content(tactic)
                for technique in techniques:
                    col_name = f'MBC_Behavior_{technique.strip()}'
                    if col_name in ATT_Tactic_col:
                        result_df.at[index, col_name] = 1

    return result_df

def extract_top_directories(s):
    parts = s.split(';')
    return [part.split('/')[0].strip() for part in parts]

def process_namespace_column(namespace):
  result_df = pd.DataFrame(0, index=input_df.index, columns=namespace_col)

  for index, row in input_df.iterrows():
    if pd.notna(row['Namespace']):
      top_dirs = extract_top_directories(row['Namespace'])
      print(top_dirs)
      for top_dir in top_dirs:
        col_name = f'namespace_{top_dir}'
        if col_name in namespace_col:
          result_df.at[index, col_name] += row['Namespace'].count(top_dir)

  return result_df

def process_capability_column(input_df, ATT_Tactic_col):
  result_df = pd.DataFrame(0, index=input_df.index, columns=ATT_Tactic_col)

  for index, row in input_df.iterrows():
    if pd.notna(row['Capability']):
      tactics = row['Capability'].split(';')

      for tactic in tactics:
        if '(' in tactic:
          name, detail = tactic.split('(', 1)
          number_search = re.search(r'\d+', detail)
          if number_search:
            number = int(number_search.group(0))
          else:
            number = 1
        else:
          number = 1
          name=tactic
        name = name.strip()
        if name in ATT_Tactic_col:
          result_df.at[index, name] += number

  return result_df

processed_input = process_tactic_column(input_df, ATT_Tactic_col)
input_df = pd.concat([input_df, processed_input], axis=1)

processed_input = process_tech_column(input_df, ATT_Technique_col)
input_df = pd.concat([input_df, processed_input], axis=1)

processed_input = process_obj_column(input_df, MBC_Object_col)
input_df = pd.concat([input_df, processed_input], axis=1)

processed_input = process_behave_column(input_df, MBC_Behavior_col)
input_df = pd.concat([input_df, processed_input], axis=1)

processed_input = process_namespace_column(namespace_col)
input_df = pd.concat([input_df, processed_input], axis=1)

processed_input = process_capability_column(input_df, capability_col)
input_df = pd.concat([input_df, processed_input], axis=1)

onehot_checklist_col = ['Entropy', 'ATT&CK Tactic', 'ATT&CK Technique', 'MBC Objective', 'MBC Behavior', 'Namespace', 'Capability']
onehot_checklist_col = onehot_checklist_col + ATT_Technique_col + ATT_Tactic_col + MBC_Object_col + MBC_Behavior_col + namespace_col + capability_col

error_list = [x for x in onehot_checklist_col if x not in input_df.columns]

if error_list : #처리 안된거 있으면
  print("데이터 처리가 비정상적으로 종료하였습니다.")
  print("학습데이터셋과 비교했을 때 추가되지 않은 열: ",error_list)
  raise ValueError #오류 출력 및 종료

#원래 col과 맞게 순서 변경
input_df = input_df[onehot_checklist_col]

#PCA모델 불러오기

pca_models = joblib.load(f"{pca_models_dir}")

pca1 = joblib.load(f"{pca1_dir}")
pca2 = joblib.load(f"{pca2_dir}")
pca3 = joblib.load(f"{pca3_dir}")
pca4 = joblib.load(f"{pca4_dir}")
pca5 = joblib.load(f"{pca5_dir}") #pca5 추가

def transform_new_data(pca_models):
    combined_data = input_df.copy()

    # 첫 번째 PCA 변환
    X1 = input_df[ATT_Tactic_col]
    X1_pca = pca1.transform(X1)
    pca_df1 = pd.DataFrame(X1_pca, index=input_df.index,
                           columns=[f"ATT_Tactic_pca{num+1}" for num in range(X1_pca.shape[1])])
    combined_data = pd.concat([combined_data, pca_df1], axis=1)

    # 두 번째 PCA 변환
    X2 = input_df[ATT_Technique_col]
    X2_pca = pca2.transform(X2)
    pca_df2 = pd.DataFrame(X2_pca, index=input_df.index,
                           columns=[f"ATT_Tech_pca{num+1}" for num in range(X2_pca.shape[1])])
    combined_data = pd.concat([combined_data, pca_df2], axis=1)

    # 세 번째 PCA 변환
    X3 = input_df[MBC_Object_col]
    X3_pca = pca3.transform(X3)
    pca_df3 = pd.DataFrame(X3_pca, index=input_df.index,
                           columns=[f"MBC_obj_pca{num+1}" for num in range(X3_pca.shape[1])])
    combined_data = pd.concat([combined_data, pca_df3], axis=1)

    # 네 번째 PCA 변환
    X4 = input_df[MBC_Behavior_col]
    X4_pca = pca4.transform(X4)
    pca_df4 = pd.DataFrame(X4_pca, index=input_df.index,
                           columns=[f"MBC_behave_pca{num+1}" for num in range(X4_pca.shape[1])])
    combined_data = pd.concat([combined_data, pca_df4], axis=1)

    # 다섯 번째 PCA 변환
    X5 = input_df[capability_col]
    X5_pca = pca5.transform(X5)
    pca_df5 = pd.DataFrame(X5_pca, index=input_df.index,
                           columns=[f"capability_pca{num+1}" for num in range(X5_pca.shape[1])])
    combined_data = pd.concat([combined_data, pca_df5], axis=1)

    return combined_data

input_df = transform_new_data(pca_models)

entropy= list(filter(lambda x: ('Entropy' in x),col_checklist))
ATT_Technique_col = list(filter(lambda x: ('ATT_Tech_pca' in x),col_checklist)) #ATT_Technique에서 원핫 후 차원축소한 열 (원핫 열X)
ATT_Tactic_col = list(filter(lambda x: ('ATT_Tactic_pca' in x),col_checklist))
MBC_Object_col = list(filter(lambda x: ('MBC_obj_pca' in x),col_checklist))
MBC_Behavior_col = list(filter(lambda x: ('MBC_behave_pca' in x),col_checklist))
namespace_col = list(filter(lambda x: ('namespace_' in x),col_checklist))
capabilityNum= list(filter(lambda x: ('capability_pca' in x),col_checklist))

selected_columns = [
    input_df[entropy],
    input_df[ATT_Technique_col],
    input_df[ATT_Tactic_col],
    input_df[MBC_Object_col],
    input_df[MBC_Behavior_col],
    input_df[namespace_col],
    input_df[capabilityNum]
]
ftr_df = pd.concat(selected_columns, axis=1)

if sum(ftr_df.isna().any(axis=1)) : #에측에 사용할 데이터셋에 결측치 존재
  print("데이터 처리 작업이 비정상적으로 종료하였습니다.")
  raise FileNotFoundError #오류 출력 및 종료

#두 결과 다 없으면 성공!

#LGBM 학습 데이터셋 열이 담긴 리스트에서, 현재 처리한 데이터셋 열이 담긴 리스트 빼기.
train_sub_df = [x for x in Model_train_col if x not in list(ftr_df.columns)] # Model_train_col - list(ftr_df.columns) : null이여야 한다.


#현재 처리한 데이터셋 열이 담긴 리스트에서, LGBM 학습 데이터셋 열이 담긴 리스트 빼기.
df_sub_train = [x for x in list(ftr_df.columns) if x not in Model_train_col] #list(ftr_df.columns) - Model_train_col : null이여야 한다.


#위에 두 결과 중 하나라도 null이 아니면, 오류를 출력하는 코드
#즉, LGBM 학습 데이터셋 열과 다르면 여기서 오류가 뜬다.

if (train_sub_df + df_sub_train) : #예측에 들어가야 하는 열 중 하나라도 없으면 오류 출력 및 종료
  print("데이터 처리 작업이 비정상적으로 종료하였습니다.")
  print("학습데이터셋과 비교했을 때 다른 열: ",train_sub_df + df_sub_train)

  raise ValueError #오류 출력 및 종료

#순서 맞추기
ftr_df = ftr_df[Model_train_col]

# 데이터 전처리 후 결과를 출력하고 저장
print("데이터 처리 작업이 성공적으로 완료되었습니다.")
print("결과 데이터셋의 일부:")
print(ftr_df.head())

# 결과 데이터프레임을 원본 CSV 파일에 덮어쓰기
ftr_df.to_csv(input_dir, index=False)

print(f"전처리 완료된 데이터가 {input_dir}에 성공적으로 저장되었습니다.")



print(ftr_df)





#모델 불러오기부분으로, 저는 우선 전처리 코드쪽만 완성했습니다. 맨처음 csv돌린 capa를 input_dir에 넣어서 전처리돌리면 그대로 input_dir에 전처리된 결과로 저장됩니다. 


model = joblib.load(f"{model_dir}") #첫번째 인자를 저장한 '모델경로/저장한 모델명'으로 변경!
#모델 예측해보기
result_float = model.predict_proba(ftr_df)
result_int = model.predict(ftr_df)

print('실수 예측값\n',result_float) #실수 예측값 : 순서대로, [ 정상코드일 확률   악성코드일 확률] (ex) [7.40462490e-02 9.25953751e-01] : 악성 92.59...%)
print()
print('정수 예측값\n', result_int) #정수 예측값 : 0 or 1 (0 : 정상, 1 : 악성)
