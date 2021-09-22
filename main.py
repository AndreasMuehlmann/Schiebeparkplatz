import requests
from collections import deque
class Obstructing_car:
    
    def __init__(self, left, right):
        self.front = left
        self.back = right


def get_parkinglot_from_website(): #make more readable
    url = 'https://bwinf.de/fileadmin/user_upload/parkplatz0.txt'
    result = requests.get(url)
    doc = result.content.decode("utf-8").split()
    first_letter = doc[0]
    last_letter = doc[1]
    normally_parking_cars = []
    alphabet=[(chr(ord(first_letter)+i)) for i in range(26)]
    for letter in alphabet:
        normally_parking_cars.append(letter)
        if letter == last_letter:
            break
    count_obstructing_cars = int(doc[2])
    doc = doc[3:]
    obstructing_parkinglot = []
    for parkingspace in range(len(normally_parking_cars)):
        obstructing_parkinglot.append(0)
    for car in range(count_obstructing_cars):
        obstructing_parkinglot[int(doc[car * 2 + 1])], obstructing_parkinglot[int(doc[car * 2 + 1]) + 1] = doc[car * 2], doc[car * 2] # write the cars into the list not into a special list
        obstructing_cars = Obstructing_car(doc[car * 2], int(doc[car * 2 + 1]), int(doc[car * 2 + 1]) + 1)
    return normally_parking_cars, obstructing_parkinglot, obstructing_cars

def print_actions(parkingspace, actions):
    print(f'{parkingspace}: ', end = '')
    for count, action in enumerate(actions):
        if count != len(actions) - 1:
            print(action, end = ', ')
        else:
            print(action)

def give_car_and_side_obstructing(to_free_up):
    for car in obstructing_cars:
        if car.left == obstructing_parkinglot[to_free_up]:
            return car, 'left'
        elif car.right == obstructing_parkinglot[to_free_up]:
            return car, 'right'

def car_mover(to_free_up, direction, actions=deque([])): # doesnt make sense so far
    obstructing_car, side = give_car_and_side_obstructing(obstructing_parkinglot, obstructing_cars, to_free_up)
    if side != direction:
        amount = 1
    else:
        amount = 2
    if direction == 'left':
        amount *= -1    
    # if you hit the end of the parkinglot actions = False
    # action has to be declared
    action = '' # has to be removed after
    if obstructing_parkinglot[obstructing_car.left + amount]:
        actions = car_mover(obstructing_parkinglot, obstructing_cars, obstructing_car.left + amount, direction, actions=deque([]))
    if not actions == False:
        actions.append(action)
    return actions

def main():
    global obstructing_parkinglot
    global obstructing_cars # remove this as well after fixing get_parkinglot_from_website()
    normally_parking_cars, obstructing_parkinglot, obstructing_cars = get_parkinglot_from_website()
    for parkingspace in range(len(normally_parking_cars)):
        if not obstructing_parkinglot[parkingspace]:
            print(f'{normally_parking_cars[parkingspace]}:')
        else:
            actions_left, possible = car_mover(parkingspace, 'left')
            actions_right, possible = car_mover(parkingspace, 'right')
            if actions_left or actions_right:
                print(f'The car that blocks the parkingspace {parkingspace} can`t be moved out of the way.')
            if actions_left < actions_right:
                print_actions(normally_parking_cars[parkingspace], actions_left)
            else:
                print_actions(normally_parking_cars[parkingspace], actions_right)

if __name__ == '__main__':
    main()