from typing import Tuple


def get_input_data(file_path="input_code.txt"):
    input_list = []
    with open(file_path, "r") as file:
        for line in file:
            input_list.append(line.split("\n")[0])

    return input_list


def balance_out_pos(pos: int) -> int:
    return pos % 100


def balance_out_pos_and_get_quot(pos: int) -> Tuple[int, int]:
    return pos % 100, abs(pos // 100)


def part_1(input_data, current_pos):
    password_counter = 0
    for movement in input_data:
        if "R" in movement:
            pos = int(movement.split("R")[1])
            current_pos = balance_out_pos(current_pos + pos)
        if "L" in movement:
            pos = int(movement.split("L")[1])
            current_pos = balance_out_pos(current_pos - pos)

        print(f"Movement: {movement}, new position: {current_pos}")
        if current_pos == 0:
            password_counter += 1

    print("Password:", password_counter)


def part_2(input_data, current_pos):
    password_counter = 0
    for movement in input_data:
        print(f"New position: {current_pos}")
        print(f"Movement: {movement}")
        if "R" in movement:
            pos = int(movement.split("R")[1])
            # For cases when pos > 99
            if pos // 100 > 0:
                print(f"Increasing password by {(pos // 100)}")
                password_counter += pos // 100

            pos_balance = pos % 100
            print(f"Position balance: {pos_balance}")

            # Check if dial crosses 99 mark
            if current_pos + pos_balance > 100:
                password_counter += 1
                print(f"Increasing counter by 1 when sum is more than 100: {password_counter}")

            current_pos = (current_pos + pos_balance) % 100
        elif "L" in movement:
            pos = int(movement.split("L")[1])
            # For cases when pos > 99
            if pos // 100 > 0:
                print(f"Increasing password by {(pos // 100)}")
                password_counter += pos // 100

            pos_balance = pos % 100
            print(f"Position balance: {pos_balance}")

            # Check if dial crosses 99 mark
            if current_pos != 0 and current_pos - pos_balance < 0:
                password_counter += 1
                print(f"Increasing counter by 1 when sum is less than 0: {password_counter}")

            current_pos = (current_pos - pos_balance) % 100

        if current_pos % 100 == 0:
            password_counter += 1
            print(f"Increasing password by 1 to {password_counter} since current position is 0")

        print(f"New position: {current_pos}")

        print("-----------------------------------")
    print("Password:", password_counter)


input_data = get_input_data()

initial_dial = 50
current_pos = initial_dial
# part_1(input_data, current_pos)

current_pos = initial_dial
part_2(input_data, current_pos)
