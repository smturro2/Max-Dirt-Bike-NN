
while True:
    key_info = ""
    # Ad d input to image data
    # space,left,right,up,down
    if keyboard.is_pressed('space'):
        key_info +="1"
    else:
        key_info +="0"
    if keyboard.is_pressed('left'):
        key_info +="1"
    else:
        key_info +="0"
    if keyboard.is_pressed('right'):
         key_info +="1"
    else:
        key_info +="0"
    if keyboard.is_pressed('up'):
        key_info +="1"
    else:
        key_info +="0"
    if keyboard.is_pressed('down'):
        key_info +="1"
    else:
        key_info +="0"
    print(key_info)