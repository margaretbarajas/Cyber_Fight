import time 
import math 
import random


classTypes = ["Robot","Dinosaur","Mage","Dog"]
statNames = ["Attack","Speed","Defence","Power","Health"]
classStats = [[6,2,5,5,100],[7,3,4,5,100],[3,5,5,10,100],[4,6,2,6,100]]
PName = ""
pStats = [0,0,0,0,0]
statAdjustment = [0,0,0,0,0,]
pClass = -1
pMoney = 500
pstatus = "fine"
pLevel = 0 
pExp = 0
CurrentLocation = "Home"
placesToTravel = [["Cybertron","Earth","Chicago","Batcave"],[200,300,75,35]]
distanceToHome = 0 
activityMenu = ["View Stats","Travel","Shop","Inventory"]
itemsToBuy = [["potion","burnHeal","iceHeal","statBoost"],[100,50,50,200]]
itemsToFind = [["potion","burnHeal","iceHeal","statBoost","cheapVase","expensiveVase","garbage"],[100,50,50,200,25,300,0]]
monsterTypes = [["Magatron","Starscream","Cat","Weak Enemy","Witch"],[10,8,5,1,30],[8,5,7,3,11],[5,7,3,1,15],[10,10,5,2,15],[120,120,75,30,300]]
inventory = ["potion"]
escapeAttempt =[False,False]

def indexInList(item,myList):
    foundIndex = -1
    for i in range(len(myList)):
        if(item == myList[i]):
            foundIndex = i
            break
    return foundIndex
    
def listToText(myList):
    combinedText = "\n"
    for i in range(len(myList)):
        combinedText += str(i) + ") " + myList[i] + "\n"
    return combinedText + "\n"
    
            


def checkMenuRange(question,listName,isCanceable = False):
    index = int(input(question + listToText(listName)))
    while(True):
        if(isCanceable and index == -1):
            return index
        elif index < 0 or index > len(listName) -1:
            index = int(input("Invalid choice please try again\n"))
        else:
            return index
    


def starLine(numRows,numSleep):
    sLine = "*" * 10
    for i in range(numRows):
        print(sLine)
    time.sleep(numSleep)
    
def showInventory(inventoryList):
    if(len(inventoryList) < 1):
        print("Uh oh... It's Empty?!")
        return
    uniqInventoryList = list(set(inventoryList))
    for i in range(len(uniqInventoryList)):
        print(str(i)+") " + uniqInventoryList[i] + "("+str(inventoryList.count(uniqInventoryList[i]))+")")


def useItemMenu():
    global pStatus
    showInventory(inventory)
    uniqInventoryList = list(set(inventory))
    if(len(inventory) < 1):
        return
    chosenItem = checkMenuRange("pick your choice, quickly!",uniqInventoryList,True)
    if chosenItem == -1:
        return
    itemToUse = indexInList(uniqInventoryList[chosenItem],itemsToFind[0])
    if(itemToUse == 0):
        pStats[4] += 10
        print("You've been healed, don't make it a habit to come here..")
    elif(itemToUse == 1):
        if(pStatus == "Fine" or pStatus == "Ice"):
            print("Burn Heal had no effect")
        else:
            print(pName + " was Burn Healed!")
            pStatus = "Fine"
    elif(itemToUse == 2):
        if(pStatus == "Fine" or pStatus == "Burn"):
            print("Ice Heal had no effect")
        else:
            print(pName + " was Ice Healed!")
            pStatus = "Fine"
    elif(itemToUse == 3):
        checkStatBoost = checkMenuRange("What stat would you like to temporarily boost?",["Attack","Speed","Defence","SPower"])
        numBoost = math.ceil(pStats[checkStatBoost] * .1)
        pStats[checkStatBoost] += numBoost
        statAdjustment[checkStatBoost] += numBoost
        print("Stat Boosted!")
    else:
        print("")
        
    if(itemToUse > 3):
        print("Is this your choice? well ok... ")
        starLine(1,2)
    else:
        print("Current Stats")
        for i in range(len(statNames)):
            print(statNames[i],pStats[i])
        inventory.remove(itemsToFind[0][itemToUse])


def playerAttack():
    global pStatus
    runStat = random.randint(0,100)
    
    fightChoice = checkMenuRange("Make your choice, quickly!",["Fight","Item","Run"])
    
    if(fightChoice == 0):
        attackType = checkMenuRange("Choose an attack!",["FIST","Magic","Dodge"])
        monDefPercentage = 1-monsterStats[2]/12
        if(attackType == 0):
            print("BOINK BOINK BOINK BA")
            damage = pStats[0] * monDefPercentage
            print("Damage " + str(damage))
            monsterStats[4] -= damage
        elif(attackType == 1):
            print("Woosh WOOOOSHHhhhhh WOOOSH")
            critChance = random.randint(0,100)
            critBonus = 1
            if(critChance > 70):
                print("CRITICAL HIT!")
                critBonus = 1.4
            damage = (pStats[3] * monDefPercentage) * critBonus
            print("Damage "+ str(damage))
            monsterStats[4] -= damage
        else:
            #Attempt to dodge 
            escapeAttempt[0] = True
        print("Monster Health " + str(monsterStats[4]))
        starLine(1,2)
    elif(fightChoice == 1):
        useItemMenu()
    else:
        #Try to Run
        if(pStats[1]/20 * 100 <= runStat):
            print("It's a miracle i got away.")
            for i in range(len(statAdjustment)):
                pStats[i] -= statAdjustment[i]
                statAdjustment[i] = 0
            escapeAttempt[1] = True
            starLine(2,1)
        else:
            print("You fool! you can not escape!")
            
    return escapeAttempt
            
    
def monsterAttack():
    global pStatus
    if(pStatus != "Fine"):
        if(pStatus == "Burn"):
            pStats[4] -=5 
            print(pName + " was hurt by burn")
        else:
            pStats[4] -=3 
            print(pName + " was hurt by ice")
        
        print(pName + " health is now " + str(pStats[4]))
    print("Monster turn")
    starLine(1,1)
    attackOptionChance = random.randint(0,100)
    pDefPercentage = (1 - (pStats[2]/20))
    if(monsterChoice == 0):
        #megatron
        if(attackOptionChance < 45):
            print("FUSION CANNON!")
            pStats[4] -= monsterStats[3] * pDefPercentage
            burnChance = random.randint(0,100)
            if(burnChance < 30):
                print(pName + " was burned from attack!")
                pStatus = "Burn"
        elif(attackOptionChance < 90):
            print("HERE'S SOMETHING TO KEEP YOU WARM!")
            pStats[4] -= monsterStats[0] * pDefPercentage
        else:
            tauntChance = random.randint(0,100)
            if (tauntChance < 10):
                print("SELF HEAL!")
                monsterStats[4] *= 1.1
            else:
                print("IDIOT!")
    elif(monsterChoice == 1):
        #Dinosaur
        if(attackOptionChance < 45):
            print("ROARRRR!")
            pStats[4] -= monsterStats[3] * pDefPercentage
            burnChance = random.randint(0,100)
            if(burnChance < 30):
                print(pName + " recieved frost bite from attack!")
                pStatus = "Ice"
        elif(attackOptionChance < 90):
            print("GRRRR")
            pStats[4] -= monsterStats[0] * pDefPercentage
        else:
            tauntChance = random.randint(0,100)
            if (tauntChance < 10):
                print("SELF HEAL!")
                monsterStats[4] *= 1.1
            else:
                print("amazing,, YOU thought you could defeat ME?")
    elif(monsterChoice == 2):
        #Mage
        if(attackOptionChance < 50):
            #Taunt
            print("Hi I'm Spike :D")
        else:
            print("I might be small, but i am undefeated!")
            pStats[4] -= (monsterStats[0] * pDefPercentage)
    elif(monsterChoice == 3):
        #weak Enemy
        print("Oops, bumped into you")
        pStats[4] -= (monsterStats[0] * pDefPercentage)
    else:
        #Dog
        megaDemonYells = ["WELCOME TO THE HELL DIMENSION ","THE HEAT IS ETERNAL",]
        print(megaDemonYells[random.randint(0,len(megaDemonYells))])
        if(attackOptionChance < 45):
            print("HELL HOUND WAVE!")
            pStats[4] -= monsterStats[3] * pDefPercentage
        elif(attackOptionChance < 90):
            print("SLAP, CRACKLE, POP")
            pStats[4] -= monsterStats[0] * pDefPercentage
        else:
            tauntChance = random.randint(0,100)
            if(tauntChance < 10):
                print("DOUBLE SELF HEAL!!!!!")
                monsterStats[4] *= 1.2
            else:
                print("LISTEN TO YOUR MASTER!")
    print(pName+ "Health: " + str(pStats[4]))
        
    
   
pName = input("What is your name\n")
print("Welcome to the wonderful world of Cybertron " + pName + "!")
starLine(3,1)
for i in range(len(classTypes)):
    print(classTypes[i]+":")
    for j in range(len(classStats[i])):
        print(statNames[j],classStats[i][j])
    starLine(1,1.5)
pClass = checkMenuRange("Choose your Class: ",classTypes)
print("You have chosen " + classTypes[pClass]+"!")
pStats = classStats[pClass]
starLine(2,2)
print("From henceforth you shall be known as "+pName + " the " + classTypes[pClass])
starLine(1,3)
print("Long ago in a time when anything was possible there was a land called IACON\n that was ironically home to a great warrior\n but war broke out and it's up to optim....I mean "+pName + " to save the day!")
starLine(1,6)    




#Main Loop


inGameLoop = True
while(inGameLoop and pStats[4] > 0):
    #Stats,travel,shop,inventory
    actChoice = checkMenuRange(" what would you like to do, nobel hero? ",activityMenu)
    if(actChoice == 0):
        print("Your Stats: ")
        for i in range(len(statNames)):
            print(statNames[i],pStats[i])
    elif(actChoice == 1):
        print("Travel")
        travelChoice = checkMenuRange("Where would you like to travel to? ",placesToTravel[0],True)
        if travelChoice == -1:
            isTravel = False
        else:
            isTravel = True
            print("And so " +pName + " set off on their journey to "+placesToTravel[0][travelChoice])
            if(placesToTravel[1][travelChoice] == distanceFromHome):
                print("Woahh, even blurr can't travel this fast!")
                isTravel = False
        #Travel Loop
        distanceDivider = random.randint(3,6)
        distanceTraveled = math.ceil(placesToTravel[1][travelChoice]/distanceDivider)
        isTravelNeg = placesToTravel[1][travelChoice] < distanceFromHome
        while(isTravel and pStats[4] > 0):
            if(not isTravelNeg):
                distanceFromHome += distanceTraveled
                if(distanceFromHome >= placesToTravel[1][travelChoice]):
                    print("You have reached " + placesToTravel[0][travelChoice])
                    isTravel = False
            else:
                distanceFromHome -= distanceTraveled
                if(distanceFromHome <= placesToTravel[1][travelChoice]):
                    print("You have reached " + placesToTravel[0][travelChoice])
                    isTravel = False
            if( not isTravel):
                distanceFromHome = placesToTravel[0][travelChoice]
                break
            
            #Random pickup or battle
            if(random.randint(0,100) < 60):
                inFight = True
                monsterPercentage = random.randint(0,100)
                monsterChoice = -1
                # fire, ice, monkey, weak, mega boss demon dude guy Person
                if(monsterPercentage <= 25):
                    monsterChoice = 3
                elif(monsterPercentage <= 55):
                    monsterChoice = 0
                elif(monsterPercentage <= 85):
                    monsterChoice = 1
                elif(monsterPercentage < 99):
                    monsterChoice = 2
                else:
                    monsterChoice = 4
                
                starLine(1,2)
                print("You have been challenged to fight by "+ monsterTypes[0][monsterChoice])
                starLine(1,1)
                monsterStats = [monsterTypes[1][monsterChoice],monsterTypes[2][monsterChoice],monsterTypes[3][monsterChoice],monsterTypes[4][monsterChoice],monsterTypes[5][monsterChoice]]
                chanceAdditional = 0
                currentTurn = -1
                if(pStats[1] > monsterStats[1]):
                    chanceAdditional = random.randint(25,50)
                turnChance = 50 + chanceAdditional    
                
                if(random.randint(0,100) < turnChance):
                    currentTurn *= -1
                    
                while(inFight and pStats[4] > 0):
                    if(currentTurn == 1):
                        escapeAttempt = playerAttack()
                        if(escapeAttempt[1]):
                            escapeAttempt[1] = False
                            break
                    else:
                        incChance = 0
                        if(pStats[1] > monsterStats[1]):
                            incChance = random.randint(25,50)
                        dChance = 25 + incChance
                        failChance = random.randint(0,100)
                        if(escapeAttempt[0]):
                            if(failChance < dChance):
                                print(pName + " HAS NARROWLY AVOIDED ATTACK!")
                            else:
                                print("DODGE FAILED")
                                monsterAttack()
                            escapeAttempt[0] = False
                        else:
                            monsterAttack()
                    starLine(1,2)
                    
                    currentTurn *= -1
                    
                    if(pStats[4] <= 0):
                        print("The mighty "+pName+ " may he return to the allspark")
                        break
                    if(monsterStats[4] <= 0):
                        print(pName + " has defeated the monster!")
                        for i in range(len(statAdjustment)):
                            pStats[i] -= statAdjustment[i]
                            statAdjustment[i] = 0
                        pExp += 10
                        print(pName + " has gained 10 exp!")
                        starLine(1,1)
                        if(pExp % ((pLevel+1)*10) == 0):
                            pExp = 0 
                            if pLevel < 20:
                                pLevel += 1
                                print(pName + " is now level " + str(pLevel))
                                starLine(1,1)
                                print("you have one stat point to use what will it be? ")
                                print("Current Stats: ")
                                for i in range(len(statNames)):
                                    print(statNames[i],pStats[i])
                                statIncreaseChoice = checkMenuRange("", statNames)
                                pStats[statIncreaseChoice] += 1
                                print(statNames[statIncreaseChoice] + " is now " + str(pStats[statIncreaseChoice]) )
                                
                        break    
                    
                #print("In Fight")
            else:
                #Random PickUp 
                starLine(1,1)
                print("Traveling......")
                starLine(1,1)
                pickUpChance = random.randint(0,100)
                if(pickUpChance < 20):
                    itemFound = itemsToFind[0][0]
                elif(pickUpChance < 30):
                    itemFound = itemsToFind[0][1]
                elif(pickUpChance < 40):
                    itemFound = itemsToFind[0][2]
                elif(pickUpChance < 45):
                    itemFound = itemsToFind[0][3]
                elif(pickUpChance < 65):
                    itemFound = itemsToFind[0][4]
                elif(pickUpChance < 69):
                    itemFound = itemsToFind[0][5]
                else:
                    itemFound = itemsToFind[0][6]
                    
                print(pName + " has found " + itemFound)
                addItemCheck = checkMenuRange("Would you like to add this item to your inventory?",["Yes","No"])
                if(addItemCheck == 0):
                    print(itemFound + " was added to your inventory")
                    inventory.append(itemFound)
                else:
                    print(itemFound + " was discarded")
                
                starLine(1,1)
                print(pName + " continues journey!")
                starLine(1,2)
                
            
                    
    elif(actChoice == 2):
        while(True):
            print("Current balance is $" +str(pMoney))
            shopChoice = checkMenuRange("Welcome to my Shop! My Name is bumblebee, how may I help you? Would you like to Buy or Sell?",["Buy","Sell","Show Inventory"],True)
            if shopChoice == -1:
                break
            elif shopChoice == 0:
                #Buy
                buyChoice = checkMenuRange("What would you like to buy?",itemsToBuy[0])
                if(pMoney - itemsToBuy[1][buyChoice]  >= 0):
                    inventory.append(itemsToBuy[0][buyChoice])
                    pMoney -= itemsToBuy[1][buyChoice]
                else:
                    print("sorry, you're currently broke :c " + itemsToBuy[0][buyChoice])
            elif shopChoice == 1:
                if(len(inventory) > 0):
                    itemList = list(set(inventory))
                    showInventory(inventory)
                    sellChoice = checkMenuRange("What would you like to sell?",itemList)
                    if(sellChoice != -1):
                        itemIndex = indexInList(itemList[sellChoice],itemsToFind[0])
                        sellPrice = math.floor(itemsToFind[1][itemIndex] * .9)
                        confirmChoice = checkMenuRange("Are you sure you want to sell, our best price is "+ str(sellPrice),["Yes","No"])
                        if confirmChoice == 0:
                            pMoney += sellPrice
                            inventory.remove(itemsToFind[0][itemIndex])
                            print("Item Sold, current balance is $"+str(pMoney))
                        else:
                            print("one bots trash is anothers treausure!")
                else:
                    print("Are you trying to play at something? you have nothing to sell!")
            elif shopChoice == 2:
                showInventory(inventory)
                    
    elif(actChoice == 3):
        showInventory(inventory)
 