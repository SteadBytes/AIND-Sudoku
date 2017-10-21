assignments = []


def cross(A, B):
    """Cross product of elements in A and B
    """
    return [a + b for a in A for b in B]


digits = '123456789'
rows = 'ABCDEFGHI'
boxes = cross(rows, digits)
cols = digits


row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
sq_unit = [cross(r_grp, c_grp) for r_grp in ('ABC', 'DEF', 'GHI')
           for c_grp in ('123', '456', '789')]
primary_diagonal = [r + d for r, d in zip(rows, digits)]
secondary_diagonal = [r + d for r, d in zip(rows, digits[::-1])]
diag_units = [primary_diagonal, secondary_diagonal]
unit_list = (row_units + col_units + sq_unit +
             diag_units)

units = {s: [unit for unit in unit_list if s in unit] for s in boxes}

peers = {s: set(sum(units[s], [])) - set([s]) for s in boxes}


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    return {s: v if v != '.' else digits for s, v in zip(boxes, grid)}


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    count = 0
    for row in row_units:
        if count % 3 == 0 and count != 0:
            print('-' * 24)
        row_vals = ' '.join([values[x] for x in row])
        output_str = ' | '.join(row_vals[i:i + 6]
                                for i in range(0, len(row_vals), 6))
        print(output_str)
        count += 1


def eliminate(values):
    solved = [b for b in boxes if len(values[b]) == 1]
    for b in solved:
        for p in peers[b]:
            values[p] = values[p].replace(values[b], '')
    return values


def only_choice(values):
    for unit in unit_list:
        for d in '123456789':
            possible_boxes = [b for b in unit if d in values[b]]
            if len(possible_boxes) == 1:
                values[possible_boxes[0]] = d
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        values = only_choice(values)
        # Check how many boxes have a determined value
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False  # Failed in reduce_puzzle
    if all(len(values[s]) == 1 for s in boxes):
        return values  # Solved
    # Square (not already determined) with fewest possibilities
    s = None
    for b in boxes:
        length = len(values[b])
        if length > 1:
            if s is None or length < len(values[s]):
                s = b

    for value in values[s]:
        new_grid = values.copy()
        new_grid[s] = value
        result = search(new_grid)
        if result:  # returns False unless solved
            return result


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    solution = search(values)
    if solution:
        return solution
    else:
        return False


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
