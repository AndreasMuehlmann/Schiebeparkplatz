#
import requests
from collections import deque
class Obstructing_car:
    
    def __init__(self, left, right):
        self.front = left
        self.back = right


def get_parkinglot_from_website():
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
        obstructing_parkinglot[int(doc[car * 2 + 1])], obstructing_parkinglot[int(doc[car * 2 + 1]) + 1] = doc[car * 2], doc[car * 2]
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

def car_mover(to_free_up, direction, actions=deque([])): 
    obstructing_car, side = give_car_and_side_obstructing(obstructing_parkinglot, obstructing_cars, to_free_up)
    if direction == 'left':
        if side != direction:
            if obstructing_parkinglot[obstructing_car.left - 1]:
                to_free_up = obstructing_car.left - 1
        else:
            if obstructing_parkinglot[obstructing_car.left - 2]:
                to_free_up = obstructing_car.left - 2
    elif direction == 'right':
        if side != direction:
            if obstructing_parkinglot[obstructing_car.left + 1]:
                to_free_up = obstructing_car.left + 1
        else:
            if obstructing_parkinglot[obstructing_car.left + 2]:
                to_free_up = obstructing_car.left + 2
    action, possible = car_mover(obstructing_parkinglot, obstructing_cars, to_free_up, direction, actions=deque([]))
    actions.append(action)
    if possible:
        move(obstructing_parkinglot, obstructing_car, direction, 2)
    return

def move(car, direction, amount):
    obstructing_parkinglot[car.right] = 0
    obstructing_parkinglot[car.right] = 0
    if direction == 'left':
        car.right -= amount
        car.left -= amount
    else:
        car.right += amount
        car.left += amount
    obstructing_parkinglot[car.right] = 1
    obstructing_parkinglot[car.right] = 1

def main():
    global obstructing_parkinglot
    global obstructing_cars
    normally_parking_cars, obstructing_parkinglot, obstructing_cars = get_parkinglot_from_website()
    for carspace in range(len(normally_parking_cars)):
        if not obstructing_parkinglot[carspace]:
            print(f'{normally_parking_cars[carspace]}:')
        else:
            actions = car_mover(obstructing_parkinglot, carspace)
            print_actions(normally_parking_cars[carspace], actions)

if __name__ == '__main__':
    main()