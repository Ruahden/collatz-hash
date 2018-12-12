import random, string, math

def get_hash (orig_bit_string, msg_len):

    # fixed iv
    iv = "1101010000001000010101010001010101110101011011111000000100110110011010001011000100010101011000001101101100010011001001111010001001000010110110000110110011110001101011011011111001110101100001111110011001011001110010010001100010110010101011101011110111000111"
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
        
        block_index += 1

    if (padding_block == True):
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

    return bit_hash_output;

i = 1
hash_table = set()
num_of_iterations = 0
while(i <= 256):
    input_string = ''.join(random.choice(string.ascii_letters + string.digits) for a in range(i))
    orig_bit_string = ''.join('0'+format(ord(char), 'b') for char in input_string)
    msg_len = len(orig_bit_string)
    
    j = 0
    while(j < len(orig_bit_string)):
        print('(i,j): (',i,',',j,')')
        temp_list = list(orig_bit_string)
        if(orig_bit_string[j] == "0"):        
            temp_list[j] = "1"
        else:
            temp_list[j] = "0"
        orig_bit_string = ''.join(temp_list)
        bit_hash_output = get_hash(orig_bit_string, msg_len)
        if bit_hash_output not in hash_table:
            hash_table.add(bit_hash_output)
        else:
            print('Collision Found!')
            exit()
        j += 1
        num_of_iterations += 1
    
    i += 1

print('No Collisions Found!')
print('Iterations: ', num_of_iterations)

#64684