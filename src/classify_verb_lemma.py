#python34 classify_verb_lemma.py ../input/qa2_two-supporting-facts_train_POS_Lemma.jl ../clusters/qa2_two-supporting-facts_train_factsOnly_cluster.json Reading Clusters...
#{'0': ['put', 'left', 'discarded', 'dropped', 'down'],
 #'1': ['grabbed', 'up', 'got', 'took', 'picked'],
 #'2': ['travelled', 'moved', 'journeyed', 'back', 'went'],
 #'3': ['football', 'apple', 'milk'],
 #'4': ['Daniel', 'Sandra', 'John', 'Mary'],
 #'5': ['garden', 'office', 'kitchen', 'hallway', 'bedroom', 'bathroom']}
#Cluster Mapping Relation
#{'0': {'4:3'}, '1': {'4:3'}, '2': {'4:5'}}

#{'verb_0': {'data': ['put', 'left', 'discarded', 'dropped', 'down'],
            #'lemma_data': ['put', 'leave', 'discard', 'drop'],
            #'set_A': ['Daniel', 'Sandra', 'John', 'Mary'],
            #'set_B': ['football', 'apple', 'milk']},
 #'verb_1': {'data': ['grabbed', 'up', 'got', 'took', 'picked'],
            #'lemma_data': ['grab', 'get', 'take', 'pick'],
            #'set_A': ['Daniel', 'Sandra', 'John', 'Mary'],
            #'set_B': ['football', 'apple', 'milk']},
 #'verb_2': {'data': ['travelled', 'moved', 'journeyed', 'back', 'went'],
            #'lemma_data': ['travel', 'move', 'journey', 'go'],
            #'set_A': ['Daniel', 'Sandra', 'John', 'Mary'],
            #'set_B': ['garden',
                      #'office',
                      #'kitchen',
                      #'hallway',
                      #'bedroom',
                      #'bathroom']}}
#verbMapping results found in ../verbMapping/qa2_two-supporting-facts_train_factsOnly_cluster_classifyVerb.json
#Provide a className for following set of verbs
#Provide a className (a : attach, d : detach, t : transport, anyOtheName) for set of verbs : ['travel', 'move', 'journey', 'go']
#t
#Provide a className for following set of verbs
#Provide a className (a : attach, d : detach, t : transport, anyOtheName) for set of verbs : ['put', 'leave', 'discard', 'drop']
#d
#Provide a className for following set of verbs
#Provide a className (a : attach, d : detach, t : transport, anyOtheName) for set of verbs : ['grab', 'get', 'take', 'pick']
#a
#{'attach': ['grab', 'get', 'take', 'pick'],
 #'detach': ['put', 'leave', 'discard', 'drop'],
 #'transport': ['travel', 'move', 'journey', 'go']}
#annotatedVerbs results found in ../annotatedVerbs/qa2_two-supporting-facts_train_factsOnly_cluster_annotatedVerb.json



import argparse
import json_lines, json
from pprint import pprint
from os.path import basename

def getFileNamePart(fileName,stripText):
    return basename(fileName).strip(stripText)

def getLemmaVerbData(posLemmaVerbDict, verbData):
    lemmaVerbs = []
    for verb in verbData:
        lemmaVerb = posLemmaVerbDict.get(verb,"")
        if lemmaVerb:
            lemmaVerbs.append(lemmaVerb)
    return lemmaVerbs

def annotateVerbs(resultDict, annotatedVerbFileName):
    annotatedVerbDict = {}
    for verb in resultDict:
        print("Provide a className for following set of verbs")
        className = input("Provide a className (a : attach, d : detach, t : transport, anyOtheName) for set of verbs : {}\n".format(resultDict[verb]["lemma_data"]))
        if className == "a":
            annotatedVerbDict["attach"] = resultDict[verb]["lemma_data"]
        elif className == "d":
            annotatedVerbDict["detach"] = resultDict[verb]["lemma_data"]
        elif className == "t":
            annotatedVerbDict["transport"] = resultDict[verb]["lemma_data"]
        else:
            annotatedVerbDict[className] = resultDict[verb]["lemma_data"]
    pprint(annotatedVerbDict)
    annotatedVerbFilePath = "../annotatedVerbs/" + annotatedVerbFileName
    with open(annotatedVerbFilePath, 'w') as outFile:
        json.dump(annotatedVerbDict, outFile, indent=4)
    print("annotatedVerbs results found in {}".format(annotatedVerbFilePath))


def identifyClasses(pos_lemmaTagged_factFile, clusters_factFile):
    classifyVerbFileName = getFileNamePart(clusters_factFile, '.json') + "_classifyVerb.json"
    annotatedVerbFileName = getFileNamePart(clusters_factFile, '.json') + "_annotatedVerb.json"
    clustersDict = {}
    entityClusterDict = {}
    with open(clusters_factFile, 'r') as clusters_File:
        print("Reading Clusters...")
        clustersDict = json.load(clusters_File)
        pprint(clustersDict)
        for clusterNo in clustersDict:
            cluster_name = 'cluster_' + clusterNo
            for clusterItem in clustersDict[clusterNo]:
                entityClusterDict[clusterItem] = clusterNo#cluster_name
    #pprint(entityClusterDict)
    
    clusterVerbDict = {}
    posLemmaVerbDict = {}
    with open(pos_lemmaTagged_factFile, 'r') as pos_lemmaFile, open(clusters_factFile, 'r') as clusters_File:
        for item in json_lines.reader(pos_lemmaFile):
            itemKeys = item.keys()
            if item['isFact']:
                pos_nn = ""
                if 'POS_NN' in itemKeys:
                    pos_nn = item['POS_NN']
                pos_nnp = ""
                if 'POS_NNP' in itemKeys:
                    pos_nnp = item['POS_NNP']
                lemma_verb = ""
                if 'Lemma_Verb' in itemKeys:
                    lemma_verb = item['Lemma_Verb']
                pos_verb = ""
                if 'POS_Verb' in itemKeys:
                    pos_verb = item['POS_Verb']
                #print(pos_nnp, pos_verb, pos_nn, lemma_verb)
                posLemmaVerbDict[pos_verb] = lemma_verb
                clusterVerb = entityClusterDict.get(pos_verb, None)
                clusterNN  = entityClusterDict.get(pos_nn, None)
                clusterNNP = entityClusterDict.get(pos_nnp, None)
                #print(clusterNNP, clusterVerb, clusterNN)
                if clusterVerb:
                    relationTuple = clusterNNP + ':' + clusterNN
                    if clusterVerb in clusterVerbDict:
                        clusterVerbDict[clusterVerb].add(relationTuple)
                    else:
                        clusterVerbDict[clusterVerb] = set([relationTuple])
    print("Cluster Mapping Relation")
    pprint(clusterVerbDict)
    print()
    resultDict = {}
    for clusterVerbId in clusterVerbDict:
        #print(clusterVerbId)
        verbDetails = {}
        verbName = 'verb_' + clusterVerbId
        verbData = clustersDict[clusterVerbId]
        for mapping in clusterVerbDict[clusterVerbId]:
            clustersMapped = mapping.split(':')
            setA = 'set_A'
            setA_Index = clustersMapped[0]
            setA_Data = clustersDict[setA_Index]
            setB = 'set_B'
            setB_Index = clustersMapped[1]
            setB_Data = clustersDict[setB_Index]
            verbDetails['data'] = verbData
            verbDetails['lemma_data'] = getLemmaVerbData(posLemmaVerbDict, verbData)
            verbDetails[setA] = setA_Data
            verbDetails[setB] = setB_Data
            resultDict[verbName] = verbDetails
    pprint(resultDict)
    resultFilePath = "../verbMapping/" + classifyVerbFileName
    with open(resultFilePath, 'w') as outFile:
        json.dump(resultDict, outFile, indent=4)
    print("verbMapping results found in {}".format(resultFilePath))
    
    annotateVerbs(resultDict, annotatedVerbFileName)

def main():
    parser = argparse.ArgumentParser(description="classify lemma verb actions into categories based on entities they connect")
    parser.add_argument("pos_lemmaTagged_factFile", help="path to jsonLines file with POS and Lemma Annotations")
    parser.add_argument("clusters_factFile", help="path to json file having clusters identified based on word embedding")
    args = parser.parse_args()
    pos_lemmaTagged_factFile = args.pos_lemmaTagged_factFile
    clusters_factFile = args.clusters_factFile
    identifyClasses(pos_lemmaTagged_factFile, clusters_factFile)

if __name__ == "__main__" : main()