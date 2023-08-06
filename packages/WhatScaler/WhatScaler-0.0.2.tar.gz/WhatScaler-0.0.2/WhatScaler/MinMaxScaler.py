class MinMaxScaler():
    '''Make an arr with large numbers easier to work with,\n
    by scaling down the numbers by the maximum value,\n
    by defualt the class will return all the outputs between 0-1\n
    it will keep the proportion between the numbers.\n
    -----------------------------------------------------
    Usage:\n
    This can be used in AI programs, or in anything else you find realted.\n
    HOW TO USE:\n
    arr = [1, 5, 2]\n
    arr = MinMaxScaler(arr).GetOutput()\n
    print(arr)\n
    results =>
    [0.2, 1, 0.4]'''
    def __init__(self, numbers:list, maxN=1) -> None:
        self.__arr = numbers
        self.__max = maxN
        self.__MakeOutput()
    
    def __MakeOutput(self):
        maxValue = max(self.__arr)
        p = self.__max / maxValue # proportion
        newList = []
        for n in self.__arr:
            newList.append(p * n)
        self.__arr = newList

    def GetOutput(self):
        return self.__arr
