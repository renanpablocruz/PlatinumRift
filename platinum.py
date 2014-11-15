import sys, math, operator

coef = dict(w_platinum = 2,
            w_mine = -1,
            w_not_mine = 1,
            w_num_enemies_on = -0.5,
            w_num_enemies_close = -1,
            w_num_my_pods = -2)

def evaluate(world_state, platinum_production, world_adj_list, my_id):
# Receive the world_state and return a evaluate for all zones

    evaluations = {}
    for zone_id, state in world_state.items():
        owner = state["owner"]
        pods = state["pods"]

        evaluation = 0.0

        # evaluate the platinum production
        evaluation += coef["w_platinum"]*platinum_production[zone_id]

        # evaluate if it's mine
        if owner == my_id:
            evaluation += coef["w_mine"]*platinum_production[zone_id]
        else: # neutral = enemy owner
            evaluation += coef["w_not_mine"]*platinum_production[zone_id]

        # evaluate the number of enemies at this zone
        for player_id in xrange(4):
            if player_id != my_id:
                evaluation += coef["w_num_enemies_on"]*pods[player_id]

        # evaluate the number of enemies close to this zone
        num_enemies_close = 0
        for close_zone in world_adj_list[zone_id]:
            for player_id in xrange(4):
                if player_id != my_id:
                    num_enemies_close += world_state[close_zone]["pods"][player_id]
        evaluation +=  coef["w_num_enemies_close"]*num_enemies_close

        # evaluate the number of my pods there
        evaluation += coef["w_num_my_pods"]*pods[my_id]

        # put on result dict
        evaluations[zone_id] = evaluation

    return evaluations



# To debug: print >> sys.stderr, "Debug messages..."

player_count, my_id, zone_count, link_count = [int(i) for i in raw_input().split()]

# reading platinum procution
platinum_production = {}
for i in xrange(zone_count):
    zone_id, platinum_source = [int(i) for i in raw_input().split()]
    platinum_production[zone_id] = platinum_source

# reading the map
world_adj_list = {}
for i in xrange(link_count):
    zone1, zone2 = [int(i) for i in raw_input().split()]
    if zone1 not in world_adj_list:
        world_adj_list[zone1] = [zone2]
    else:
        world_adj_list[zone1].append(zone2)
    if zone2 not in world_adj_list:
        world_adj_list[zone2] = [zone1]
    else:
        world_adj_list[zone2].append(zone1)

# game loop
while 1:
    platinum = int(raw_input()) # my available Platinum
    world_state = {}


    for i in xrange(zone_count):
        zone_id, owner_id, num_pods_P0, num_pods_P1, num_pods_P2, num_pods_P3 = [int(i) for i in raw_input().split()]
        world_state[zone_id] = dict(owner=owner_id, pods=[num_pods_P0, num_pods_P1, num_pods_P2, num_pods_P3])

    # call the other file
    evaluations = evaluate(world_state, platinum_production, world_adj_list, my_id)

    # moving phase
    my_zones = set(zone for zone in world_state if world_state[zone]["owner"] == my_id)
    moving = ""
    for zone in my_zones:
        next_zone = zone
        for neighboor in world_adj_list[zone]:
            if  evaluations[neighboor] > evaluations[next_zone]:
                next_zone = neighboor
        if next_zone != zone:
            num_pods = world_state[zone]["pods"][my_id]
            moving += str(num_pods/2)+" "+str(zone)+" "+str(next_zone)+" "
    if moving == "":
        print "WAIT"
    else:
        print moving

    # placing phase
    placing = ""
    sorted_eval = sorted(evaluations.items(), key=operator.itemgetter(1))
    print >> sys.stderr, sorted_eval
    while len(sorted_eval)>0 and platinum >= 20:
        placing_zone = sorted_eval.pop()[0]
        if world_state[placing_zone]["owner"] in (-1, my_id):
            platinum -= 20
            placing += "1 "+str(placing_zone)+" "
    if placing != "":
        print placing
    else:
        print "WAIT"
