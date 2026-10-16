from posicion import print_at


def marco(col1, fil1, col2, fil2):
    for fl in range(fil1, fil2+1):
        for cl in range(col1, col2+1):
            if (fl == fil1) or (fl == fil2):
                print_at(fl, cl, '═')
            elif ((cl == col1) or (cl == col2)) and ((fl > fil1) or (fl < fil2)):
                print_at(fl, cl, '║')

            if (fl == fil1) and (cl == col1):
                print_at(fl, cl, '╔')
            elif (fl == fil1) and (cl == col2):
                print_at(fl, cl, '╗')

            if (fl == fil2) and (cl == col1):
                print_at(fl, cl, '╚')
            elif (fl == fil2) and (cl == col2):
                print_at(fl, cl, '╝')
