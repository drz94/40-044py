# This Python file uses the following encoding: utf-8
# if__name__ == "__main__":
#     pass
_END     =0xC0
_ESC     =0xDB
_ESC_END =0xDC
_ESC_ESC =0xDD


_PING    =0
_INIT    =1
_ACK     =2
_NAK     =3
_GET     =4
_PUT     =5
_READ    =6
_WRITE   =7
_ID      =8
_FASTGET =10
_IDN     =20

Crc16Table = [0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7,
0x8108, 0x9129, 0xA14A, 0xB16B, 0xC18C, 0xD1AD, 0xE1CE, 0xF1EF,
0x1231, 0x0210, 0x3273, 0x2252, 0x52B5, 0x4294, 0x72F7, 0x62D6,
0x9339, 0x8318, 0xB37B, 0xA35A, 0xD3BD, 0xC39C, 0xF3FF, 0xE3DE,
0x2462, 0x3443, 0x0420, 0x1401, 0x64E6, 0x74C7, 0x44A4, 0x5485,
0xA56A, 0xB54B, 0x8528, 0x9509, 0xE5EE, 0xF5CF, 0xC5AC, 0xD58D,
0x3653, 0x2672, 0x1611, 0x0630, 0x76D7, 0x66F6, 0x5695, 0x46B4,
0xB75B, 0xA77A, 0x9719, 0x8738, 0xF7DF, 0xE7FE, 0xD79D, 0xC7BC,
0x48C4, 0x58E5, 0x6886, 0x78A7, 0x0840, 0x1861, 0x2802, 0x3823,
0xC9CC, 0xD9ED, 0xE98E, 0xF9AF, 0x8948, 0x9969, 0xA90A, 0xB92B,
0x5AF5, 0x4AD4, 0x7AB7, 0x6A96, 0x1A71, 0x0A50, 0x3A33, 0x2A12,
0xDBFD, 0xCBDC, 0xFBBF, 0xEB9E, 0x9B79, 0x8B58, 0xBB3B, 0xAB1A,
0x6CA6, 0x7C87, 0x4CE4, 0x5CC5, 0x2C22, 0x3C03, 0x0C60, 0x1C41,
0xEDAE, 0xFD8F, 0xCDEC, 0xDDCD, 0xAD2A, 0xBD0B, 0x8D68, 0x9D49,
0x7E97, 0x6EB6, 0x5ED5, 0x4EF4, 0x3E13, 0x2E32, 0x1E51, 0x0E70,
0xFF9F, 0xEFBE, 0xDFDD, 0xCFFC, 0xBF1B, 0xAF3A, 0x9F59, 0x8F78,
0x9188, 0x81A9, 0xB1CA, 0xA1EB, 0xD10C, 0xC12D, 0xF14E, 0xE16F,
0x1080, 0x00A1, 0x30C2, 0x20E3, 0x5004, 0x4025, 0x7046, 0x6067,
0x83B9, 0x9398, 0xA3FB, 0xB3DA, 0xC33D, 0xD31C, 0xE37F, 0xF35E,
0x02B1, 0x1290, 0x22F3, 0x32D2, 0x4235, 0x5214, 0x6277, 0x7256,
0xB5EA, 0xA5CB, 0x95A8, 0x8589, 0xF56E, 0xE54F, 0xD52C, 0xC50D,
0x34E2, 0x24C3, 0x14A0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
0xA7DB, 0xB7FA, 0x8799, 0x97B8, 0xE75F, 0xF77E, 0xC71D, 0xD73C,
0x26D3, 0x36F2, 0x0691, 0x16B0, 0x6657, 0x7676, 0x4615, 0x5634,
0xD94C, 0xC96D, 0xF90E, 0xE92F, 0x99C8, 0x89E9, 0xB98A, 0xA9AB,
0x5844, 0x4865, 0x7806, 0x6827, 0x18C0, 0x08E1, 0x3882, 0x28A3,
0xCB7D, 0xDB5C, 0xEB3F, 0xFB1E, 0x8BF9, 0x9BD8, 0xABBB, 0xBB9A,
0x4A75, 0x5A54, 0x6A37, 0x7A16, 0x0AF1, 0x1AD0, 0x2AB3, 0x3A92,
0xFD2E, 0xED0F, 0xDD6C, 0xCD4D, 0xBDAA, 0xAD8B, 0x9DE8, 0x8DC9,
0x7C26, 0x6C07, 0x5C64, 0x4C45, 0x3CA2, 0x2C83, 0x1CE0, 0x0CC1,
0xEF1F, 0xFF3E, 0xCF5D, 0xDF7C, 0xAF9B, 0xBFBA, 0x8FD9, 0x9FF8,
0x6E17, 0x7E36, 0x4E55, 0x5E74, 0x2E93, 0x3EB2, 0x0ED1, 0x1EF0
]

def TableCRC16(pcBlock):
    crc = 0xFFFF;
    i = 0
    length = len(pcBlock)
    while length > 0:
        crc = ((crc << 8) ^ Crc16Table[(crc >> 8) ^ pcBlock[i]]) & 0xFFFF
        i = i + 1
        length = length - 1
    return crc

def RFC_Tx(tx_buff):
    """
    The function adds _END on each side of a message
    and manages _END _ECS cases inside
    """
    out_buf_tx = []
    out_buf_tx.append(_END)

    for i in range(len(tx_buff)):
        if (tx_buff[i] == _END):
            out_buf_tx.append(_ESC)
            out_buf_tx.append(_ESC_END)
        else:
            if (tx_buff[i] == _ESC):
                out_buf_tx.append(_ESC)
                out_buf_tx.append( _ESC_ESC)
            else:
                out_buf_tx.append(tx_buff[i])

    out_buf_tx.append( _END)
    return out_buf_tx


def SSP_WRITE(dest, src, adr, data):
    out_buf = []
    out_buf.append(dest)
    out_buf.append(src)
    out_buf.append(_WRITE)
    out_buf.append(adr)
    out_buf.append(adr >> 8)
    out_buf.append(adr >> 16)
    out_buf.append(adr >> 24)
    out_buf.extend(data)

    crc = TableCRC16(out_buf)
    out_buf.append(crc&0xFF)
    out_buf.append((crc>>8)&0xFF)

    out_buf = RFC_Tx(out_buf)
	

    return out_buf

def SSP_PUT(dest, src, adr, data):  
    out_buf = []
    out_buf.append(dest)
    out_buf.append(src)
    out_buf.append(_PUT)
    out_buf.append(adr)
    out_buf.append(adr >> 8)
    out_buf.extend(data)
    crc = TableCRC16(out_buf)
    out_buf.append(crc&0xFF)
    out_buf.append((crc>>8)&0xFF)
    out_buf = RFC_Tx(out_buf)

    return out_buf
	
def SSP_PING(dest, src):  
    out_buf = []
    out_buf.append(dest)
    out_buf.append(src)
    out_buf.append(_PING)
    crc = TableCRC16(out_buf)
    out_buf.append(crc&0xFF)
    out_buf.append((crc>>8)&0xFF)
    out_buf = RFC_Tx(out_buf) 
    return out_buf
def guess(name):
    selfAdr = 0
    sspAdr = 0
    if (name.find("bias") != -1):
        if (name.find("GyroX") != -1): selfAdr,sspAdr = 101, 21
        if (name.find("GyroY") != -1): selfAdr,sspAdr = 102, 21
        if (name.find("GyroZ") != -1): selfAdr,sspAdr = 103, 21

        if (name.find("AccelX") != -1):selfAdr,sspAdr = 100, 24
        if (name.find("AccelY") != -1):selfAdr,sspAdr = 100, 25
        if (name.find("AccelZ") != -1):selfAdr,sspAdr = 100, 26

    if (name.find("grad") != -1):
        if (name.find("GyroX") != -1): selfAdr,sspAdr = 101, 27
        if (name.find("GyroY") != -1): selfAdr,sspAdr = 102, 27
        if (name.find("GyroZ") != -1): selfAdr,sspAdr = 103, 27

    if (name.find("scale") != -1):
        if (name.find("GyroX") != -1): selfAdr,sspAdr = 101, 24
        if (name.find("GyroY") != -1): selfAdr,sspAdr = 102, 24
        if (name.find("GyroZ") != -1): selfAdr,sspAdr = 103, 24

        if (name.find("AccelX") != -1):selfAdr,sspAdr = 100, 21
        if (name.find("AccelY") != -1):selfAdr,sspAdr = 100, 22
        if (name.find("AccelZ") != -1):selfAdr,sspAdr = 100, 23

    return (selfAdr,sspAdr)

def guess_adr(tb,ch):
    if (tb == 0 and ch == 0): return (24) #BG X
    if (tb == 0 and ch == 1): return (25) #BG Y
    if (tb == 0 and ch == 2): return (26) #BG Z

    if (tb == 1 and ch == 0): return (21) #SFEG X
    if (tb == 1 and ch == 1): return (22) #SFEG Y
    if (tb == 1 and ch == 2): return (23) #SFEG Z

    if (tb == 2 and ch == 3): return (36) #MG XY
    if (tb == 2 and ch == 4): return (39) #MG XZ
    if (tb == 2 and ch == 5): return (37) #MG YX
    if (tb == 2 and ch == 6): return (40) #MG YZ
    if (tb == 2 and ch == 7): return (38) #MG ZX
    if (tb == 2 and ch == 8): return (41) #MG ZY

    if (tb == 3 and ch == 0): return (27) #gr X
    if (tb == 3 and ch == 1): return (28) #gr Y
    if (tb == 3 and ch == 2): return (29) #gr Z

    if (tb == 4 and ch == 0): return (33) #BA X
    if (tb == 4 and ch == 1): return (34) #BA Y
    if (tb == 4 and ch == 2): return (35) #BA Z

    if (tb == 5 and ch == 0): return (30) #SFEA X
    if (tb == 5 and ch == 1): return (31) #SFEA Y
    if (tb == 5 and ch == 2): return (32) #SFEA Z

    if (tb == 6 and ch == 3): return (42) #MA XY
    if (tb == 6 and ch == 4): return (45) #MA XZ
    if (tb == 6 and ch == 5): return (43) #MA YX
    if (tb == 6 and ch == 6): return (46) #MA YZ
    if (tb == 6 and ch == 7): return (44) #MA ZX
    if (tb == 6 and ch == 8): return (47) #MA ZY
    else: return("unsupported")

