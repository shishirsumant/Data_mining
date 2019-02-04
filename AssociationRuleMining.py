import csv

#function to parse the items in transaction files
def readTrans(fPath):
    transList = []
    with open(fPath)as transCsv:
        csvRead = csv.reader(transCsv)
        for trans in csvRead:
            eachTrans = trans[0].split(',')
            transList.append(eachTrans)
    print('Transactions in the set are',transList)
    return transList

#function to find the 1 itemset candidate list
def findCand1(allTrans):
    Candsize1 = []
    for eachTrans in allTrans:
        for item in eachTrans:
            if not [item] in Candsize1:
                Candsize1.append([item])
    Candsize1.sort()
    return list(map(frozenset,Candsize1))

#function to check whether itemset meets minimum support condition
def supportScan(alltrans,Candsetk,minsup,transcount):
    kItemset = {}
    for eachtrans in alltrans:
        for itemset in Candsetk:
            if itemset.issubset(eachtrans): #increment count if itemset is present
                if not itemset in kItemset:
                    kItemset[itemset] = 1
                else:
                    kItemset[itemset] += 1
    kfreq = []
    ksupport = {}
    for itemset in kItemset:
        support = kItemset[itemset]/transcount #calculate support
        if support >= minsup: kfreq.insert(0,itemset)
        ksupport[itemset] = support
    return kfreq,ksupport

#function to generate candidate itemsets iteratively with increasing size
def apriori(freqlistk, sizek):
    candListk = []
    kLen = len(freqlistk)
    for i in range(kLen):
        for j in range(i+1, kLen):
            list1 = list(freqlistk[i])[:sizek-2]
            list2 = list(freqlistk[j])[:sizek-2]
            list1.sort()
            list2.sort()
            if list1==list2:
                candListk.append(freqlistk[i] | freqlistk[j])
    return candListk

#calculates the support values and composes a final list of candidate itemsets
def itemSetk(dataSet, support,candList1,totTrans):
    dataSetList = list(map(set, dataSet))
    frequentList1, supDict = supportScan(dataSetList, candList1, support,totTrans)
    totList = [frequentList1]
    size = 2
    while (len(totList[size-2]) > 0):
        candlistk = apriori(totList[size-2], size)
        freqlistk, supportK = supportScan(dataSetList, candlistk, support,totTrans)
        supDict.update(supportK)
        print('\nCandidate Itemset of size ',size,' is',freqlistk)
        totList.append(freqlistk)
        size += 1
    return totList, supDict
#generates association rules with confidence greater than min confidence
def getMinConfSet(freqItemSet,current,SupInfo, rules, minconf):
    prunedCurrent = []
    for itemset2 in current:
        currentConf = SupInfo[freqItemSet]/SupInfo[freqItemSet-itemset2]
        if (currentConf >= minconf):
            print(freqItemSet-itemset2,' ==> ', itemset2,' has confidence ',currentConf)
            rules.append((freqItemSet-itemset2, itemset2,currentConf))
            prunedCurrent.append(itemset2)
    return prunedCurrent
#creates new association rules by merging new items to existing itemset
def generateNew(freqItemSet, current, supInfo, rules, minconf):
    currentSetLen = len(current[0])
    freqlen = len(freqItemSet)
    if(freqlen > (currentSetLen+1)):
        newCand = apriori(current,currentSetLen+1)
        newCand = getMinConfSet(freqItemSet,newCand,supInfo,rules,minconf)
        newLen = len(newCand)
        if(newLen>1):
            generateNew(freqItemSet,newCand,supInfo,rules,minconf)


def association(suplist,supdata,minconf):
    listFin = []
    for i in range(1,len(suplist)):
        for itemset1 in suplist[i]:
            tempcopy = [frozenset([item]) for item in itemset1]
            if (i > 1): generateNew(itemset1,tempcopy,supdata,listFin,minconf)
            else: getMinConfSet(itemset1,tempcopy,supdata,listFin,minconf)
    return listFin

if __name__=='__main__':
    minSupport = input('Enter the minimum support value in percentage')
    minSupport = float(minSupport)/100
    minConfidence = input('Enter the minimum confidence value in percentage')
    minConfidence = float(minConfidence)/100
    Transactions = readTrans('C:/Users/HP/Desktop/Transaction3.csv')
    totTrans = float(len(Transactions))
    candList1 = findCand1(Transactions) #find the candidate 1 itemset
    numItems=len(candList1)
    print('\nThe number of unique items in the dataset are: ',numItems)
    print('\nThe items are as follows: ',candList1)
    finList,supportInfo = itemSetk(Transactions,minSupport,candList1,totTrans) #iteratively find k- frequent itemsets
    print('\n Item sets and corresponding support values are:')
    print(supportInfo)
    print('\n The list of rules are : \n')
    finitems = association(finList,supportInfo,minConfidence)
