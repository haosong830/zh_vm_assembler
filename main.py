from array import *

ISA_FILE = "isa_data.txt"
PROGRAM_FILE = "test.zh"
PAGE_SIZE = 16

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
	counter = 0 # change to more pythonic shit
	isa_dict = {} # To assign names to info
	isa_info = [] # To save info about the instruction

	isa_data = open(ISA_FILE, "r")

	for line in isa_data.read().split("\n"):
		line_divided = line.split(" ")

		ins_id = int(line_divided[1])
		ins_ri = int(line_divided[0], 2)
		ins_page = int(counter / PAGE_SIZE)
		ins_name = line_divided[2]

		isa_info.append(ins_id);
		isa_info.append(ins_ri);
		isa_info.append(ins_page);

		isa_dict[ins_name] = isa_info # save the info with the name

		isa_info = [] # clean the info list

		counter += 1

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
	current_page = 0 # default page at start
	for ins in instructions:
		ins_info = isa_dict[ins[0]] # get instruction info

		# Check if we have to change page
		if (ins_info[2] != current_page):
			ins_info_isac = isa_dict["isa"]

			bin_code_isac = ins_info_isac[0] << 12 # add the isa ins id
			bin_code_isac += ins_info[2] # add the isa page id

			bin_instructions.append(bin_code_isac) # write the isa change instruction
			print(format(bin_code_isac, '#018b')) # print it

			current_page = ins_info[2]

		# Start with the actual instruction
		bin_code = ins_info[0] << 12
		ins_ri = ins_info[1]

		# One argument
		if (len(ins) - 1 == 1):
			if (ins_ri == 2):
				bin_code += to_dec(ins[1])
			elif (ins_ri == 0):
				bin_code += int(register_names[ins[1]])
			else:
				print("Instruction has invalid ri")

		# Two arguments
		elif (len(ins) - 1 == 2):
			if (ins_ri == 2):
				print("Instruction has invalid ri")
			elif (ins_ri == 1):
				bin_code += int(register_names[ins[1]]) << 8
				bin_code += to_dec(ins[2])
			elif (ins_ri == 0):
				bin_code += int(register_names[ins[1]]) << 8
				bin_code += int(register_names[ins[2]])
			else:
				print("Instruction has invalid ri")

		bin_instructions.append(bin_code)
		print(format(bin_code, '#018b'))
	return bin_instructions

def main():
	isa_dict = read_isa()
	instructions = read_program()
	bin_instructions = read_instructions(isa_dict, instructions)
	output = open("bin_out.zhb", "wb")

	for ins in bin_instructions:
		high = (ins & 0b1111111100000000) >> 8
		low = (ins & 0b0000000011111111)

		output.write(high.to_bytes(1, byteorder='big'))
		output.write(low.to_bytes(1, byteorder='big'))

if __name__ == "__main__":
	main()
