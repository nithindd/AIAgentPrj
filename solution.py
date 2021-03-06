assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

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
	possible_twins = []
	for box in values.keys():
		if len(values[box])==2:
			possible_twins.append(box)
	
	naked_twins = [[box, twinbox] for box in possible_twins for twinbox in peers[box] if values[box]==values[twinbox]]
	for twin1, twin2 in naked_twins:
		intersected_elements = peers(twin1) & peers(twin2)
		for int_individual_val in intersected_elements:
			if len(values[int_individual_val]) > 2:
				for value in values[twin1]:
					values = assign_value(values, int_individual_val, values[int_individual_val].replace(value,''))
	return values

def cross(A, B):
   return [s+t for s in A for t in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
units_list = row_units + column_units + square_units
units = dict((s, [u for u in units_list if s in u ]) for s in boxes)
peers = dict((s, set(sum(units[s],[])) - set([s])) for s in boxes)
    
def grid_values(grid):
	chars=[]
	digits = "123456789"
	for value in grid:
		if value in digits:
			chars.append(value)
		if value == ".":
			chars.append(digits)
	assert len(chars)==81
	return dict(zip(boxes, chars))

def display(values):
    width = 1+max(len(values[s]) for s in boxes)
	line = "+".join(['-'*(width*3)]*3)
	for r in rows:
		print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
		if r in 'CF' : print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys if len(values[box])==1]
	
	for value_key in solved_values:
		digit = values[value_key]
		for peer in peers[value_key]:
			if digit in peer:
				values[peer] = values[peer].replace(digit, '')
				
	return values

def only_choice(values):
    for unit in units_list:
		for digit in '123456789':
			dplaces = [box for box in unit if digit in values[box]]
			if len(dplaces) == 1:
				values[dplaces[0]] = digit
	return values
	
def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
	stalled = False
	
	while not stalled:
		solved_values_before = [box for box in values.keys() if len(values[box]) ==1]
		values = eliminate(values)
		values = only_choice(values)
		values = naked_twins(values)
		solved_values_after = [box for box in values.keys() if len(values[box])==1]
		stalled = solved_values_after == solved_values_before
		if len([box for box in values.keys() if len(values[box]) == 0]):
			return False
	
	return values

def search(values):
    values = reduce_puzzle(values)
	
	if values is False:
		return False
	if all(len(values[s]) == 1 for s in boxes):
		return values
		
		n,s = min((len(values[s]),s) for s in boxes if len(values[s]) > 1)
		
		for value in values[s]:
			new_sudoku = values.copy()
			new_sudoku[s] = value
			attempt = search(new_sudoku)
			if attempt:
				return attempt
	
def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
	values = search(grid_values(grid))
	
	return values

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
