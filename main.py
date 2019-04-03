ISA_FILE = "isa_data.txt"
PROGRAM_FILE = "test.zh"

register_names = {
	"ax" : 0,
	"al" : 1,
	"bx" : 2,
	"bl" : 3,
	"cx" : 4,
	"cl" : 5,
	"dx" : 6,
	"dl" : 7,
	"ex" : 8,
	"el" : 9,
	"fx" : 10,
	"fl" : 11
}

def to_dec(str_num):
	number = 0
	prefix = str_num[0:2]
	main_part = str_num[2:]

	if (prefix == "0x"):
		# Hexadecimal
		number = int(main_part, 16)
	elif (prefix == "0b"):
		# Binary
		number = int(main_part, 2)
	else:
		# Decimal
		number = int(str_num)

	return number

def div_instruction(line, num_op):
	result = []
	divided_instruction = line.split(" ")

	for i in range(num_op + 1):
		result.append(divided_instruction[i])

	return result

def read_isa():
	isa_dict = {}
	isa_data = open(ISA_FILE, "r")

	for line in isa_data.read().split("\n"):
		line_divided = line.split(" ")
		isa_dict[line_divided[1]] = int(line_divided[0])

	return isa_dict

def read_program():
	div_instruction_list = []
	program = open(PROGRAM_FILE, "r")
	instruction_list = program.read()

	for line in instruction_list.split("\n"):
		instruction = div_instruction(line, len(line.split(" ")) - 1)
		div_instruction_list.append(instruction)

	return div_instruction_list

def read_instructions(isa_dict, instructions):
	bin_instructions = []
	for ins in instructions:
		bin_code = isa_dict[ins[0]] << 12

		# One argument
		if (len(ins) - 1 == 1):
			bin_code += to_dec(ins[1])
		# Two arguments
		elif (len(ins) - 1 == 2):
			bin_code += int(register_names[ins[1]]) << 8
			bin_code += int(ins[2])

		bin_instructions.append(bin_code)
		print(format(bin_code, '#018b'))

def main():
	isa_dict = read_isa()
	instructions = read_program()
	bin_instructions = read_instructions(isa_dict, instructions)


if __name__ == "__main__":
	main()
