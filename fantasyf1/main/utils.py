import requests
import json
from fantasyf1 import cache


@cache.cached(timeout=180, key_prefix='driver_standings')
def get_driver_standings():
    headers = {"Content-Type": "application/json"}
    request = requests.post('https://safe-bayou-28242.herokuapp.com/graphql/', json={'query': '{driverstandings {driverId {forename surname} position points }}'}, headers=headers)
    if request.status_code == 200:
        data = request.json()
        driver_list = [[" ".join([driver['driverId']['forename'],driver['driverId']['surname']]), driver['position'], driver['points']] for driver in data['data']['driverstandings']]
        return sorted(driver_list, key= lambda x: x[1])
    else:
        raise Exception("Query failed to run by returning code of {}".format(request.status_code))

@cache.cached(timeout=180, key_prefix='last_race_results')
def get_last_race_results():
    headers = {"Content-Type": "application/json"}
    request = requests.post('https://safe-bayou-28242.herokuapp.com/graphql/', json={'query': '{results(year: 2019, round: "last") {driverId {forename surname} position points statusId {status}}}'}, headers=headers)
    if request.status_code == 200:
        data = request.json()
        driver_list = [[" ".join([driver['driverId']['forename'],driver['driverId']['surname']]), driver['position'], driver['points'], driver['statusId']['status']] for driver in data['data']['results']]
        for driver in driver_list:
            if driver[1] == '\\N' or driver[3] != 'Finished' and driver[3] != '+1 Lap' and driver[3] != '+2 Laps' and driver[3] != '+3 Laps':
                driver[1] = driver[3]
        return sorted(driver_list, key= lambda x: x[2], reverse=True)
    else:
        raise Exception("Query failed to run by returning code of {}".format(request.status_code))

@cache.cached(timeout=180, key_prefix='constructor_standings')
def get_constructor_standings():
    headers = {"Content-Type": "application/json"}
    request = requests.post('https://safe-bayou-28242.herokuapp.com/graphql/', json={'query': '{constructorstandings {constructorId {name} position points}}'}, headers=headers)
    if request.status_code == 200:
        data = request.json()
        constructor_list = [[constructor['constructorId']['name'], constructor['position'], constructor['points']] for constructor in data['data']['constructorstandings']]
        return sorted(constructor_list, key=lambda x: x[1])
    else:
        raise Exception("Query failed to run by returning code of {}".format(request.status_code))