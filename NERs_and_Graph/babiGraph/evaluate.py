import collections
import json
import io
from Globals import Globals

if __name__ == "__main__":

    count=0
    results = ""
    with io.open(Globals.OUTPUT_GRAPH_FILE,"r") as data_file:   
        for line in data_file:
            jsonObj = json.loads(line)
            if(jsonObj['PANS']==jsonObj['answer']):
                count+=1
                results+=" Answer is "+jsonObj['answer'] + " Predicted Answer is " + jsonObj['PANS'] + " Supporting Fact " + jsonObj['supportingFactNos'][0] + " Predicted Supporting Fact " + jsonObj['PSUPPFACT'] + "\n"
    
    with io.open(Globals.EVALUATION_FILE,"w") as ofile:
        ofile.write(results)
        ofile.write("\n")
        ofile.write("\n Count of Questions correctly answered is " + str(count))            