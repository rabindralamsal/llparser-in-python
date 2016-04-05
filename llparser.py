print "Let the following grammer be the input for parser: "
print "E -> TA" 
print "A -> +TA|_"
print "T -> FB"
print "B -> *FB|_"
print "F -> (E)| c"
print "  "
print "epsila symbol is denoted by '_' sign and right hand marker at table is denoted by '$' sign respectively. "
print "  "

Grammer = {
	"E":  ["T A"], 
	"A":  ["+ T A", "_"],  
	"T":  ["F B"], 
	"B": ["* F B", "_"] , 
	"F":  ["( E )", "c"] 
}

#let us consider the production of epsila be denoted by "_"
epsila = '_'
TERMINAL_SYMBOLS = ['+', '*', '(', ')', 'c']
NON_TERMINAL_SYMBOLS = ["E", "A", "T", "B", "F"]
START_SYMBOL = 'E'
RIGHT_HAND_MARKER = '$'
INPUT_STRING = 'c*c+c'

def has_epsila_derivation(G, alpha):
	return epsila in Grammer.get(alpha, [])

def COMPUTATION_FIRST(G, alpha):
	''' alpha may be terminal or non-terminal '''
	if alpha in TERMINAL_SYMBOLS or alpha == epsila:
		return [alpha,]

	first_set = set()
	# In case of non-terminal, see productions to find first
	productions = Grammer[alpha]

	for production in productions:
		for alpha in production.split():
			first_value = alpha
			if first_value in TERMINAL_SYMBOLS:
				first_set.add(first_value)
				break
			elif first_value == epsila:
				first_set.add(epsila)
				break
			elif first_value in NON_TERMINAL_SYMBOLS:
				first_set.update(COMPUTATION_FIRST(Grammer, first_value))
				# But check whether it gives epsila derivation. In that case,
				# see the first of next literal.
				if not has_epsila_derivation(Grammer, first_value):
					break
				else:
					first_set.remove(epsila)
			else:
				raise ValueError('Invalid literal: no terminal or non-terminal or epsila')
	return list(first_set)


def COMPUTATION_FOLLOW(G, alpha, called_by=[]):
	''' alpha may be terminal or non-terminal '''


	follow_set = set()

	if alpha == START_SYMBOL:
		follow_set.add(RIGHT_HAND_MARKER)

	for A, productions in Grammer.iteritems():
		for production in productions:
			if alpha in production.split():
				#print productions
				#print "Using production ", production, "for alpha:", alpha
				#print follow_set
				alpha_index = production.index(alpha)
				next_index = alpha_index + 1

				while(True):
					#print "0"
					if next_index == len(production):
						#print "1"
						if not A in called_by and  A != alpha:
							#print "Follow"
							follow_set.update(COMPUTATION_FOLLOW(Grammer, A, called_by + [alpha,]))
						break

					elif production[next_index] in TERMINAL_SYMBOLS:
						#print "2"
						follow_set.add(production[next_index])
						break
					elif production[next_index] in NON_TERMINAL_SYMBOLS:
						#print "3"
						#print "First"
						follow_set.update(COMPUTATION_FIRST(Grammer, production[next_index]))
						if not has_epsila_derivation(Grammer, production[next_index]):
							break
						#print "Epsila derivation", next_index
					next_index = next_index + 1
	try:
		follow_set.remove(epsila)
	except KeyError:
		pass

	return list(follow_set)


def print_FIRST_FOLLOW(Grammer):
	print "%-30s %-30s %-30s" %('Production (A -> a)', 'First(a)', 'Follow(A)')
	for A, productions in Grammer.iteritems():
		for production in productions:
			prod_str = "%s -> %s" %(A, production)
			print "%-30s %-30s %-30s" %(prod_str, COMPUTATION_FIRST(Grammer, production[0]), COMPUTATION_FOLLOW(Grammer, A))

	# x = PrettyTable(['Production', 'First(alpha)', 'Follow(A)',])
	# for A, productions in Grammer.iteritems():
	# 	for production in productions:
	# 		prod_str = "%s -> %-3s" %(A, production)
	# 		x.add_row([prod_str, COMPUTATION_FIRST(Grammer, production[0]), COMPUTATION_FOLLOW(Grammer, A)])
	# print x.get_string(padding_width=5)
	
def generate_table(Grammer):
	M = {}
	for n in NON_TERMINAL_SYMBOLS:
		M[n] = {}
		for m in TERMINAL_SYMBOLS + ['$',]:
			M[n][m] = []
	for A, productions in Grammer.iteritems():
		for production in productions:
			first = COMPUTATION_FIRST(Grammer, production[0])
			follow = COMPUTATION_FOLLOW(Grammer, A)
			for f in first:
				if f != epsila:
					M[A][f].append(production)
				else:
					for h in follow:
						M[A][h].append(production)

	return M


def print_TABLE(Grammer):
	# M =  generate_table(Grammer)
	# print " ",
	# for i in NON_TERMINAL_SYMBOLS:
	# 	print "%10s" %i,
	# # x.add_column(' ', NON_TERMINAL_SYMBOLS)
	# for t in TERMINAL_SYMBOLS + ['$',]:
	# 	column = []
	# 	for n in NON_TERMINAL_SYMBOLS:
	# 		production = M[n][t]
	# 		if len(production) == 0:
	# 			production = "."
	# 		if len(production) == 1:
	# 			production = production[0]
	# # 		column.append(production)
	# # 	x.add_column(t, column)

	# print x.get_string(padding_width=1)

	M = generate_table(Grammer)

	# [["", "+", *, ( ) c $], [E, . . TA .]]
	table_list = []
	for j in range(len(NON_TERMINAL_SYMBOLS) + 1):
		row = []
		for i in range(len(TERMINAL_SYMBOLS) + 2):
			row.append("")
		table_list.append(row)


	# table_list = [["" for i in range(len(TERMINAL_SYMBOLS) + 2)] for j in range(len(NON_TERMINAL_SYMBOLS) + 1)]
	i = 0
	for t in TERMINAL_SYMBOLS + ['$']:
		column = []
		j = 0
		table_list[0][i+1] = t
		i += 1
		for n in NON_TERMINAL_SYMBOLS:
			table_list[j+1][0] = n
			j += 1
			production = M[n][t]
			if len(production) == 0:
				production = "."
			if len(production) == 1:
				production = production[0]
			table_list[j][i] = production
			# print i, j
	# 		column.append(production)
	# 	x.add_column(t, column)

	for row in table_list:
		for value in row:
			print "%10s" %value, 
		print ""




	# M =  generate_table(Grammer)
	# x = PrettyTable()
	# x.add_column(' ', NON_TERMINAL_SYMBOLS)
	# for t in TERMINAL_SYMBOLS + ['$',]:
	# 	column = []
	# 	for n in NON_TERMINAL_SYMBOLS:
	# 		production = M[n][t]
	# 		if len(production) == 0:
	# 			production = "."
	# 		if len(production) == 1:
	# 			production = production[0]
	# 		column.append(production)
	# 	x.add_column(t, column)

	# print x.get_string(padding_width=1)

print "The First and Follow set for the Given Grammer:"
print_FIRST_FOLLOW(Grammer)
print " "
print "The Parsing Table for given Grammer:"

print_TABLE(Grammer)
print " "
print "The Parsing Procedure for the given input string " + (INPUT_STRING)
def testing_parser(Grammer, inp):
	M = generate_table(Grammer)

	inp = list(inp + RIGHT_HAND_MARKER)
	
	stack = [RIGHT_HAND_MARKER, START_SYMBOL]
	action = '-'

	print "%-40s %-35s %-30s" %("Stack", "Input", "Action")
	while(True):
		print "%-30s %-40s %-30s" %(stack, inp, action)
		X = stack[-1]
		e = inp[0]
		if X in TERMINAL_SYMBOLS or X in '$':
			if X == e:
				stack.pop()
				inp.pop(0)
				action = "Terminal Match"
			else:
				print "Error due to terminal non matching"
				return
		else:
			if len(M[X][e]) != 0:
				production_to_append = list(M[X][e][0].split())
				production_to_append.reverse()
				stack.pop()
				stack.extend(list(production_to_append))
				action = "Replace with", M[X][e]
			else:
				print "Error"
				return
		# Remove epsila from stack
		try:
			stack.remove(epsila)
		except ValueError:
			pass

		if X == '$':
			print ' The given input string ' + (INPUT_STRING) + ' has scucessfully parsed'
			break
testing_parser(Grammer, INPUT_STRING)
	
