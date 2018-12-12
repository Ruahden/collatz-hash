import random, string, math

def get_hash (iv, orig_bit_string, msg_len):

    padding_block = False
    block_index = 0

    while(block_index*256 < msg_len):

        # check if last block
        next_block_index = (block_index+1)*256    
        if next_block_index >= msg_len: # this is the last block

            bit_string = orig_bit_string[block_index*256:msg_len]
            
            # check if there is space for 64 bits
            space_left = next_block_index - msg_len
            if space_left < 64:
                bit_string.zfill(256)
                msg_len_bit = ""
                padding_block = True       

            else: # last block can contain last 64   
                while(len(bit_string) + 64 < 256): # padding 0's to the last block
                    bit_string += "0"

                msg_len_bit = format(msg_len, 'b')
                msg_len_bit.zfill(64)

            if(block_index == 0): # first and last block
                hash_input = iv + bit_string + msg_len_bit
                xl = iv
            else: 
                print("entered else!")
                hash_input = bit_hash_output + bit_string + msg_len_bit
                xl = bit_hash_output
            xr = bit_string + msg_len_bit

        else: # not last block

            # bit_string Definition if not last block
            bit_string = orig_bit_string[block_index*256:block_index*256+256]

            if(block_index == 0): # first and last block
                hash_input = iv + bit_string
                xl = iv
            else: 
                hash_input = bit_hash_output + bit_string
                xl = bit_hash_output
            xr = bit_string
        
        s = ""
        i = 0
        int_hash = int(hash_input, 2)

        while (i < 256):
            if (int_hash % 2 == 0): # even
                temp = format(int_hash, 'b')
                temp = "0" + temp[0:len(temp)-1] # bitwise shift to the right or divide by two
                int_hash = int(temp, 2)
                s = "0" + s
            else: #odd
                int_hash = (3*int_hash) +1
                temp = format(int_hash, 'b')
                temp = "0" + temp[0:len(temp)-1] # bitwise shift to the right or divide by two
                int_hash = int(temp, 2)
                s = "1" + s
            i += 1
        
        hash_bit = format(int_hash, 'b')
        hash_bit = hash_bit.zfill(512)

        xpl = hash_bit[0:256]
        xpr = hash_bit[256:512]

        # xors
        hash_output = int(xl, 2) ^ int(xr, 2)
        hash_output = hash_output ^ int(xpl, 2)
        hash_output = hash_output ^ int(xpr, 2)
        hash_output = hash_output ^ int(s, 2)
        bit_hash_output = format(hash_output, 'b')
        bit_hash_output = bit_hash_output.zfill(256)
        print("hash_input: ", hash_input)
        print("bit_hash_output: ", bit_hash_output)
        
        block_index += 1

    if (padding_block == True):
        print('entered padding block!')
        pb_content = "0"

        while(len(pb_content) + 64 < 256): # padding 0's to the last block
            pb_content += "0"

        msg_len_bit = format(msg_len, 'b')
        msg_len_bit.zfill(64)
        hash_input = bit_hash_output + bit_string + msg_len_bit

        xl = bit_hash_output
        xr = bit_string + msg_len_bit
        s = ""
        i = 0
        int_hash = int(hash_input, 2)

        while (i < 256):
            if (int_hash % 2 == 0): # even
                temp = format(int_hash, 'b')
                temp = "0" + temp[0:len(temp)-1] #bitwise shift to the right or divide by two
                int_hash = int(temp, 2)
                s = "0" + s
            else: #odd
                int_hash = (3*int_hash) +1
                temp = format(int_hash, 'b')
                temp = "0" + temp[0:len(temp)-1] #bitwise shift to the right or divide by two
                int_hash = int(temp, 2)
                s = "1" + s
            i += 1
        
        hash_bit = format(int_hash, 'b')
        hash_bit = hash_bit.zfill(512)

        xpl = hash_bit[0:256]
        xpr = hash_bit[256:512]

        # xors
        hash_output = int(xl, 2) ^ int(xr, 2)
        hash_output = hash_output ^ int(xpl, 2)
        hash_output = hash_output ^ int(xpr, 2)
        hash_output = hash_output ^ int(s, 2)
        bit_hash_output = format(hash_output, 'b')
        bit_hash_output = bit_hash_output.zfill(256)

    print("hash_input: ", hash_input)
    print("bit_hash_output: ", bit_hash_output)
    # print("Length: ", len(bit_hash_output))

    return bit_hash_output;

def get_hash_blocks (iv, orig_bit_string, msg_len):

    # fixed iv
    padding_block = False
    block_index = 0
    prev_hash = iv

    iv_array = [None] * 3
    bit_string = [None] * 3

    i=0
    iv_array[0] = iv

    while(block_index*256 < msg_len):

        # check if last block
        next_block_index = (block_index+1)*256    
        if next_block_index >= msg_len: # this is the last block
            bit_string = orig_bit_string[block_index*256:msg_len]
        else:
            bit_string[i] = orig_bit_string[block_index*256:block_index*256+256]
        
        

        block_index += 1

    bit_hash_output = get_hash(prev_hash, bit_string, len(bit_string))
    print("hash_input: ", prev_hash + bit_string)
    print("bit_hash_output: ", bit_hash_output)
    prev_hash = bit_hash_output

    return bit_hash_output;

iv = "1101010000001000010101010001010101110101011011111000000100110110011010001011000100010101011000001101101100010011001001111010001001000010110110000110110011110001101011011011111001110101100001111110011001011001110010010001100010110010101011101011110111000111"

input_string = ''.join(random.choice(string.ascii_letters + string.digits) for a in range(60))
orig_bit_string = ''.join('0'+format(ord(char), 'b') for char in input_string)
msg_len = len(orig_bit_string)
bit_hash_output = get_hash(iv, orig_bit_string, msg_len)
print("-----------------First output: ", bit_hash_output)

orig_bit_string = ''.join('0'+format(ord(char), 'b') for char in input_string)
bit_hash_output = get_hash_blocks(iv, orig_bit_string, msg_len)
print("-----------------Second output: ", bit_hash_output)

