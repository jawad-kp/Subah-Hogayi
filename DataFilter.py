import argparse #To pass address as parameters instead of hard-coding it in here
import re #To filter out the parts we don't need

ap = argparse.ArgumentParser() #Creating an arg parse object
ap.add_argument("-i", "--input", required=True, help="Path to the Orignal Data File") #Input File Path
ap.add_argument("-o", "--output", required=True, help="Output Path for resulting Data File") #Outpt File Path
args = vars(ap.parse_args()) #Parsing them here

# The range for eyes and lips Lies as follows
# The right eye using [36, 42).
# The left eye with [42, 48).
# The mouth [48, 68).
#This gives us the resulting range from [35,68) as the XML is 0 indexed 

Landmarks = set(list(range(36,68))) #Setting up our landmarks based on what we have above
#It's a set so you can use it with "in" in a loop

Part = re.compile("part name='[0-9]+'") #This is our regular expression for matching something that refers to a part. Check the labels_ibug_300W_[either test or train].xml to understand why

print("Starting our Parse")

rows = open(args["input"]).read().strip().split("\n") #Holds all the rows of data in an array seperated by each new line

output = open(args["output"],"w") #Open output file in write mode

#Now we parse our stuff lol

for row in rows:
	parts = re.findall(Part,row)
	if len(parts) == 0:
		output.write("{}\n".format(row))
	else:
		#We need to process and filter data
		attr = "name='"
		i = row.find(attr)
		j = row.find("'", i + len(attr) + 1)
		name = int(row[i + len(attr):j])#Splicing string to get the part number

		if name in Landmarks:
			output.write("{}\n".format(row))

output.close()
print("Finished Parse")



