import argparse
import dlib
import timeit
import csv

ap = argparse.ArgumentParser() #Creating an arg parse object
ap.add_argument("-p", "--predictor", required=True, help="Path to the trained DAT file.") #Model Input
ap.add_argument("-t", "--test", required=True, help="Path to testing XML") #Path to testing XML
ap.add_argument("-x", "--train", required=True, help="Path to Training XML") #Path to testing XML
args = vars(ap.parse_args()) #Parsing them here

print("\n\nEvaluating our Custom Model against our Train XML ")

TrainStart = timeit.default_timer()
print("Start Time: " + str(TrainStart))
errTrain = dlib.test_shape_predictor(args["train"],args["predictor"])
TrainStop = timeit.default_timer()
print("The approximate error was: "+str(errTrain))
print("Stop Time: "+ str(TrainStop))
print("\n\nRuntime: " + str(TrainStop-TrainStart))


print("\n\nEvaluating our Custom Model against our Test XML ")

TestStart = timeit.default_timer()
print("Start Time: " + str(TestStart))
errTest = dlib.test_shape_predictor(args["test"],args["predictor"])
TestStop = timeit.default_timer()
print("The approximate error was: "+str(errTest))
print("Stop Time: "+ str(TestStop))
print("\n\n Runtime: " + str(TestStop-TestStart))

print("\n\n Total Runtime:" + str(TestStop-TrainStart))

with open ("ModelError.csv","a+",newline="\n") as FileObj:
	WriteObj = csv.writer(FileObj)
	NmStart = args["predictor"].find("Cust")
	NameOfFile = args["predictor"]
	NameOfFile = NameOfFile[NmStart:]
	Lst = [NameOfFile,errTest,errTrain]
	WriteObj.writerow(Lst)
print("\n\nData written sucessfully!")