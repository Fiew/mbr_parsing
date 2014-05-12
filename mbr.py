import argparse
import hexdump
import sys
import re 
from construct import *


mbr = Struct("mbr",
    HexDumpAdapter(Bytes("bootloader_code", 446)),
    Array(4,
        Struct("partitions",
            Enum(Byte("state"),
                INACTIVE = 0x00,
                ACTIVE = 0x80,
            ),
            BitStruct("beginning",
                Octet("head"),
                Bits("sect", 6),
                Bits("cyl", 10),
            ),
            Enum(UBInt8("type"),
                Nothing = 0x00,
                FAT12_CHS = 0x01,
                XENIX_ROOT = 0x02,
                XENIX_USR = 0x03,
                FAT16_16_32MB_CHS = 0x04,
                Extended_DOS = 0x05,
                FAT16_32MB_CHS = 0x06,
                NTFS = 0x07,
                FAT32_CHS = 0x0b,
                FAT32_LBA = 0x0c,
                FAT16_32MB_2GB_LBA = 0x0e,
                Microsoft_Extended_LBA = 0x0f,
                Hidden_FAT12_CHS = 0x11,
                Hidden_FAT16_16_32MB_CHS = 0x14,
                Hidden_FAT16_32MB_2GB_CHS = 0x16,
                AST_SmartSleep_Partition = 0x18,
                Hidden_FAT32_CHS = 0x1b,
                Hidden_FAT32_LBA = 0x1c,
                Hidden_FAT16_32MB_2GB_LBA = 0x1e,
                PQservice = 0x27,
                Plan_9_partition = 0x39,
                PartitionMagic_recovery_partition = 0x3c,
                Microsoft_MBR_Dynamic_Disk = 0x42,
                GoBack_partition = 0x44,
                Novell = 0x51,
                CP_M = 0x52,
                Unix_System_V = 0x63,
                PC_ARMOUR_protected_partition = 0x64,
                Solaris_x86_or_Linux_Swap = 0x82,
                LINUX_NATIVE = 0x83,
                Hibernation = 0x84,
                Linux_Extended = 0x85,
                NTFS_Volume_Set = 0x86,
                BSD_OS = 0x9f,
                FreeBSD = 0xa5,
                OpenBSD = 0xa6,
                Mac_OSX = 0xa8,
                NetBSD = 0xa9,
                Mac_OSX_Boot = 0xab,
                MacOS_X_HFS = 0xaf,
                BSDI = 0xb7,
                BSDI_Swap = 0xb8,
                Boot_Wizard_hidden = 0xbb,
                Solaris_8_boot_partition = 0xbe,
                CP_M_86 = 0xd8,
                Dell_PowerEdge_Server_utilities_FAT_FS = 0xde,
                DG_UX_virtual_disk_manager_partition = 0xdf,
                BeOS_BFS = 0xeb,
                EFI_GPT_Disk = 0xee,
                EFI_System_Partition = 0xef,
                VMWare_File_System = 0xfb,
                VMWare_Swap = 0xfc,
                _default_ = Pass,
            ),
            BitStruct("ending",
                Octet("head"),
                Bits("sect", 6),
                Bits("cyl", 10),
            ),
            UBInt32("sector_offset"), # offset from MBR in sectors
            UBInt32("size"), # in sectors
        )
    ),
    Const(Bytes("signature", 2), "\x55\xAA"),
)




def parse_args():
    parser =argparse.ArgumentParser()
    parser.add_argument("-i", "--image", help="image du disque") 
    return parser.parse_args()


def save_mbr(image):
    # open disk image
    file_image = open(image, "rb")
    file_mbr = open("mbr_", "w")
    # write mbr in file "mbr_"
    file_mbr.write(hexdump.hexdump(file_image.read(512),"return"))
    # open a file to write the hexa part of the mbr whithout spaces
    mbr_hexa = open("parse.txt", "w")
    hex = ""
    # extract the hexa part
    for line in file_mbr.readlines():
        hex = hex + line[10:58]
    hex_withoutSpace = ""
    # delete spaces
    for i in hex.split(" "):
        hex_withoutSpace = hex_withoutSpace+i 
    mbr_hexa.write(hex_withoutSpace)
    file_image.close()
    file_mbr.close()
    mbr_hexa.close()
    return mbr_hexa.name
    
  
    
def main(args):
    
     image = args.image
     file_mbr = save_mbr(image)
     file = open(file_mbr, "rb")
     cap1 = (file.read()).decode("hex")
    
     #print mbr.parse(cap1)
     mbr2 = mbr.parse(cap1)
     for i in range(len(mbr2.partitions)) :
        if mbr2.partitions[i].state == "ACTIVE" :    
            print mbr2.partitions[i]
     
     


main(parse_args())
