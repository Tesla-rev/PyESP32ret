import cantools
 
db = cantools.database.load_file('model3dbc/Model3CAN.dbc')
 
#print(db.decode_message("ID102VCLEFT_doorStatus", b'\\x01\\x45\\x23\\x00\\x11') )
 
#print(db.decode_message(0x102, b'\\x01\\x45\\x23\\x00\\x11') )

print(db.decode_message(int("102",16), b'\\x01\\x45\\x23\\x00\\x11') )


