# extracts D-optimality values & run-times from each file, with different number of runs
import matplotlib.pyplot as plt

C = 0 
D = 0
K = [2,4,8]#,4,8]
runs = [100]
k = 0 
doptimal_min = 0
doptimal_max = -999
doptimal_avg = 0 
doptimal_values = []
count = 0

# [min,max,avg]
real_time = [999,-999,0]
usr_time = [999,-999,0]
sys_time = [999,-999,0]

real_values = []
usr_values = []
sys_values = []

# takes text in format "1m0.456s" and returns total seconds
def return_seconds(value) :
	import re
	m , s = value.split('m')
	total_s = float(m)*60 + float(s[:-1])
	return total_s
	#print total_s

#ts = "real	0m0.602s"
#return_seconds(ts)
import os.path

for i in K :
	print("Opening files:")
	for r in runs :
	    file = "../logs/dumpMSMA-K" + str(i) + "-D" + str(i) + "-C0-I0-R" + str(r) + ".txt"
	    print(file)
	    if os.path.isfile(file) :
		    with open(file,"r") as f :

		    	# GETTING D-OPTIMALITY VALUES & TIMES
		    	for line in f.readlines() :
		    		line = line.rstrip()

		    		# GETTING D-OPTIMALITY VALUES
		    		if line.startswith("#") : #finding the line that has the d-optimality value
		    			value = float(line[1:].rstrip())
		    			#print value
		    			if value > doptimal_max :
		    				doptimal_max = value
		    			if value < doptimal_min :
		    				doptimal_min = value
		    			doptimal_values.append(value)

		    		# GETTING TIMES
		    		if line.startswith("real") :
		    			seconds = return_seconds(line[5:].rstrip())
		    			real_values.append(seconds)
		    			if seconds < real_time[0] :
		    				real_time[0] = seconds
		    			if seconds > real_time[1] :
		    				real_time[1] = seconds

		    		if line.startswith("user") :
		    			seconds = return_seconds(line[5:].rstrip())
		    			usr_values.append(seconds)
		    			if seconds < usr_time[0] :
		    				usr_time[0] = seconds
		    			if seconds > usr_time[1] :
		    				usr_time[1] = seconds
		    			
		    		if line.startswith("sys") :
		    			seconds = return_seconds(line[4:].rstrip())
		    			sys_values.append(seconds)
		    			if seconds < sys_time[0] :
		    				sys_time[0] = seconds
		    			if seconds > sys_time[1] :
		    				sys_time[1] = seconds


		    print ("Total number of runs: %f" % len(doptimal_values))
		    print ("Minimum D-optimal value: %f" % doptimal_min)
		    print ("Maximum D-optimal value: %f" % doptimal_max)
		    doptimal_avg = sum(doptimal_values) / float(len(doptimal_values))
		    print ("Average D-optimal value: %f" % doptimal_avg)

		    # plotting the graph
		    
		    if i == 8 :
		    	size = 1 
		    	for value in doptimal_values :
		    		plt.axis([0, r+5, -60, -40 ])
		    		plt.plot(size,value, "ro")
		    		size = size + 1
		    	plt.show()
		    '''
		    if i == 4 :
		    	size = 1 
		    	for value in doptimal_values :
		    		plt.plot(value,size, "bo")
		    if i == 8 :
		    	size = 1 
		    	for value in doptimal_values :
		    		plt.plot(value,size, "go")
		    '''


		    doptimal_values = []
		    doptimal_min = 0
		    doptimal_max = -999
		    doptimal_avg = 0

		    print ("Maximum real time: %f \nMinimum real time: %f" % (real_time[1],real_time[0]))
		    print ("Maximum usr time: %f \nMinimum usr time: %f" % (usr_time[1],usr_time[0]))
		    print ("Maximum sys time: %f \nMinimum sys time: %f" % (sys_time[1],sys_time[0]))
		    real_time[2] = sum(real_values)/(float(len(real_values)))
		    usr_time[2] = sum(usr_values)/(float(len(usr_values)))
		    sys_time[2] = sum(sys_values)/(float(len(sys_values)))
		    print ("\n\nTotal real time: %f \nTotal usr time: %f \nTotal sys time: %f" % (sum(real_values),sum(usr_values),sum(sys_values)))
		    #print ("\nAverage real time: %f \nAverage usr time: %f \nAverage sys time: %f" % (real_time[2],usr_time[2],sys_time[2]))
		    print("\n\n\n\n")

		    real_time = [999,-999,0]
		    usr_time = [999,-999,0]
		    sys_time = [999,-999,0]
		    real_values = []
		    usr_values = []
		    sys_values = []




