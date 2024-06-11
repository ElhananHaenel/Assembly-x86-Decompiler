__author__ = 'Elhanan'

import sys


print_reg = {

    '0': 'al',
    '1': 'cl',
    '2': 'dl',
    '3': 'bl',
    '4': 'ah',
    '5': 'ch',
    '6': 'dh',
    '7': 'bh',
    '8': 'ax',
    '9': 'cx',
    '10': 'dx',
    '11': 'bx',
    '12': 'sp',
    '13': 'bp',
    '14': 'si',
    '15': 'bi'

}

print_only_db_reg = {
    '0': 'ax',
    '1': 'cx',
    '2': 'dx',
    '3': 'bx',
    '4': 'sp',
    '5': 'bp',
    '6': 'si',
    '7': 'bi'
}

print_only_b_reg = {

    '0': 'al',
    '1': 'cl',
    '2': 'dl',
    '3': 'bl',
    '4': 'ah',
    '5': 'ch',
    '6': 'dh',
    '7': 'bh',


}

pecoda_80 = {

    '0': 'add',
    '1': 'or',
    '2': 'sbb',
    '3': 'bl',
    '4': 'and',
    '5': 'sub',
    '6': 'xor',
    '7': 'cmp',

}

pecoda_f6 = {

    '0': 'test',
    '2': 'not',
    '3': 'neg',
    '4': 'mul',
    '5': 'imul',
    '6': 'div',
    '7': 'idiv',

}

register_with_speciel_register = {

    '0': 'ax',
    '1': 'cx',
    '2': 'dx',
    '3': 'bx',
    '4': 'sp',
    '5': 'bp',
    '6': 'si',
    '7': 'di',

}

pecoda_ff = {

    '0': 'inc',
    '1': 'dec',
    '2': 'call',
    '3': 'neg',
    '4': 'jmp',
    '5': 'jmp',
    '6': 'push  ',

}

print_type_jmp = {

    '0': 'jo ',
    '1': 'jno ',
    '2': 'jb ',
    '3': 'jnb ',
    '4': 'jz ',
    '5': 'jne ',
    '6': 'jna ',
    '7': 'ja ',
    '8': 'js ',
    '9': 'jns ',
    '10': 'jp ',
    '11': 'jpo ',
    '12': 'jl ',
    '13': 'jnl ',
    '14': 'gng ',
    '15': 'jg ',

}

start_jmp = 233
end_jmp = 236

function = {}

counter = 0
num_byte = 0

# input_file_write.write('mov')


def counter_and_one_byte(input_file):  #return one byte of the input file and ++counter
    global counter
    global num_byte
    counter += 1
    num_byte += 1
    return input_file.read(1)


def mov(register, input_file_write, order, input_file,
        all_the_byte):  #checing the type of mov and send us to the right function
    input_file_write.write('mov ')

    if order == '128':  #two register

        cheking_register(register, input_file_write, input_file, order, all_the_byte)
    elif order == '160':  #ax or Al to memory
        ax_memory(register, input_file_write, input_file)

    elif order == '192':
        bit = counter_and_one_byte(input_file)
        if all_the_byte == '198':
            register = '0'
        only_memory(register, input_file_write, input_file, bit)

    else:

        if (int(register) >= 0 and int(register) < 8):

            first = counter_and_one_byte(input_file)
            num = str(ord(first))
            what_to_print = print_reg[register]
            input_file_write.write(what_to_print + ",")
            input_file_write.write(num)
        else:

            first = counter_and_one_byte(input_file)
            secend = counter_and_one_byte(input_file)
            num = str(ord(secend) * 256 + ord(first))

            what_to_print = print_reg[register]
            input_file_write.write(what_to_print + ",")
            input_file_write.write(num)


def pecodot1(register, input_file_write, order, input_file, all_the_byte):  #cheking the command after te first indexing

    pecoda = str(int(all_the_byte) >> 3 & 15)
    input_file_write.write(pecoda_80[pecoda] + ' ')
    register = str(int(register) & 7)

    if register == '4' or register == '5':  #al or ax

        number_to_ax_or_al(register, input_file_write, input_file)
    else:
        bit = counter_and_one_byte(input_file)
        register = str(int(register) & 7)

        if register == '0' or register == '2':
            semi_register_to_or_memory(input_file_write, input_file, bit, register)
        elif register == '1' or register == '3':
            register_to_or_memory(input_file_write, input_file, bit, register)


def cheking_register(register, input_file_write, input_file, order,
                     all_the_byte):  # cheking the parametr after the command, register and memory byte. and send us to the right function
    bit = counter_and_one_byte(input_file)

    if all_the_byte == '139' and ord(bit) >> 6 == 3:  #db
        print_for_db(input_file_write, input_file, bit)
    elif all_the_byte == '138' and ord(bit) >> 6 == 3:  #b
        print_for_b(input_file_write, input_file, bit)
    elif all_the_byte == '137' or all_the_byte == '139':  #memory to register or extange
        print_for_memory_to_register_without_ax(input_file_write, input_file, bit, all_the_byte)
    elif all_the_byte == '136' or all_the_byte == '138':  #memory to semi register or extange
        print_for_memory_to_semi_register_without_ax(input_file_write, input_file, bit, all_the_byte)


def print_for_db(input_file_write, input_file, bit): #cheking the register DB
    #split the bit - to know the rejex i need to write

    first_reg = str(ord(bit) & 7)
    secend_reg = str((ord(bit) & 56) >> 3)

    input_file_write.write(print_only_db_reg[secend_reg] + ',')

    input_file_write.write(print_only_db_reg[first_reg])


def print_for_b(input_file_write, input_file, bit): #cheking the register b
    #split the bit - to know the rejex i need to write

    first_reg = str(ord(bit) & 7)
    secend_reg = str((ord(bit) & 56) >> 3)

    input_file_write.write(print_only_b_reg[secend_reg] + ',')

    input_file_write.write(print_only_b_reg[first_reg])


def print_for_memory_to_register_without_ax(input_file_write, input_file, bit, all_the_byte): #cheking the register db and memory byte
    secend_reg = str((ord(bit) & 56) >> 3)
    next_bit = counter_and_one_byte(input_file)
    next_bit2 = counter_and_one_byte(input_file)
    memory_stack = str(ord(next_bit2) * 256 + ord(next_bit))
    if all_the_byte == '137':  #memory to register
        input_file_write.write('[' + memory_stack + ']' + ',')
        input_file_write.write(print_only_db_reg[secend_reg])
    else:
        input_file_write.write(print_only_db_reg[secend_reg] + ',')
        input_file_write.write('[' + memory_stack + ']')


def print_for_memory_to_semi_register_without_ax(input_file_write, input_file, bit, all_the_byte):#cheking the register b and memory byte
    secend_reg = str((ord(bit) & 56) >> 3)
    next_bit = counter_and_one_byte(input_file)
    next_bit2 = counter_and_one_byte(input_file)
    memory_stack = str(ord(next_bit2) * 256 + ord(next_bit))
    if all_the_byte == '137':  #memory to register
        input_file_write.write('[' + memory_stack + ']' + ',')
        input_file_write.write(print_only_b_reg[secend_reg])
    else:
        input_file_write.write(print_only_b_reg[secend_reg] + ',')
        input_file_write.write('[' + memory_stack + ']')


def ax_memory(register, input_file_write, input_file): #cheking the oederof the ax rgister and the memory
    first = counter_and_one_byte(input_file)
    secend = counter_and_one_byte(input_file)
    num = str(ord(secend) * 256 + ord(first))

    if register == '0' or register == "2":

        if register == '0':
            input_file_write.write('al,[' + num + ']')
        else:
            input_file_write.write('[' + num + '],al')
    else:

        if register == '1':
            input_file_write.write('ax,[' + num + ']')
        else:
            input_file_write.write('[' + num + '],ax')


def only_memory(register, input_file_write, input_file, bit): #checing if register or memory
    if str((ord(bit)) >> 6) == '0':
        next_bit = counter_and_one_byte(input_file)
        next_bit2 = counter_and_one_byte(input_file)
        memory_stack = str(ord(next_bit2) * 256 + ord(next_bit))
        if register == '0' or register == '3':  #memory bite

            first = counter_and_one_byte(input_file)
            input_file_write.write('[' + memory_stack + '],' + str(ord(first)))
        else:
            first = counter_and_one_byte(input_file)
            secend = counter_and_one_byte(input_file)
            num = str(ord(secend) * 256 + ord(first))
            input_file_write.write('[' + memory_stack + '],' + num)
    elif str((ord(bit)) >> 6) == '3':

        if register == '0':
            number_to_semi_register(bit, input_file_write, input_file)
        elif register == '1':
            two_byte_number_to_register(bit, input_file_write, input_file)
        elif register == '3':

            byte_number_to_register(bit, input_file_write, input_file)


def number_to_ax_or_al(register, input_file_write, input_file): #cheking if number to ax or al t
    first = counter_and_one_byte(input_file)
    secend = counter_and_one_byte(input_file)
    num = str(ord(secend) * 256 + ord(first))
    if register == '4':

        input_file_write.write('al,' + num)

    elif register == '5':
        input_file_write.write('ax,' + num)


def cheking_pecoda(register, input_file_write, input_file): #cheking the command after te first indexing
    bit = counter_and_one_byte(input_file)
    pecoda = str((ord(bit) & 56) >> 3)
    input_file_write.write(pecoda_80[pecoda] + ' ')
    only_memory(register, input_file_write, input_file, bit)


def number_to_semi_register(bit, input_file_write, input_file): #cheking register and number
    reg = str(ord(bit) & 7)
    first = counter_and_one_byte(input_file)
    num = str(ord(first))
    input_file_write.write(print_only_b_reg[reg] + "," + num)


def two_byte_number_to_register(bit, input_file_write, input_file): #cheking register and number
    reg = str(ord(bit) & 7)
    first = counter_and_one_byte(input_file)
    secend = counter_and_one_byte(input_file)
    num = str(ord(secend) * 256 + ord(first))
    input_file_write.write(print_only_db_reg[reg] + "," + num)


def byte_number_to_register(bit, input_file_write, input_file): #cheking register and number
    reg = str(ord(bit) & 7)
    first = counter_and_one_byte(input_file)
    num = str(ord(first))
    input_file_write.write(print_only_db_reg[reg] + "," + num)


def cheking_pecoda_2(register, input_file_write, input_file): #cheking the command after te first indexing
    bit = counter_and_one_byte(input_file)
    pecoda = str((ord(bit) & 56) >> 3)
    input_file_write.write(pecoda_f6[pecoda] + ' ')
    if int(pecoda) >= 2 and int(pecoda) < 7:
        only_one_register_or_one_memory(register, input_file_write, input_file, bit)
    else:
        only_memory(register, input_file_write, input_file, bit)


def only_one_register_or_one_memory(register, input_file_write, input_file, bit):#checing register or memory byte
    if str((ord(bit)) >> 6) == '0':
        print 3
        next_bit = counter_and_one_byte(input_file)
        next_bit2 = counter_and_one_byte(input_file)
        memory_stack = str(ord(next_bit2) * 256 + ord(next_bit))
        input_file_write.write('[' + memory_stack + ']')
    else:

        reg = str(ord(bit) & 7)
        input_file_write.write(print_only_b_reg[reg])


def split_between_inc_and_dec(register, input_file_write, order, input_file, all_the_byte): #cheking if the command is inc or dec
    if int(register) < 8:
        input_file_write.write("inc ")
    else:
        input_file_write.write("dec ")

    register = str(int(register) & 7)
    input_file_write.write(register_with_speciel_register[register])


def cheking_pecoda_3(register, input_file_write, input_file):#cheking the command after te first indexing
    bit = counter_and_one_byte(input_file)
    pecoda = str((ord(bit) & 56) >> 3)
    input_file_write.write(pecoda_ff[pecoda] + ' ')
    only_one_register_or_one_memory(register, input_file_write, input_file, bit)


def print_jmp(register, input_file_write, input_file): #cheking type of jmp
    input_file_write.write('jmp ')
    if register == '11':
        print_Relative_Short_Displacement(input_file_write, input_file)
    elif register == '9':
        print_loction_db(input_file_write, input_file)

    elif register == '12':
        #print_far_loction(input_file_write, input_file)
        print 1


def print_Relative_Short_Displacement(input_file_write, input_file): #print the loction of he jmp
    first = counter_and_one_byte(input_file)

    if str((ord(first)) >> 7) == '1':
        byts = (0 - (((ord(first)) ^ 255) + 1))

        input_file_write.write(str(byts))
    else:
        input_file_write.write(str((ord(first))))


def print_loction_db(input_file_write, input_file): #print loction
    location = counter_and_one_byte(input_file)
    location2 = counter_and_one_byte(input_file)
    location_db = str(ord(location2) * 256 + ord(location))
    input_file_write.write('[' + location_db + ']')


def print_int(input_file_write, input_file): #print the type of the interup
    input_file_write.write('int ')
    first = counter_and_one_byte(input_file)
    first = str(ord(first))
    input_file_write.write(str(hex(int(first)))[2::] + 'h')


def semi_register_to_or_memory(input_file_write, input_file, bit, register): #checking if register or memory byte
    if ord(bit) >> 6 == 0:
        secend_reg = str((ord(bit) & 56) >> 3)
        next_bit = counter_and_one_byte(input_file)
        next_bit2 = counter_and_one_byte(input_file)
        memory_stack = str(ord(next_bit2) * 256 + ord(next_bit))
        if register == '0':

            input_file_write.write('[' + memory_stack + ']' + ',')
            input_file_write.write(print_only_b_reg[secend_reg])


        else:
            input_file_write.write(print_only_b_reg[secend_reg] + ',')
            input_file_write.write('[' + memory_stack + ']')

    else:
        print_for_b(input_file_write, input_file, bit)


def register_to_or_memory(input_file_write, input_file, bit, register): #registery to memory byte or exstcange
    if ord(bit) >> 6 == 0:
        secend_reg = str((ord(bit) & 56) >> 3)
        next_bit = counter_and_one_byte(input_file)
        next_bit2 = counter_and_one_byte(input_file)
        memory_stack = str(ord(next_bit2) * 256 + ord(next_bit))
        if register == '1':

            input_file_write.write('[' + memory_stack + ']' + ',')
            input_file_write.write(print_only_db_reg[secend_reg])


        else:
            input_file_write.write(print_only_db_reg[secend_reg] + ',')
            input_file_write.write('[' + memory_stack + ']')

    else:

        print_for_db(input_file_write, input_file, bit)


def cheking_kind_cmp(all_the_byte, register, input_file, input_file_write): #cheking comper
    bit = counter_and_one_byte(input_file)
    register = str(int(register) & 7)

    if register == '0' or register == '2':
        semi_register_to_or_memory(input_file_write, input_file, bit, register)
    elif register == '1' or register == '3':
        register_to_or_memory(input_file_write, input_file, bit, register)


def call_fun(address, input_file, input_file_write): #print call
    global counter
    input_file_write.write('call ')
    location = counter_and_one_byte(input_file)
    location2 = counter_and_one_byte(input_file)
    location_db = str(ord(location2) * 256 + ord(location))
    if str((int(location_db)) >> 15) == '1':
        byts = (0 - (((int(location_db)) ^ 65535) + 1))

    else:
        byts = int(location_db)
    location_db = byts + counter + 1
    x = str(location_db)
    y = counter
    input_file_write.write('[' + x + ']')
    if location_db not in function:
        fnt_path = 'function_' + x + '.txt'
        main(fnt_path, location_db, address)
    counter = y


def main(fnt_path, num_to_down, address):
    #address = r'C:\gvahim\assembly\dosbox\WORK\peroj\pacman.com'
    #address = r'C:\gvahim\assembly\dosbox\peroject\try1.com'

    input_file = open(address, 'rb')

    #print file
    input_file_write = input_file_write2 = open(fnt_path, 'w')
    input_file_write.write("; Disassembly output by Elhanan\r\n")
    num_of_function = fnt_path.split(".")
    input_file_write.write("; " + num_of_function[0] + "\r\n")

    global num_byte, counter
    counter = num_to_down - 1

    if num_to_down != 0:
        y = input_file.read(num_to_down - 1)
        counter = num_to_down - 1
    else:
        counter = 0

    byte = counter_and_one_byte(input_file)

    all_the_byte = ord(byte)

    all_the_byte = str(all_the_byte)

    order = str(ord(byte) & 240)
    register = str(ord(byte) & 15)
    #print order
    #print for_and





    while byte != 195:
        #mov
        if (order == '176') or ((order == '128') and int(register) > 6 and int(register) < 13) or (
                        (order == '160') and (int(register) >= 0 and int(register) < 5) or (
                                (order == '192') and int(register) > 5 and int(register) < 8) ):

            mov(register, input_file_write, order, input_file, all_the_byte)

        elif all_the_byte == '232':  # call
            call_fun(address, input_file, input_file_write)



        elif int(all_the_byte) >= 56 and int(all_the_byte) < 60:  #cmp

            input_file_write.write('cmp ')
            cheking_kind_cmp(all_the_byte, register, input_file, input_file_write)

        elif int(all_the_byte) >= 0 and int(all_the_byte) < 62:  #looc in dicton..pecodot1

            pecodot1(register, input_file_write, order, input_file, all_the_byte)

        elif all_the_byte == '128' or all_the_byte == '129' or all_the_byte == '131':

            cheking_pecoda(register, input_file_write, input_file)

        elif all_the_byte == '246' or all_the_byte == '247':  #div mul...
            cheking_pecoda_2(register, input_file_write, input_file)

        elif order == '64':  #dec,inc
            split_between_inc_and_dec(register, input_file_write, order, input_file, all_the_byte)

        elif all_the_byte == '254' or all_the_byte == '255':
            cheking_pecoda_3(register, input_file_write, input_file)

        elif int(all_the_byte) >= 233 and int(all_the_byte) < 236:  #jmp
            print_jmp(register, input_file_write, input_file)

        elif order == '112' and (int(register) > 0 and int(register) < 15):  #type of jmp
            input_file_write.write(print_type_jmp[register])
            print_Relative_Short_Displacement(input_file_write, input_file)

        elif all_the_byte == '205':  #int
            print_int(input_file_write, input_file)

        elif all_the_byte == '141':  #lea
            input_file_write.write('lea ')
            bit = counter_and_one_byte(input_file)
            only_memory(register, input_file_write, input_file, bit)

        elif order == '80' and int(register) >= 0 and int(register) < 8:
            input_file_write.write('push ')

            input_file_write.write(register_with_speciel_register[register])

        elif order == '80' and int(register) > 7 and int(register) < 16:
            input_file_write.write('pop ')
            register = str(int(register) & 7)
            input_file_write.write(register_with_speciel_register[register])

        elif all_the_byte == '226':
            input_file_write.write('loop ')
            print_Relative_Short_Displacement(input_file_write, input_file)

        input_file_write.write("\r\n")
        num_byte = 0

        byte = counter_and_one_byte(input_file)

        all_the_byte = str(ord(byte))
        order = str(ord(byte) & 240)
        register = str(ord(byte) & 15)
        byte = ord(byte)

    input_file_write.write('ret ')
    input_file_write.close



