"""
Simple data file reader.
"""


def io(path):
    """
    :rtype: Data rows in string format
    """
    file = open(path, 'r')
    data = file.readlines()  # vector of the data (line-by-line, string type)
    file.close()
    return data


"""
The standard Kp values look like 0, 0+, 1-, 1, 1+, 2-,
but are stored as Kp = 0, 3, 7, 10, 13, 17, ... in the OMNI data set.
OMNI have mapped 0+ to 3, 1- to 7, 1 to 10, 1+ to 13, 2- to 17, etc.
For example Kp = 7+ is coded as 73; Kp = 7- is coded as 77; Kp = 7 as 70
"""


def kp_classification(value):
    match value:
        case "0" | "3":
            return 0
        case "7" | "10" | "13":
            return 1
        case "17" | "20" | "23":
            return 2
        case "27" | "30" | "33":
            return 3
        case "37" | "40" | "43":
            return 4
        case "47" | "50" | "53":
            return 5
        case "57" | "60" | "63":
            return 6
        case "67" | "70" | "73":
            return 7
        case "77" | "80" | "83":
            return 8
        case "87" | "90" | "93":
            return 9


# --- Epoch and Substorm onset compare ---

def epoch_index(cycle, time):
    k = -1

    for i in range(len(cycle)):
        if int(time) in range(int(cycle[i][0]), int(cycle[i][1]), 50):
            k = i

    return k


# --- Season search ---

def season_index(month):
    if month in range(3, 6) or month in range(9, 12):
        return 2  # off-season
    elif month in range(6, 9):
        return 1  # Summer
    else:
        return 0  # Winter


# --- Print list ---

def print_list(path, name, outputHeader, toPrint):
    file = open(path + name + '.lst', 'w')
    file.write(outputHeader)
    file.write('\n')

    for line in toPrint:
        file.write(line)
        file.write('\n')
    file.close()
