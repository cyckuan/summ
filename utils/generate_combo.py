#! /usr/bin/env python

def generate_combo(input_list,range_from,range_to):
	""" generates all possible combinations of elements in the input_list of size range_from to range_to
	"""

	import collections, itertools
	results = collections.defaultdict(list)
	for n in range(range_from, range_to + 1):
		combo_n = list(itertools.combinations(input_list, n))
		results[n] = results[n] + list(list(e) for e in combo_n)
		
	return results
	

if __name__ == '__main__':
	print(generate_combo(['a','b','c'],2,3))