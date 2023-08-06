
from storage import *
from exception import *
from authkey import *

from PyQt5.QtCore import QByteArray, QDataStream, QBuffer, QFile, QIODevice


class TDesktop:
    def __init__(self) -> None:
        pass
    
    @property
    def passcodeKey(self) -> AuthKey:
        return self.__passcodeKey

    @property
    def localKey(self) -> AuthKey:
        return self.__localKey
        
    @property
    def account_count(self) -> int:
        return self.__account_count

    @property
    def authKey(self) -> AuthKey:
        return self.__authKey

    def FromTData(self, basePath : str, passcode : str = "", keyFile : str = "data") -> None:
        
        # READ KEY_DATA
        keyData = ReadFile("key_" + keyFile, basePath)

        salt, keyEncrypted, infoEncrypted = QByteArray(), QByteArray(), QByteArray()

        keyData.stream >> salt >> keyEncrypted >> infoEncrypted
        if keyData.stream.status() != 0:
            raise OpenTeleException(OpenTeleErrorCode.QDataStreamFailed, "Failed to stream keyData")

        
        self.__passcodeKey = CreateLocalKey(salt, QByteArray(passcode.encode("utf-8")))

        keyInnerData = DecryptLocal(keyEncrypted, self.__passcodeKey)
        self.__localKey = AuthKey(keyInnerData.stream.readRawData(256))

        info = DecryptLocal(infoEncrypted, self.__localKey)
        self.__account_count = info.stream.readInt32()

        mtp = ReadEncryptedFile(ToFilePart(ComputeDataNameKey(keyFile)), basePath, self.__localKey)

        blockId = mtp.stream.readInt32()
        if blockId != 75:
            raise OpenTeleException(OpenTeleErrorCode.FileInvalidMagic, "Not supported file version")

        serialized = QByteArray()
        mtp.stream >> serialized

        stream = QDataStream(serialized)
        stream.setVersion(QDataStream.Version.Qt_5_1)

        UserId = stream.readInt32()
        MainDcId = stream.readInt32()
        
        if ((UserId << 32) | MainDcId) == ~0:
            UserId = stream.readUInt64()
            MainDcId = stream.readInt32()

        if stream.status() != 0:
            raise OpenTeleException(OpenTeleErrorCode.QDataStreamFailed, "Could not read main fields from mtp authorization.")
        
        key_count = stream.readInt32()
        if stream.status() != 0:
            raise OpenTeleException(OpenTeleErrorCode.QDataStreamFailed, "Could not read keys count from mtp authorization.")
        
        for i in range(0, key_count):
            dcId = stream.readInt32()
            keyData = stream.readRawData(256)
            if dcId == MainDcId:
                self.__authKey = AuthKey(keyData, AuthKey.Type.ReadFromFile, dcId)
                break
            
        # while (not mtp.stream.atEnd()):
        #     blockId = mtp.stream.readInt32()
        #     if mtp.stream.status() != 0:
        #         raise OpenTeleException(OpenTeleErrorCode.QDataStreamFailed, "Failed to stream mtpData")
        #     print(blockId)
    
