# get input string
input_string = input("Input the string to be hashed: ")
orig_bit_string = ''.join('0'+format(ord(char), 'b') for char in input_string)
# orig_bit_string="0101001011001100101111011000000010111001000110110100011101111000001100100100000100100101110111011100111101000010111101111110100111100101000100100011000010001101100111011010010100110101111001011011000111101000011101111001010001000010100011011111100110011110100011001000001000001001001111000110110001111100100100101111010111001100010010010000011010000001011110001111001011010101010000111011010101100010100011011111011100000000101001010110001000100100001101010001000101110001101110110100111110111100111001110000011111100111110000100100011010100111111000111111100011000001001001101010001101001000111010111101101001110110101001100101000000010100101010101010001111000000000101101110100000000010001000110110100000101111111000001110101110101101101101110110011100010001101100010010111011100010011000010111000011011001001110110101110111011111100110111001100100101011011001001010000000011001101100001110001111000100011101100010010100000100001100101101000001110111110011001110001111010110001110110100001011101111111000100010000001110001001010111010111111011111010011011100101110010010101111100101100101011000000010011011110011110010100000100101001111101101010000100100001101010011001000101000010001110101101111011111000110011011011010010001111000101100000100010010111010001100100011100111001000001011101100100100010111100101001101000011111111110010101001111110100010111000101111010110110111110011011101011111011101111010101100110000011001010111001001010101011100011100011001111101000011111101110101111010111011101111101011011101010101011111001000111100101010001001100000100101000000000011011011011111001101000000110000001101011011010100000011100100011001000010010111101101100101000110110110110000111000010001101000110110001010011010000100011100011111011010000110100101111100101010000101100100110111011001011111000101110010110111000101111111011011101010000101010011010001101001001010010010110110010000111101000101100010100001000111100100010110000100000011100010110101000111011010111100000001111000100001101010110101000110101010110000100101100111101010000111101001000100110100101000111010011001011101010010010000100001101000110010011111000000010010001111011101100101010110000011101100001100100110110001110111100011100111001001110110010010101100101101100100000000100101110000111001000000010010111000110111101100001010010001010000111100010110001011011110110011101111011011111101110110001111100111010110010010111001001011111101110000000010101000101011100011000111010011110001110010100100001111000010101011001011010110011000111101111001000000100001011010011011100110101011001010000011100100010000101011111110000011111111010101100011010101000011010001001010011000111001000011101100101100111100000101011101011101001001001011011110011000111100101000000110010010111010001010010000000111011110010010010011011101010110110011110100011101011111011100111001011000001000110010000100111010011100001100110100111010100111001010010100110101000001001101010110010111011110110111000100000111010111000100100101011001111000011110101100100100001001000110100010011001011111001001110110110111100001110011110000101011010111010010111000111111100001000100110110000011001100000001010010001000010110000101000100010010001110000011000000010110000010110110000001010000001101110101000100110010001100110001001110001101011110101001011010110100010100011110011111110100011011001101111001011010000000101000100110001111110111011000101010000001110010101010100001010110101111000111000011111111101010011000101111000010101111011100111000010110110100010110101000101111110110111000110100010101110111111111110110101111011100010011001010000101011111111001101111010111001110011100110001101000010100000100011011000010111000001110010001000011011101010110000111010011011101101101000101101111110001100000001010010111000011011100111011001101011111111011011000101010000100101101110111100011111011010101001101100111001100011001011100111101101110100110100001110110011111110110011111100110111010011000101000101011111001110011001111110000111011000110010101100101000100000001111001011101001000011011100000110111000111100000101011000110001011000110000110111000001111001001"
msg_len = len(orig_bit_string)

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

print("Final hash value: ", bit_hash_output)
print("Length: ", len(bit_hash_output))