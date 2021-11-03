import requests
from collections import deque

def get_parkinglot_from_website(url):
    result = requests.get(url)
    doc = result.content.decode("utf-8").split()
    normal_parkinglot = give_normal_parkinglot(doc)
    obstructing_parkinglot = give_obstructing_parkinglot(doc, normal_parkinglot)
    return normal_parkinglot, obstructing_parkinglot

def give_normal_parkinglot(doc):
    first_letter = doc[0]
    last_letter = doc[1]
    normal_parkinglot = []
    alphabet=[(chr(ord(first_letter)+i)) for i in range(26)]
    for letter in alphabet:
        normal_parkinglot.append(letter)
        if letter == last_letter:
            break
    return normal_parkinglot

def give_obstructing_parkinglot(doc, normally_parking_cars):
    count_obstructing_cars = int(doc[2])
    doc = doc[3:]
    obstructing_parkinglot = []
    for parkingspace in range(len(normally_parking_cars)):
        obstructing_parkinglot.append(0)
    for car in range(count_obstructing_cars):
        obstructing_parkinglot[int(doc[car * 2 + 1])], obstructing_parkinglot[int(doc[car * 2 + 1]) + 1] = doc[car * 2], doc[car * 2]
    return obstructing_parkinglot

def give_side_obstructing(to_free_up):
    if 0 <= to_free_up - 1 and obstructing_parkinglot[to_free_up] == obstructing_parkinglot[to_free_up - 1]:
        return 'right'
    elif to_free_up + 1 < len(obstructing_parkinglot) and obstructing_parkinglot[to_free_up] == obstructing_parkinglot[to_free_up + 1]:
        return 'left'

def give_amount(direction, side):
    if side != direction:
        return 1
    else:
        return 2

def give_spot_to_check(to_free_up, amount, side, direction):
    if direction == 'left':
        if side != direction:
            front = to_free_up - 1  
        else:
            front = to_free_up
        return front - amount
    else:
        if side != direction:
            front = to_free_up + 1  
        else:
            front = to_free_up
        return front + amount

def car_mover(to_free_up, direction):
    actions = deque([])
    obstructing_car = obstructing_parkinglot[to_free_up]
    side = give_side_obstructing(to_free_up)
    amount = give_amount(direction, side)
    spot_to_check = give_spot_to_check(to_free_up, amount, side, direction)
    if not 0 <= spot_to_check < len(obstructing_parkinglot):
        return False
    action = [obstructing_car, direction, amount]
    if obstructing_parkinglot[spot_to_check] != obstructing_car and obstructing_parkinglot[spot_to_check]:
        actions = car_mover(spot_to_check, direction)
    if not actions == False:
        actions.append(action)
    return actions

def count_amount(actions):
    total_amount = 0
    for action in actions:
        total_amount += action[2]
    return total_amount

def write_acitons_to_file(parkingspace, actions, file):
    file.write(f'{parkingspace}: ')
    for count, action in enumerate(actions):
        if count != len(actions) - 1:
            file.write(f'{action[0]} {action[1]} {action[2]},  ')
        else:
            file.write(f'{action[0]} {action[1]} {action[2]}\n')
    return

def write_shortest_method_to_file(blocked_car, actions_left, actions_right, file):
    if actions_left:
        if actions_right:
            if len(actions_left) == len(actions_right):
                if count_amount(actions_left) < count_amount(actions_right):
                    write_acitons_to_file(blocked_car, actions_left, file)
                else:
                    write_acitons_to_file(blocked_car, actions_right, file)
            elif len(actions_left) < len(actions_right):
                write_acitons_to_file(blocked_car, actions_left, file)
            else:
                write_acitons_to_file(blocked_car, actions_right, file)
        else:
            write_acitons_to_file(blocked_car, actions_left, file)   
    elif actions_right:
        write_acitons_to_file(blocked_car, actions_right, file)
    else:
        file.write(f'{blocked_car}: not possible to free up.')

def main():
    global obstructing_parkinglot
    with open('schiebeparkplatz_results.txt', 'w') as file: 
        file.write('Schiebeparkplatz\n\n')
        for task in range(6):
            file.write(f'Test {task}\n\n')
            normal_parkinglot, obstructing_parkinglot = get_parkinglot_from_website(f'https://bwinf.de/fileadmin/user_upload/parkplatz{task}.txt')
            for parkingspace in range(len(normal_parkinglot)):
                if not obstructing_parkinglot[parkingspace]:
                    file.write(f'{normal_parkinglot[parkingspace]}: \n')
                else:
                    actions_left = car_mover(parkingspace, 'left')
                    actions_right = car_mover(parkingspace, 'right')
                    write_shortest_method_to_file(normal_parkinglot[parkingspace], actions_left, actions_right, file)
            file.write('\n\n')
    return

if __name__ == '__main__':
    main()