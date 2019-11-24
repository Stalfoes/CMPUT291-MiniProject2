import sys

def removeSlash():
	inf = open(sys.argv[1], 'r')
	out = open(sys.argv[2], 'w')
	
	

	for line in inf:
		line = line.replace('\\', '&92')
		k = True
		key = ''
		data = ''
		for char in line:
			if char == ':':
				k = False
			elif k:
				key = key + char
			elif not(k):
				data = data + char
		out.write(key + '\n')
		out.write(data)
			
	
if __name__ == "__main__":
	removeSlash()
