import sys
assignments = []
# Set to False to solve normal non-diagonal puzzles
diagonal = True


def cross(A, B):
    """Cross product of elements in A and B
    """
    return [a + b for a in A for b in B]


# Setup Sudoku grid structure
digits = '123456789'
rows = 'ABCDEFGHI'
boxes = cross(rows, digits)
cols = digits

# units are each 9 box section of the board within which the digits 1-9 must
# appear only once

# ex [A1,A2,A3...A9]
row_units = [cross(r, cols) for r in rows]

# ex [A1, B1, C1, I9]
col_units = [cross(rows, c) for c in cols]

# ex [A1,A2,A3,B1,B2,B3,C1,C2,C3]
sq_units = [cross(r_grp, c_grp) for r_grp in ('ABC', 'DEF', 'GHI')
            for c_grp in ('123', '456', '789')]

# Collect all possible units together
# list of lists of squares in each unit [[<squares unit>],[<squares unit>]]
unit_list = row_units + col_units + sq_units

# diagonal by default for Udacity grading - diagonal flag at top of file
if diagonal:
    # ex ['A1','B2','C3'...'I9']
    primary_diagonal = [r + c for r, c in zip(rows, cols)]
    # ex ['A9','B8','C7'...'I1']
    secondary_diagonal = [r + c for r, c in zip(rows, cols[::-1])]
    diag_units = [primary_diagonal, secondary_diagonal]
    unit_list += diag_units


# Mapping from each square (ex A1) to the units it belongs to
# {'A1': [[A1,A2,A3...A9],[A1, B1, C1, I9],[A1,A2,A3,B1,B2,B3,C1,C2,C3]]...}
units = {s: [unit for unit in unit_list if s in unit] for s in boxes}

peers = {s: set(sum(units[s], [])) - set([s]) for s in boxes}


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any
    # values
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
    two_possible = [b for b, v in values.items() if len(v) == 2]
    twins = [[b1, b2] for b1 in two_possible for b2 in peers[b1]
             if set(values[b1]) == set(values[b2])]
    for pair in twins:
        common_peers = set(peers[pair[0]]) & set(peers[pair[1]])
        for peer in common_peers:
            if len(values[peer]) >= 2:
                for v in values[pair[0]]:
                    assign_value(values, peer, values[peer].replace(v, ''))
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.

    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value,
                    then the value will be '123456789'.
    """
    return {s: v if v != '.' else digits for s, v in zip(boxes, grid)}


def display(values):
    """
    Display the values as a 2-D grid, separated into 3x3 sections

    Args:
        values(dict): The sudoku in dictionary form
    """
    max_box_width = max(len(values[b]) for b in boxes) + 1
    for i in range(len(row_units)):
        row = ''.join(values[b].center(max_box_width) for b in row_units[i])
        row = ' | '.join(row[i:i + max_box_width * 3]
                         for i in range(0, len(row), max_box_width * 3))
        if i > 0 and i % 3 == 0:
            print('-' * len(row))

        print(row)


def eliminate(values):
    """ Removes the value of each determined box from its peers.

    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        updated values dictionary
    """
    solved = [b for b in boxes if len(values[b]) == 1]
    for b in solved:
        for p in peers[b]:
            assign_value(values, p, values[p].replace(values[b], ''))
    return values


def only_choice(values):
    """ Finds boxes which have a unique possible value in a unit and assigns
    that value to the box.
    Applies the strategy 'If there is only one box in a unit which would
    allow a certain digit, then that box *must* be assigned that digit'

    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        updated values dictionary
    """
    for unit in unit_list:
        for d in '123456789':
            possible_boxes = [b for b in unit if d in values[b]]
            if len(possible_boxes) == 1:
                assign_value(values, possible_boxes[0], d)
    return values


def reduce_puzzle(values):
    """ Repeatedly applies eliminate, only_choice and naked_twins strategies
    on the Sudoku to reduce the problem space, until no more progress is made.

    Args:
        values(dict): The sudoku in dictionary form
    Returns:
        values dictionary reduced as much as possible
        False if a box has 0 possible values -> error in strategy or puzzle
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])

        # Apply constraint propagation strategies
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        # Check how many boxes have a determined value
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero poss values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """ Applies constraint propagation in a Depth First Search strategy. The
    board is reduced as far as possible, then the box with the mininum possible
    values is chosen and recursively attempt to solve the puzzle obtained
    by choosing each possible value.
    """
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
        assign_value(new_grid, s, value)
        result = search(new_grid)
        if result:  # returns False unless solved
            return result


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: ('2.............62....1....7...6..8...3...9...7...6..4...
                        4....8....52.............3')
    Returns:
        The dictionary representation of the final sudoku grid.
        False if no solution exists.
    """
    values = grid_values(grid)
    solution = search(values)
    if solution:
        return solution
    else:
        return False


if __name__ == '__main__':
    args = sys.argv[1:]
    puzzle = None
    visualize = True
    # pass in a string puzzle to solve after '-p' flag
    if '-p' in args:
        puzzle = args[args.index('-p') + 1]
    # diagonal by default for Udacity project grading
    else:
        puzzle = ('2.............62....1....7...6..8...3...9...7...6..' +
                  '4...4....8....52.............3')
    if '--novisual' in args:
        visualize = False

    display(solve(puzzle))

    if visualize:
        try:
            from visualize import visualize_assignments
            visualize_assignments(assignments)

        except SystemExit:
            pass
        except:
            print('We could not visualize your board due to a pygame issue.' +
                  'Not a problem! It is not a requirement.')
