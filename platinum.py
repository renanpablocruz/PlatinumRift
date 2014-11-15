import sys, math, operator

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# playerCount: the amount of players (2 to 4)
# myId: my player ID (0, 1, 2 or 3)
# zoneCount: the amount of zones on the map
# linkCount: the amount of links between all zones

playerCount, myId, zoneCount, linkCount = [int(i) for i in raw_input().split()]

prod = {}
for i in xrange(zoneCount):
    # zoneId: this zone's ID (between 0 and zoneCount-1)
    # platinumSource: the amount of Platinum this zone can provide per game turn
    zoneId, platinumSource = [int(i) for i in raw_input().split()]
    prod[zoneId] = platinumSource

graph = {}
for i in xrange(linkCount):
    zone1, zone2 = [int(i) for i in raw_input().split()]
    if zone1 not in graph:
        graph[zone1] = [zone2]
    else:
        graph[zone1].append(zone2)
    if zone2 not in graph:
        graph[zone2] = [zone1]
    else:
        graph[zone2].append(zone1)

# game loop
while 1:
    platinum = int(raw_input()) # my available Platinum
    world_state = {}
    my_zones = set()
    for i in xrange(zoneCount):
        # zId: this zone's ID
        # ownerId: the player who owns this zone (-1 otherwise)
        # podsP0: player 0's PODs on this zone
        # podsP1: player 1's PODs on this zone
        # podsP2: player 2's PODs on this zone (always 0 for a two player game)
        # podsP3: player 3's PODs on this zone (always 0 for a two or three player game)
        zId, ownerId, podsP0, podsP1, podsP2, podsP3 = [int(i) for i in raw_input().split()]
        world_state[zId] = [ownerId, podsP0, podsP1, podsP2, podsP3]
        if ownerId == myId:
            my_zones.add(zId)

    evaluations = {}
    for zId in world_state:
        ownerId, podsP0, podsP1, podsP2, podsP3 = world_state[zId]
        # evaluation
        evaluation = 2*prod[zId]
        evaluation += prod[zId] if ownerId != myId else -prod[zId] # neutral = enemy owner
        for j in xrange(playerCount):
            if j != myId:
                evaluation += - world_state[zId][j+1]/2.0
        num_enemies_close = 0
        for neighboor in graph[zId]:
            for j in xrange(playerCount):
                if j != myId:
                    num_enemies_close += world_state[neighboor][j+1]

        evaluation +=  -1*num_enemies_close
        evaluation += -2*world_state[zId][myId+1]

        evaluations[zId] = evaluation

    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    # moving phase
    moving = ""
    for zone in my_zones:
        next_zone = zone
        for neighboor in graph[zone]:
            if  evaluations[neighboor] > evaluations[next_zone]:
                next_zone = neighboor
        if next_zone != zone:
            num_pods = world_state[zone][myId+1]
            moving += str((1+num_pods)/2)+" "+str(zone)+" "+str(next_zone)+" "
    if moving == "":
        print "WAIT"
    else:
        print moving

    placing = ""
    sorted_eval = sorted(evaluations.items(), key=operator.itemgetter(1))
    while len(sorted_eval)>0 and platinum >= 20:
        placing_zone = sorted_eval.pop()[0]
        if world_state[placing_zone][0] in (-1, myId):
            platinum -= 20
            placing += "1 "+str(placing_zone)+" "
    if placing != "":
        print placing
    else:
        print "WAIT"
