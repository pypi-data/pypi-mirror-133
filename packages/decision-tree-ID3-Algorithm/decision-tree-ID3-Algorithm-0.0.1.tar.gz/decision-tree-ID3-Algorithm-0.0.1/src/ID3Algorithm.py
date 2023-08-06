from load_csv import load_csv_file
from buildTree import build_tree
from classify_data import classify
class ID3:
    def __init__(self,*args):
        if len(args) == 2:
            self.data_train,\
            self.features_train,\
            self.data_test,\
            self.features_test = load_csv_file(args[0],args[1])
        elif len(args) == 4:
            self.data_train = args[0]
            self.data_test = args[1]
            self.features_train = args[2]
            self.features_test = args[3]

    def build_tree(self):
        self.node = build_tree(self.data_train,self.features_train)

    def classify(self):
        for xtest in self.data_test:
            print("The test instance:",xtest)
            print("The label for test instance:",end="   ")   
            classify(self.node,xtest,self.features_test)  
