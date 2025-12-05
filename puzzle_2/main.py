def get_input_data(file_path="input_ids.txt"):
    input_list = []
    with open(file_path, "r") as file:
        for line in file:
            return line.split("\n")[0].split(",")

    return input_list


def split_into_chunks(s, n):
    return [int(s[i:i + n]) for i in range(0, len(s), n)]


def check_repeat_pattern_generic(number, repeat_strategy=None):
    """
    In this logic we start by assuming every number is repeated once.
    If we observe that repeat once doesn't work then we switch strategy to first two
    numbers repeated and so on until we reach end of the number
    :param number: Input number
    :param repeat_strategy: Strategy to use for splitting
    :return: If repeats any pattern
    """
    num_length = len(number)
    if repeat_strategy is None:
        repeat_strategy = range(1, num_length)

    for strategy in repeat_strategy:
        if num_length % strategy == 0:
            chunks = split_into_chunks(number, strategy)
            # Ideally every number in chunk should be same
            if len(set(chunks)) == 1:
                return True
        else:
            continue

    return False


def main(solving_for=None):
    input_ids = get_input_data()

    sum_invalid_ids = 0
    for id_range in input_ids:
        start, stop = id_range.split("-")[0], id_range.split("-")[1]
        print(start, stop)
        for number in range(int(start), int(stop) + 1):
            # print("Checking", number)
            match = False
            if solving_for == "part1":
                strategy = [int(len(str(number)) / 2)]
                if strategy[0] > 0 and len(str(number)) % 2 == 0:
                    match = check_repeat_pattern_generic(str(number), repeat_strategy=strategy)
            elif solving_for == "part2":
                match = check_repeat_pattern_generic(str(number))

            if match:
                print("Id found:", number)
                sum_invalid_ids += number
            else:
                print("Rejecting: ", number)
        print("Sum: ", sum_invalid_ids)
    print("Grand Sum: ", sum_invalid_ids)


if __name__ == '__main__':
    part = "part2"
    main(solving_for=part)
