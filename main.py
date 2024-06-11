__author__ = 'Elhanan'
import decompiler_asm
import sys

FIRST_PARAM = 1

if len(sys.argv) > 1:
    address = sys.argv[FIRST_PARAM]
else:
    address = raw_input('address of file: ')

decompiler_asm.main('main.txt',0,address)
