import ItemInformation

# Information about the Item
item1 = ItemInformation.Item(23456, "S", "Item A")
item2 = ItemInformation.Item(23457, "M", "Item B")
item3 = ItemInformation.Item(23458, "L", "Item C")
item4 = ItemInformation.Item(23459, "C", "Item D")

item_idList = [item1.id, item2.id, item3.id, item4.id]
item_lockerSize = [item1.ls, item2.ls, item3.ls, item4.ls]

# Information about the locker
# 0 is used to represent locker is empty
# 1 is used to represent locker is used
lockerS = 0
lockerM = 0
lockerL = 0
chute = 0

# Main Code
# Loop to check if ID exist
idnChecker = input("Please Enter the ID provided:- ")
if int(idnChecker) in item_idList:
    y = 1
    # y is used for me to check if ID exist
else:
    print("ID have error, please try again")
    idnChecker = input("Please Enter the ID provided:- ")

# This code is used to find where the ID is stored in the List
if int(y) == 1:
    itemFinder = item_idList.index(int(idnChecker))

# This code is used to find what Size it has been assigned
LsValueStore = item_lockerSize[itemFinder]

if LsValueStore == "S" and int(lockerS) == 0:
    lockerS = 1

elif LsValueStore == "M" or int(lockerS) == 1:
    lockerM = 1

elif LsValueStore == "L" or int(lockerS) == 1 or int(lockerM) == 1:
    lockerL = 1

else:
    chute = 1

# To be removed, for visual representation

print("These are the lockers used for now")
print(lockerS)
print(lockerM)
print(lockerL)
print(chute)
