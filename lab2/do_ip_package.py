def adr_to_byte(adr: str):
    src = adr.split('.')
    src_byte = int(src[0]).to_bytes(8, 'big')

    for num in range(1, 4):
        src_byte += int(num).to_bytes(8, 'big')
    return src_byte


def do_ip_package(file_name: str, ADR_SRC: str, ADR_DEST: str):
    """ Функция формирующая пакет IP """
    try:
        f = open(file_name, 'wb')
        f.write((0).to_bytes(4, 'big'))  # Version
        f.write((0).to_bytes(4, 'big'))  # IHL
        f.write((0).to_bytes(6, 'big'))  # DSCP
        f.write((0).to_bytes(2, 'big'))  # ECN
        f.write((0).to_bytes(16, 'big'))  # Total Length
        f.write((0).to_bytes(16, 'big'))  # Identification
        f.write((0).to_bytes(3, 'big'))  # Flags
        f.write((0).to_bytes(13, 'big'))  # Fragment Offset
        f.write((0).to_bytes(8, 'big'))  # Time to live
        f.write((0).to_bytes(8, 'big'))  # Protocol
        f.write((0).to_bytes(16, 'big'))  # HeaderCheckSum

        src = adr_to_byte(ADR_SRC)
        dest = adr_to_byte(ADR_DEST)
        f.write(src)  # Source Address
        f.write(dest)  # Destination Address

        f.close()
    except Exception as e:
        print(e)
