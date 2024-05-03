#!/usr/bin/env python3
import os
import sys
import json
import subprocess

def GetPkgName(path):
    deb = subprocess.getoutput(f"dpkg --info '{path}'")
    debPackage = None
    for i in deb.splitlines():
        i = i.strip()
        if i[:9] == "Package: ":
            debPackage = i[9:].strip()
            break
    return debPackage

def GetPkgVersion(path):
    deb = subprocess.getoutput(f"dpkg --info '{path}'")
    debPackage = None
    for i in deb.splitlines():
        i = i.strip()
        if i[:9] == "Version: ":
            debPackage = i[9:].strip()
            break
    return debPackage

def GetPkgArch(path):
    deb = subprocess.getoutput(f"dpkg --info '{path}'")
    debPackage = None
    for i in deb.splitlines():
        i = i.strip()
        if i[:14] == "Architecture: ":
            debPackage = i[14:].strip()
            break
    return debPackage

def GetPkgDes(path):
    deb = subprocess.getoutput(f"dpkg --info '{path}'")
    index = deb.index("Description: ") + 13
    return deb[index:]
    

data = {}
jsonData = []
author = sys.argv[1]
for i in sys.argv[2:]:
    # 归类
    #fileName = os.path.splitext(os.path.basename(i))[0]
    fileName = GetPkgName(i)
    changeName = fileName.replace("linux-image-", "linux-").replace("linux-headers-", "linux-")
    if changeName in data:
        data[changeName].append(i)
    else:
        data[changeName] = [i]
# 处理
for i in data.keys():
    pkgName = []
    version = ""
    arch = ""
    des = ""
    for k in data[i]:
        pkgName.append(GetPkgName(k))
        if version == "":
            version = GetPkgVersion(k)
        if arch == "":
            arch = GetPkgArch(k)
        if des == "":
            des = GetPkgDes(k)
    jsonData.append({
        "Name": i,
        "PkgName": pkgName,
        "System": ["all"],
        "Arch": [arch],
        "Author": author,
        "Des": des,
        "Ver": version
    })
        

print(json.dumps(jsonData, ensure_ascii=False, indent=4))