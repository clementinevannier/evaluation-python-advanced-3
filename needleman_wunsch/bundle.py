from needleman_wunsch import ruler
import time
import sys

if __name__ == "__main__":
    
	DATASET = sys.argv[1]
    
	with open(DATASET, "r") as dataset:
		lines = (line.rstrip() for line in dataset)
		lines = (line for line in lines if line) #ignorer les lignes blanches
		lines = list(lines)
        
		if len(lines)%2 != 0 :
			lines = lines[:-1] #enlever la derniere ligne si nombre impair
            
		t = time
		n = 1
        
		while len(lines) != 0:
			top = lines.pop(0) 			
			bottom = lines.pop(0)
			start_time = time.time()
			rul = ruler.Ruler(top, bottom)
			rul.compute()				

			print(f"====== example # {n} - distance = {rul.distance} \n")
			rtop , rbottom = rul.report()
			print(rtop)
			print(rbottom)
			print("Execution time: %s seconds" % (time.time()- start_time))			
			n += 1