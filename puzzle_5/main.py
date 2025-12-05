def get_input_data(file_path="sample_input.txt"):
    fresh_items = []
    inventory_items = []
    list_type = "fresh"
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                list_type = "inventory"
                continue

            if list_type == "fresh":
                start, end = map(int, line.split("-"))
                fresh_items.append((start, end))
            else:
                inventory_items.append(int(line))

    return fresh_items, inventory_items


def merge_ranges(intervals):
    intervals.sort(key=lambda x: x[0])

    # Lets start merging now
    merged = []
    for start, end in intervals:
        # This means no merge required
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        # Merge by taking the maximum values of last appended interval and existing end
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged


def is_in_ranges(intervals, x):
    for start, end in intervals:
        if start <= x <= end:
            return True

    return False


def find_items_that_are_fresh(fresh_ranges, inventory_list):
    return sum(is_in_ranges(fresh_ranges, item) for item in inventory_list)


def count_items_in_interval(fresh_items_interval):
    total_count = 0
    for start, end in fresh_items_interval:
        total_count += end - start + 1

    return total_count


def main():
    fresh, inventory = get_input_data("input.txt")
    fresh_sorted = merge_ranges(fresh)

    # Part 1
    print(f"Total fresh items in inventory: {find_items_that_are_fresh(fresh_sorted, inventory)}")

    # Part 2
    print(f"Unique fresh items: {count_items_in_interval(fresh_sorted)}")


if __name__ == "__main__":
    main()
