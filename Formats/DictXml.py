def dict_to_xml(data, count=0):
    if count == 0:
        tabs = ""
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    else:
        tabs = '    ' * count
        xml = ''

    for key, value in data.items():
        xml += tabs + f"<{key}>\n"
        key = key.split(" ")[0]

        if type(value) is dict:
            xml += dict_to_xml(value, count + 1)
            xml += tabs + f"</{key}>\n"
        elif type(value) is list:
            xml += "".join([tabs + f"    <{x} />\n" for x in value])
            xml += tabs + f"</{key}>\n"
        else:
            if value:
                xml += tabs + f"    {value}\n"
            xml += tabs + f"</{key}>\n"

    return xml
