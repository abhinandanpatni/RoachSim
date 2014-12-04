import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from random import randint
import time


roaches_accepted = 0
rogue_roaches_accepted = 0
roach_x = []
roach_y = []
shelter_x = []
shelter_y = []
shelter_capacity = []
shelter_occupied = []
shelter_darkness = []
decider_value = []
preference_list = []
roaches = 0
vision = 0
shelters = 0
preference_list_made = False
rogue_roaches = 0
rogue_x = []
rogue_y = []

def main():
    global roaches, vision, shelters, rogue_roaches
    roaches = input('Enter the number of cockroaches : ')
    roaches = int(roaches)
    
    rogue_roaches = input('Enter the number of rogue roaches : ')
    rogue_roaches = int(rogue_roaches)
    vision = roaches + rogue_roaches
    shelters = input('Enter the number of shelters:')
    shelters = int(shelters)

    #assigning random coordinates to cockroaches
    for i in range(0,roaches):
        roach_x.append(randint(0,roaches-1))
        roach_y.append(randint(0,roaches-1))

    for i in range(0,rogue_roaches):
        rogue_x.append(randint(0,roaches-1))
        rogue_y.append(randint(0,roaches-1))

    #print roach_x
    #print roach_y
    #print rogue_x
    #print rogue_y
    

    #assigning ranom coordinates to shelters
    for i in range(0,shelters):
        shelter_x.append(randint(0,roaches-1))
        shelter_y.append(randint(0,roaches-1))

    print shelter_x
    print shelter_y

    #assigning capacities, random darkness values and init of preference list
    for i in range(0,shelters):
        capacity = input('Enter the capacity of shelter ' + str(i+1) + ':')
        capacity = int(capacity)
        shelter_capacity.append(capacity)
        shelter_occupied.append(0)
        shelter_darkness.append(randint(0,10))
        decider_value.append(0)
        preference_list.append(i)

    print ('shelter capacities : ' + str(shelter_capacity))
    print ('shelter occupied : ' + str(shelter_occupied))
    print ('shelter darkness : ' + str(shelter_darkness))
    print ('decider values : ' + str(decider_value))
    print ('preference_list : ' + str(preference_list))

    #Actual plotting for the first time
    fig = plt.figure()
    scat = plt.scatter(roach_x, roach_y, c='green')
    scat = plt.scatter(rogue_x, rogue_y, c='yellow')
    scat = plt.scatter(shelter_x, shelter_y, c='red', marker=(4,0), s = 80)
    plt.xlim(-1, roaches+1)
    plt.ylim(-1, roaches+1)
    
    #Animation
    ani = animation.FuncAnimation(fig, update_plot, interval=500, 
        fargs=(scat, vision))
    
    plt.show()

#Function responsible for the whole thing
def update_plot(i, scat, vision):
    global roaches_accepted, roaches, shelters, rogue_roaches_accepted, rogue_roaches
    count_shelter_occupied = 0
    if(roaches_accepted + rogue_roaches_accepted < vision):
        plt.clf()
        #print ('Roaches done are ' + str(roaches_accepted))
        #Run till there is at least one cockroach in each shelter
        #if count_shelter_occupied < shelters:
        i = 0
        for i in range(0,shelters):
            if(shelter_occupied[i] > 0):
                count_shelter_occupied += 1
        #print('Number of shelters occupied are ' + str(count_shelter_occupied))
        temp_vision = vision / shelters
        #print('temp vision is : ' + str(temp_vision) + ' and shelters = ' + str(shelters))
        
        if(count_shelter_occupied < shelters):
            i = 0
            for i in range(0,shelters):
                j = 0
                while j < len(roach_x):
                    if (shelter_capacity[i] - shelter_occupied[i]) > 0 and abs(shelter_x[i] - roach_x[j]) < temp_vision  and abs(shelter_y[i] - roach_y[j]) < temp_vision:
                        #print('Doing movement for ' + str(i) + ' and ' + str(j))
                        rand_do_movement(i,j)
                        if(shelter_x[i] == roach_x[j] and shelter_y[i] == roach_y[j]):
                            shelter_occupied[i] += 1
                            roaches_accepted += 1
                            roaches = remove_roach(j)
                            print('roach removed :' + str(j))
                            print('roaches left : ' + str(roaches))
                        #print roach_x
                        #print roach_y
                        #print('\n')
                    
                    j += 1
                temp_vision += 1

        else:
            #print('Entering alternative flow for making preference lists')
            global preference_list_made
            #Runs for the remainder
            
            i = 0
            for i in range(0,shelters):
                #Make preference list
                decider_value[i] = shelter_darkness[i] * shelter_occupied[i]
            q = 0
            for q in range(0,shelters):
                for w in range(q+1,shelters):
                    if decider_value[q] < decider_value[w]:
                        temp = decider_value[q]
                        decider_value[q] = decider_value[w]
                        decider_value[w] = temp
                        temp2 = preference_list[q]
                        preference_list[q] = preference_list[w]
                        preference_list[w] = temp2
            print('Updating preference list : ' + str(preference_list))
                

            #i = 0
            decider = preference_list[0]
            #for i in preference_list:
            print ('checking capacity for shelter : ' + str(decider))
            if (shelter_occupied[decider] < shelter_capacity[decider]):
            #if (shelter_occupied[i] < shelter_capacity[i]):
                j = 0
                while j < len(roach_x):
                    if (shelter_capacity[decider] - shelter_occupied[decider]) > 0 and abs(shelter_x[decider] - roach_x[j]) < vision and abs(shelter_y[decider] - roach_y[j]) < vision:
                        #print('Doing movement for ' + str(decider) + ' and ' + str(j))
                        rand_do_movement(decider,j)
                        if(shelter_x[decider] == roach_x[j] and shelter_y[decider] == roach_y[j]):
                            shelter_occupied[decider] += 1
                            roaches_accepted += 1
                            roaches = remove_roach(j)
                            print('roach removed :' + str(j))
                            print('roaches left : ' + str(roaches))
                        #print roach_x
                        #print roach_y
                        #print('\n')
                    j += 1
            else:
                del preference_list[0]
                shelters -= 1

            rogue_decider = preference_list[-1]
            #for i in preference_list:
            print ('checking capacity for shelter : ' + str(rogue_decider))
            if (shelter_occupied[rogue_decider] < shelter_capacity[rogue_decider]):
            #if (shelter_occupied[i] < shelter_capacity[i]):
                j = 0
                while j < len(rogue_x):
                    if (shelter_capacity[rogue_decider] - shelter_occupied[rogue_decider]) > 0 and abs(shelter_x[rogue_decider] - rogue_x[j]) < vision and abs(shelter_y[rogue_decider] - rogue_y[j]) < vision:
                        #print('Doing rogue movement for ' + str(rogue_decider) + ' and ' + str(j))
                        do_rogue_movement(rogue_decider,j)
                        if(shelter_x[rogue_decider] == rogue_x[j] and shelter_y[rogue_decider] == rogue_y[j]):
                            shelter_occupied[rogue_decider] += 1
                            rogue_roaches_accepted += 1
                            roaches = remove_rogue(j)
                            print('rogue roach removed :' + str(j))
                            print('rogue roaches left : ' + str(rogue_roaches))
                        #print rogue_x
                        #print rogue_y
                        #print('\n')
                    j += 1
            else:
                del preference_list[-1]
                shelters -= 1

               # else:
                #    preference_decider += 1
                    
               # vision += 1
    

    scat = plt.scatter(roach_x, roach_y, c='green')
    scat = plt.scatter(rogue_x, rogue_y, c='yellow')
    scat = plt.scatter(shelter_x, shelter_y, c='red', marker=(4,0), s = 80)
    return scat,

#Function responsible for movement
def do_movement(j, k):
    #Checking for x coordinates
    if shelter_x[j] < roach_x[k]:
        roach_x[k] -= 1

    elif shelter_x[j] > roach_x[k]:
        roach_x[k] += 1

    else:
        pass

    #Checking for y coordinates
    if shelter_y[j] < roach_y[k]:
        roach_y[k] -= 1

    elif shelter_y[j] > roach_y[k]:
        roach_y[k] += 1

    else:
        pass

def do_rogue_movement(j, k):
    #Checking for x coordinates
    if shelter_x[j] < rogue_x[k]:
        rogue_x[k] -= randint(1,2)

    elif shelter_x[j] > rogue_x[k]:
        rogue_x[k] += randint(1,2)

    else:
        pass

    #Checking for y coordinates
    if shelter_y[j] < rogue_y[k]:
        rogue_y[k] -= randint(1,2)

    elif shelter_y[j] > rogue_y[k]:
        rogue_y[k] += randint(1,2)

    else:
        pass

def rand_do_movement(j, k):
    #Checking for x coordinates
    if shelter_x[j] < roach_x[k]:
        roach_x[k] -= randint(1,2)

    elif shelter_x[j] > roach_x[k]:
        roach_x[k] += randint(1,2)

    else:
        pass

    #Checking for y coordinates
    if shelter_y[j] < roach_y[k]:
        roach_y[k] -= randint(1,2)

    elif shelter_y[j] > roach_y[k]:
        roach_y[k] += randint(1,2)

    else:
        pass


def remove_roach(j):
    global roaches
   # print('roaches before removal : ' + str(roaches))
    '''for t in range(j,roaches-1):
        roach_x[t] = roach_x[t+1]
        roach_y[t] = roach_y[t+1] '''
    del roach_x[j]
    del roach_y[j]
    roaches -= 1
    #print('roaches after removal : ' + str(roaches))
    return roaches

def remove_rogue(j):
    global rogue_roaches
    #print('rogue roaches before removal : ' + str(rogue_roaches))
    '''for t in range(j,roaches-1):
        roach_x[t] = roach_x[t+1]
        roach_y[t] = roach_y[t+1] '''
    del rogue_x[j]
    del rogue_y[j]
    rogue_roaches -= 1
    #print('rogue roaches after removal : ' + str(rogue_roaches))
    return rogue_roaches
        

main()