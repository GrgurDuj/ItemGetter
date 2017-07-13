i = 1
listfor1 = []
listfor2 = []
listfor3 = []

for i in range(1,201,3):
    listfor1.append(i)
for i in range(2,201,3):
    listfor2.append(i)
for i in range(3,201,3):
    listfor3.append(i)

while len(unpulled_summoners) > 0:
    if i in listfor1:
        set_up('KR')
    elif i in listfor2:
        set_up2('KR')
    elif i in listfor3:
        set_up3('KR')
    summoner = unpulled_summoners.popleft()
    summMatchList = summoner.match_list(begin_time=gather_start)
    print('summMatchList' , len(summMatchList))
    for match_reference in summMatchList:
        # If you are connected to a database, the match will automatically be stored in it.
        # Simply pull the match, and it's in your database for whenever you need it again!
        # If you pull a match twice, the second time it will be loaded from the database rather than pulled from Riot
        # and therefore will not count against your rate limit. This is true of all datatypes, include Summoner.
        match = riotapi.get_match(match_reference)
        if match is None:  # If the match still fails to load, continue on to the next one
                continue
        elif str(match) in match_set:
            print('Found duplicate' + match)
            continue
        else:
            match_set.add(match)
            print("Stored {0} in my database".format(match))
        pulled_summoners.append(summoner)
        i+=1
    print(len(pulled_summoners))


