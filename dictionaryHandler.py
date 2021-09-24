class DictionaryHandler():
    def __init__(self):
        print("created")

    def dictToLower(dic, keyName):
        response = {}
        for k in dic.keys():
            if str(keyName).lower() in k.lower():
                response[k] = str(dic[k]).lower()
        return response

    
    def dictToUpper():
        pass

    def findInDict():
        pass