from buildTree import build_tree
from classify_data import classify
import csv
class ID3:
    def __init__(self,*args):
        
        self.data_train = args[0]
        self.data_test = args[2]
        self.features_train = args[1]
        self.features_test = args[3]

    def build_tree(self):
        self.node = build_tree(self.data_train,self.features_train)

    def classify(self):
        for xtest in self.data_test:
            print("The test instance:",xtest)
            print("The label for test instance:",end="   ")   
            classify(self.node,xtest,self.features_test)  

def load_csv(filename_test): 
    lines=csv.reader(open(filename_test,"r"))
    dataset = list(lines) 
    headers = dataset.pop(0) 
    return dataset,headers

dataset_test,headers_test = load_csv("e:\\PythonPackages\\decisiontree\\src\\data3_test.csv")
dataset_train,headers_train = load_csv("e:\\PythonPackages\\decisiontree\\src\\data3.csv")
id3 = ID3(dataset_train,headers_train,dataset_test,headers_test)
id3.build_tree()
id3.classify()