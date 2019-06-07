import glob
import os
import numpy as np
import math

def getPiName(string):
	delimiter="/"
	return string.split(delimiter)[2]

parent_dir="../LOG/"
target_file="checkSystemParams.nohup"
file_handle_out=open(parent_dir+"system_param.txt","w+")
sub_dirs=[x[0] for x in os.walk(parent_dir)]
for elem in sub_dirs:
	if(os.path.isdir(elem)):
		print(elem)
		target_path=elem+"/"+target_file
		cpu_temp=[]
		memory_usage=[]
		cpu_consumption=[]
		if(os.path.exists(target_path)):
			print("File Exists")
			pi_name=getPiName(elem)
			file_handle_in=open(target_path,"r")
			for lines in file_handle_in:
				lines=lines.strip("\r\n")
				#print(lines)
				if(lines.find("t",0,len(lines))!=-1):
					if(lines.find("Memory",0,len(lines))!=-1):
						memory_usage.append(float(lines.split(":")[1]))
					if(lines.find("CPU",0,len(lines))!=-1):
						cpu_consumption.append(float(lines.split(":")[1]))
				else:
					if(lines.find("IST",0,len(lines))==-1 and lines.find("'C",0,len(lines))!=-1):
						#print(lines.split("'")[0])
						cpu_temp.append(float(lines.split("'")[0]))
			out_string=pi_name+","+str(np.mean(cpu_temp))+","+str(np.std(cpu_temp))+","+str(math.log(np.mean(memory_usage)))+","+str(math.log(np.std(memory_usage)))+","+str(np.mean(cpu_consumption))+","+str(np.std(cpu_consumption))
			file_handle_out.write(out_string+"\n")
			file_handle_in.close()
file_handle_out.flush()
file_handle_out.close()
