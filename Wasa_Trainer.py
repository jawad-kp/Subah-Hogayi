import multiprocessing
import csv
import dlib
import argparse
import os
import timeit

ap = argparse.ArgumentParser() #Creating an arg parse object
ap.add_argument("-i", "--input", required=True, help="Path to the XML with Data") #Input File Path
ap.add_argument("-m", "--model", required=True, help="Output Path for the Model") #Outpt File Path
args = vars(ap.parse_args()) #Parsing them here

print("\n\nSetting Our Options")
options = dlib.shape_predictor_training_options()

# here we be settin em options
#Configure this for manual input later

# tree_depth
# nu
# cascade_depth
# feature_pool_size
# num_test_splits
# oversampling_amount
# oversampling_translation_jitter

options.tree_depth = 4
options.nu = 0.1
options.cascade_depth = 15
options.feature_pool_size = 400
options.num_test_splits = 60
options.oversampling_amount = 5    	
options.oversampling_translation_jitter = 0.1

options.be_verbose = True
options.num_threads = multiprocessing.cpu_count()

print("Our Options are as follows: ")
print(options)

#Training our thingy
print("Training...")

start = timeit.default_timer()
dlib.train_shape_predictor(args["input"], args["model"], options)
stop = timeit.default_timer()

print("Done Training!!")
print("\nRun-time: "+ str(stop-start))

with open ("ModelInfo.csv","a+",newline="\n") as FileObj:
	print("Writing Data")
	SizeOfModel = (os.stat(args["model"]).st_size)/1024
	Write_Obj = csv.writer(FileObj)
	NmStart = args["model"].find("Cust")
	NameOfFile = args["model"]
	NameOfFile = NameOfFile[NmStart:]
	Lst = [NameOfFile,SizeOfModel,(stop-start),options.tree_depth,options.nu,options.cascade_depth,options.feature_pool_size,options.num_test_splits,options.oversampling_amount,options.oversampling_translation_jitter]
	Write_Obj.writerow(Lst)
print("Data Written to file Sucessfully!!")