# Diagonal Sudoku Solver
![Part of the Udacity Artificial Intelligence Nanodegree](https://img.shields.io/badge/Udacity-Artificial--Inteligence%20Nanodegree-02b3e4.svg)

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Naked Twins uses disjoint subsets to reduce the problem space in Sudoku. The rule states:
* If any two boxes belonging to a unit have only two possible values and these values are the same, then these values can only be in these boxes and can be **removed** from the possibilities for all other boxes in the unit.
* The pair of twins form a **disjoint subset** of the row, meaning that there is no elements in common (intersection = &empty;) between the twins and the other sets in the row.

For example, given the row:
```
row = [{1,3,6,9}, {1,5}, {4}, {3,6,9}, {8}, {7}, {1,5}, {1,6}, {2}]
```
The possible values `{1,5}` are present in **two** different boxes, forming a **disjoint subset** of the row. Therefore, the values `{1,5}` can be eliminated from all other undetermined boxes in the row:
```
row = [{3,6,9}, {1,5}, {4}, {3,6,9}, {8}, {7}, {1,5}, {6}, {2}]
# in this case, only the '1' was present as a possibility in other boxes
```
All possible twins need to be found in a given grid. Then, for each pair any undetermined boxes in the same unit as the twins can have the values of the twins eliminated.

Note: `values` is a dictionary representing the Sudoku grid. It contains the **possible** values for each box in the grid. Given a grid with rows `[A...I]` and columns `[1...9]`
```
values = {'A1':1, 'A2':'12345', 'A3':123456789...}
```

Find a subset of boxes in the grid which have **only two** possible values:
```python
two_possible = [b for b, v in values.items() if len(v) == 2]
```
Use `two_possible` to find naked twins by finding boxes whose two values are the same as one of those in its peers. This means they are in a unit together and thus create a naked pair:
```python
twins = [[b1, b2] for b1 in two_possible for b2 in peers[b1]
            if set(values[b1]) == set(values[b2])]
# sets are used as values could be in either order -> '12' and '21' should match
```
Then, for each pair of boxes in `twins` find the peers which they have in common (are in the same unit) and then eliminate the values of the pairs from their possible values - provided the peer hasn't already been determined:
```python
for pair in twins:
    common_peers = set(peers[pair[0]]) & set(peers[pair[1]])
    for peer in common_peers:
        if len(values[peer]) > 2:
            for v in values[pair[0]]:
                values[peer] = values[peer].replace(v, '')
```

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The two diagonals are another set of units. The same strategies (eliminate,
only choice and search) can be applied as long as the diagonal units are
included along with the row, column and 3x3 square units.

Diagonal units can be produced as follows:
```python
cols = '123456789'
rows = 'ABCDEFGHI'
primary_diagonal = [r + c for r, c in zip(rows, cols)]
secondary_diagonal = [r + c for r, c in zip(rows, cols[::-1])]
diag_units = [primary_diagonal, secondary_diagonal]
```
`diag_units` can then be included along with other unit types in any constraint propagation techniques used.
### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Usage
The solver runs on **diagonal puzzles**. 
* To change this, set the `diagonal = True` flag
at the top of [`solution.py`](solution.py) to `diagonal = False`.

Run the solver with a default diagonal Sudoku:
* `$ python solution.py` 

Use the `-p` flag to pass in a string representation of a puzzle:
* `$ python solution.py -p 2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3`

Use the `--novisual` flag to turn off pygame visualization and see results only
in terminal:
* * `$ python solution.py --novisual` 



### Code

* `solution.py` - Fill in the required functions in this file to complete the project.
* `test_solution.py` - You can test your solution by running `python -m unittest`.
* `PySudoku.py` - This is code for visualizing your solution.
* `visualize.py` - This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

