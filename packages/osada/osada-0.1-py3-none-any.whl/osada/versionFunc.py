versions = {
    "0.0": "12/30/2021",
    "0.0.1": "1/3/2022",
    "0.1" : "1/5/2022"
    }


version = list(versions.keys())[len(versions)-1]
version_info = f"{version} ({versions[version]})"


def getVersion():
    lst = list(map(int, version.split(".")))
    return len(lst), lst


def versionMatch(target):
    length, lst = getVersion()
    target_lst = list(map(int, target.split(".")))
    version_length = max(length, len(target_lst))
    coef = [10**(version_length-i) for i in range(version_length)]
    
    tmp = 0
    for i, ver in enumerate(lst):
        tmp += coef[i]*ver
    for i, tar in enumerate(target_lst):
        tmp -= coef[i]*tar
    return tmp >= 0
    