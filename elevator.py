import time
from random import randint

MAX_FLOORS = 10
MAX_ELEVATOR_CAPACITY = 6
NOT_MOVING = None
MAX_PEOPLE = 5

floors = []
my_elevator = None
priority_queue = None


class Time:
    tick_count = 0

    def run(self):
        while True:
            self.tick_count += 1

            print(f"|| TICK {self.tick_count} ||")

            PersonCreator.create()
            print(*floors, sep="\n")

            priority_queue.check_queue()

            print(my_elevator)
            print(priority_queue)

            my_elevator.move()

            if my_elevator.has_call_on_current_floor() and my_elevator.has_capacity():
                my_elevator.load_in()

            if my_elevator.person_reached_destination():
                my_elevator.load_out()

            time.sleep(3)


class Priority:
    def __init__(self) -> None:
        self.queue_persons = []

    def add_to_queue(self, person) -> None:
        self.queue_persons.append(person)

    def check_queue(self):
        if self.queue_persons:
            if self.queue_persons[0] not in my_elevator.elevator_persons:
                my_elevator.move_to = self.queue_persons[0].origin_floor
            else:
                my_elevator.move_to = self.queue_persons[0].destination_floor

    def deque_person(self, person):
        self.queue_persons.remove(person)

    def __repr__(self) -> str:
        return f"priority = {self.queue_persons[0]}     queue = {self.queue_persons}\nx-------------------------------------------x\n"


class Person:
    def __init__(self, origin_floor, destination_floor) -> None:
        self.origin_floor = origin_floor
        self.destination_floor = destination_floor

    def check_elevator_route(self) -> bool:
        current_floor = floors[my_elevator.present_floor - 1].floor_no
        if (
            my_elevator.move_to >= self.destination_floor > current_floor
            or my_elevator.move_to <= self.destination_floor < current_floor
        ):
            return True
        return False

    def __repr__(self) -> str:
        return f"P({self.origin_floor}, {self.destination_floor})"


class PersonCreator:
    def create():
        while True:
            source_floor = randint(1, MAX_FLOORS)
            destination_floor = randint(1, MAX_FLOORS)

            if source_floor != destination_floor:
                break

        person = Person(source_floor, destination_floor)

        floors[source_floor - 1].floor_persons.append(person)

        priority_queue.add_to_queue(person)


class Floor:
    def __init__(self, floor_no) -> None:
        self.floor_no = floor_no
        self.floor_persons = []

    def __str__(self):
        floor_no = "{:>{}}".format(self.floor_no, len(str(MAX_FLOORS)))
        return f"Floor {floor_no}  -  [{self.floor_persons}]"


class Elevator:
    def __init__(self) -> None:
        self.present_floor: int = 1
        self.move_to = NOT_MOVING
        self.elevator_persons = []
        self.elevator_capacity = 0

    def move(self):
        if self.move_to != NOT_MOVING:
            if self.present_floor > self.move_to:
                self.present_floor -= 1
            elif self.present_floor < self.move_to:
                self.present_floor += 1

    def load_in(self):
        persons = floors[self.present_floor - 1].floor_persons
        i = 0
        while i < len(persons):
            if persons[i] == priority_queue.queue_persons[0]:
                self.elevator_persons.append(persons.pop(i))
                self.elevator_capacity += 1
                priority_queue.check_queue()
            elif persons[i].check_elevator_route():
                self.elevator_persons.append(persons.pop(i))
                self.elevator_capacity += 1
            else:
                i += 1

    def load_out(self):
        if self.move_to == self.present_floor:
            self.move_to = NOT_MOVING

        new_elevator_persons = []
        for person in self.elevator_persons:
            if person.destination_floor != self.present_floor:
                new_elevator_persons.append(person)
            else:
                priority_queue.deque_person(person)
                self.elevator_capacity -= 1

        self.elevator_persons = new_elevator_persons

        priority_queue.check_queue()

    def has_call_on_current_floor(self):
        if floors[my_elevator.present_floor - 1].floor_persons:
            return True
        return False

    def person_reached_destination(self) -> bool:
        for person in self.elevator_persons:
            if person.destination_floor == self.present_floor:
                return True
        return False

    def has_capacity(self):
        if self.elevator_capacity < MAX_ELEVATOR_CAPACITY:
            return True
        return False

    def __repr__(self):
        return f"\nElevator {self.present_floor} -> {self.move_to} \nElevator  -  {self.elevator_capacity}/{MAX_ELEVATOR_CAPACITY}  -  {self.elevator_persons}\n"


def main():
    global floors, my_elevator, priority_queue
    floors = [Floor(floorNo) for floorNo in range(1, MAX_FLOORS + 1)]

    my_elevator = Elevator()

    priority_queue = Priority()

    tick = Time()
    tick.run()


if __name__ == "__main__":
    main()
