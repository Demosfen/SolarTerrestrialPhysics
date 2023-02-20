"""

"""


# --- Read ASCII file ---
def io(path):
    """

    :rtype: Data rows in string format
    """
    file = open(path, 'r')
    data = file.readlines()  # vector of the data (line-by-line, string type)
    file.close()
    return data


def kp_classification(value):
    match value:
        case "3":
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
