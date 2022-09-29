# read textfile into string
with open("private_test/AGGW0002890/full_PAGG0037null_4_CLB_SBPS_2022_K2015_00113_20220916_1663305198402.jpg'.jpg", 'r') as txtfile:
    mytextstring = txtfile.read()

# change text into a binary array
binarray = ' '.join(format(ch, 'b') for ch in bytearray(mytextstring))

print(binarray)
