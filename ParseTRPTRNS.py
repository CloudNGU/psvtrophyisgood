import binascii
import ParseTRPSFM
def init(path):
    global trpData
    global readPath
    readPath = path
    trpData = open(path, "rb").read()

def getAccountId():
    return binascii.hexlify(trpData[0x120:0x120+0x8])

def makeCmaAid(aid):
    cmaAid = [aid[i:i + 2] for i in range(0, len(aid), 2)]
    cmaAid.reverse()
    return str(cmaAid)
def getNumberOfUnlockedTrophies():
    return int(str(binascii.hexlify(trpData[0x187:0x187+0x1])),16)

def getNpCommId():
    return trpData[0x170:0x170 + 0x0C]

def getNpCommSign():
    return binascii.hexlify(trpData[0x190:0x22f])

def findDataZone(v):
        begin = 0x2B7
        end = begin + 0xAC
        a = 0
        while a != v:
            begin += 0xAC +0x04
            end = begin + 0xAC
            a += 1
        return {"begin":begin,"end":end}

def getTrophyDataBlock(v):
    begin = findDataZone(v)["begin"]
    end = findDataZone(v)["end"]
    return binascii.hexlify(trpData[begin:end])

def writeTimestamp(v,timestamp):
    origTrophyDataBlock = binascii.unhexlify(getTrophyDataBlock(v))
    ts = parseTrophyDataBlock(v)["timestamp"]
    trophyDataBlock = origTrophyDataBlock.replace(binascii.unhexlify(ts[0]),binascii.unhexlify(timestamp))
    trophyDataBlock = trophyDataBlock.replace(binascii.unhexlify(ts[1]),binascii.unhexlify(timestamp))
    trpData = open(readPath, "rb").read()
    trpData = trpData.replace(origTrophyDataBlock,trophyDataBlock)
    open(readPath,"wb").write(trpData)

def setAccountId(aid):
    origAid = getAccountId()
    trpData = open(readPath, "rb").read()
    trpData = trpData.replace(binascii.unhexlify(origAid),binascii.unhexlify(aid))
    open(readPath, "wb").write(trpData)

def unlockTrophy(v):
    npCommId = getNpCommId()
    ParseTRPSFM.init("conf/"+npCommId+"/TROP.SFM")
    grade = ParseTRPSFM.parseTrophyData(v)["grade"]
    if grade == "P":
        grade = "01"
    elif grade == "G":
        grade = "02"
    elif grade == "S":
        grade = "03"
    elif grade == "B":
        grade = "04"
    origTrophyDataBlock = getTrophyDataBlock(v)
    a = origTrophyDataBlock[96+2:]
    b = origTrophyDataBlock[:96]
    trophyDataBlock = b + grade + a
    a = trophyDataBlock[32+2:]
    b = trophyDataBlock[:32]
    trophyDataBlock = b + "02" + a
    trpData = open(readPath, "rb").read()
    trpData = trpData.replace(binascii.unhexlify(origTrophyDataBlock),binascii.unhexlify(trophyDataBlock))
    open(readPath,"wb").write(trpData)



def lockTrophy(v):
    npCommId = getNpCommId()
    idInHex = hex(v)[2:]
    if len(idInHex) != 2:
        idInHex = "0"+idInHex
    trophyDataBlock = "a00000000000000000000000"+idInHex+"000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002"
    trpData = open(readPath, "rb").read()
    trpData = trpData.replace(binascii.unhexlify(getTrophyDataBlock(v)),binascii.unhexlify(trophyDataBlock))
    open(readPath,"wb").write(trpData)


def parseTrophyDataBlock(v):
    trophyDataBlock = getTrophyDataBlock(v)
    trophyType = trophyDataBlock[96:96 + 2]
    if trophyType == "01":
        trophyType = "P"
    elif trophyType == "02":
        trophyType = "G"
    elif trophyType == "03":
        trophyType = "S"
    elif trophyType == "04":
        trophyType = "B"
    else:
        trophyType = "Unknown"
    unlocked = trophyDataBlock[32:32+2]
    if unlocked == "02":
        unlocked = True
    elif unlocked == "00":
        unlocked = False
    else:
        unlocked = "Unknown"
    timestamp = [0,0]
    timestamp[0] = trophyDataBlock[116:116+14]
    timestamp[1] = trophyDataBlock[132:132+14]

    return {"grade":trophyType,"unlocked":unlocked,"timestamp":timestamp}

