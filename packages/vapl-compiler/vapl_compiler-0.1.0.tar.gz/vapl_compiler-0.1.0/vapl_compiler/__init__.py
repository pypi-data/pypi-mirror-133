class COMPILER():
	def __init__(self,code):
		self.code = code
		self.memory = {}
		self.functionmemory = {}
		self.mailbox = ""
		self.compilecode(self.code)

	def compilecode(self,src:str, note=""):
		src = src.splitlines()
		for _ in src:
			self.compileline(_)

	def compileline(self,line):
		if line.startswith("!!"): #comment
			print("",end="")
		if line == "%":
			self.mailbox = "break"
		if line == "&":
			self.mailbox = "continue"
		if self.mailbox != "":
			return


		if line.startswith("!P "): #print
			if line[3:].startswith("(") and line[3:].endswith(")"):
				print(line[4:-1],end="")
			elif line[3:] == "@N":
				print()
			else:
				if type(self.memory[line[3:]]) is list:
					print("["+", ".join(self.memory[line[3:]])+"]",end="")
				else:
					print(self.memory[line[3:]],end="")
		if line.startswith("!I"): #input
			if line[3:].startswith("(") and line[3:].endswith(")"):
				tmp = input(line[4:-1])
				return tmp
			else:
				tmp = input(self.compileline(line[3:]))
				return tmp
		if line.startswith("!DV"): #define variable
			name = line[4:].split(":",1)[0]
			var = self.compileline(line[4:].split(":",1)[1])
			self.memory[name] = var
		if line.startswith("!F"): #function
			name = line[4:].split("}",1)[0]
			function = line[4:].split("} ",1)[1]
			self.functionmemory[name] = function
		if line.startswith("!E"): #execute function
			name = line[3:]
			function = self.functionmemory[name]
			self.compilecode("\n".join(function.split(";")))
		if line.startswith("!DC"): #do calculation
			templine = line[4:]
			if templine.startswith("$V"): #variables only
				listints = self.splitchars(["+","-","*","/"],templine[3:])
				listops = self.findchars(["+","-","*","/"],templine[3:])
				if len(listints) != len(listops)+1:
					#throw error
					print("",end="")
				curans = 0
				curans += int(self.memory[listints[0]])
				for i in range(0,len(listops)):
					if listops[i] == "+":
						curans += int(self.memory[listints[i+1]])
					if listops[i] == "-":
						curans -= int(self.memory[listints[i+1]])
					if listops[i] == "*":
						curans *= int(self.memory[listints[i+1]])
					if listops[i] == "/":
						curans /= int(self.memory[listints[i+1]])
				return curans
			if templine.startswith("$N"): #numbers only
				listints = self.splitchars(["+","-","*","/"],templine[3:])
				listops = self.findchars(["+","-","*","/"],templine[3:])
				if len(listints) != len(listops)+1:
					#throw error
					print("",end="")
				curans = 0
				curans += int(listints[0])
				for i in range(0,len(listops)):
					if listops[i] == "+":
						curans += int(listints[i+1])
					if listops[i] == "-":
						curans -= int(listints[i+1])
					if listops[i] == "*":
						curans *= int(listints[i+1])
					if listops[i] == "/":
						curans /= int(listints[i+1])
				return curans
		if line.startswith("!R"): #repeat (for loop)
			templine = line[3:]
			if templine.startswith("$N"): #number (repeating factor is a number)
				templine = templine[4:]
				num = int(templine.split("}",1)[0])
			if templine.startswith("$V"): #variable
				templine = templine[4:]
				num = int(self.memory[templine.split("}",1)[0]])
			todo = templine.split("} ",1)[1]
			for i in range(num):
				self.compilecode("\n".join(todo.split(";")))
				if self.mailbox != "":
					if self.mailbox == "break":
						self.mailbox = ""
						break
					self.mailbox = ""
					
		if line.startswith("?IF"): #if
			templine = line[4:]
			if templine.startswith("$E"): #equal
				templine = templine[4:]
				statement = templine.split("} ")[0]
				code = templine.split("} ")[1]
				arg1 = statement.split("=",1)[0]
				arg2 = statement.split("=",1)[1]
				if int(self.memory[arg1]) == int(self.memory[arg2]):
					self.compilecode("\n".join(code.split(";")))
			if templine.startswith("$N"): #not equal
				templine = templine[4:]
				statement = templine.split("} ")[0]
				code = templine.split("} ")[1]
				arg1 = statement.split("=",1)[0]
				arg2 = statement.split("=",1)[1]
				if int(self.memory[arg1]) != int(self.memory[arg2]):
					self.compilecode("\n".join(code.split(";")))
			if templine.startswith("$GT"): #greater than
				templine = templine[5:]
				statement = templine.split("} ")[0]
				code = templine.split("} ")[1]
				arg1 = statement.split("=",1)[0]
				arg2 = statement.split("=",1)[1]
				if int(self.memory[arg1]) > int(self.memory[arg2]):
					self.compilecode("\n".join(code.split(";")))
			if templine.startswith("$LT"): #less than
				templine = templine[5:]
				statement = templine.split("} ")[0]
				code = templine.split("} ")[1]
				arg1 = statement.split("=",1)[0]
				arg2 = statement.split("=",1)[1]
				if int(self.memory[arg1]) < int(self.memory[arg2]):
					self.compilecode("\n".join(code.split(";")))
			if templine.startswith("$GE"): #greater than or equal to
				templine = templine[5:]
				statement = templine.split("} ")[0]
				code = templine.split("} ")[1]
				arg1 = statement.split("=",1)[0]
				arg2 = statement.split("=",1)[1]
				if int(self.memory[arg1]) >= int(self.memory[arg2]):
					self.compilecode("\n".join(code.split(";")))
			if templine.startswith("$LE"): #less than or equal to
				templine = templine[5:]
				statement = templine.split("} ")[0]
				code = templine.split("} ")[1]
				arg1 = statement.split("=",1)[0]
				arg2 = statement.split("=",1)[1]
				if int(self.memory[arg1]) <= int(self.memory[arg2]):
					self.compilecode("\n".join(code.split(";")))
		if line.startswith("!DL"): #define list
			lst = []
			for i in line[4:].split(":")[1].split(","):
				lst.append(i)
			self.memory[line[4:].split(":")[0]] = lst
		if line.startswith("!LO"): #list operation
			templine = line[4:]
			varname = templine[1:].split("} ")[0]
			templine = templine.split("} ")[1]
			operation = templine[1:].split("] ")[0]
			todo = templine.split("] ")[1]
			lsttoworkon = self.memory[varname]
			if operation == "#A": #add/append
				lsttoworkon.append(todo)
			if operation == "#R": #remove
				lsttoworkon.remove(todo)
			if operation == "#G": #get (index)
				return lsttoworkon[int(todo)]
			if operation == "#V": #(get) variable (index)
				return lsttoworkon[int(self.memory[todo])]
			if operation == "#C": #change (index)
				if todo.startswith("$V"): #variable
					todo = todo[3:]
					lsttoworkon[int(self.memory[todo.split(":")[0]])] = self.memory[todo.split(":")[1]]
				if todo.startswith("$N"): #no variable
					todo = todo[3:]
					lsttoworkon[int(todo.split(":")[0])] = todo.split(":")[1]
			if operation == "#L": #length
				return len(lsttoworkon)
		if line.startswith("!X"): #exit
			exit()
		else:
			return line

	def splitchars(self,charlist:list,string:str):
		index = 0
		startindex = 0
		returnlist = []
		for i in string:
			if i in charlist:
				returnlist.append(string[startindex:index])
				startindex = index + 1
			index += 1
		returnlist.append(string[startindex:])
		return returnlist

	def findchars(self,charlist:list,string:str):
		returnlist = []
		for i in string:
			if i in charlist:
				returnlist.append(i)
		return returnlist


code = open("codetest.vapl","rt")
compiler = COMPILER(code.read())