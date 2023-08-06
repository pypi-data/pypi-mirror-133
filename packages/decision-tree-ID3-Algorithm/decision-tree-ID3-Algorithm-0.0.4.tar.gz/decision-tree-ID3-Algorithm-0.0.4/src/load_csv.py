import csv
def load_csv_file(filename_train, filename_test):
    lines=csv.reader(open(filename_train,"r"))
    dataset_train = list(lines)
    headers_train = dataset_train.pop(0) 

    lines=csv.reader(open(filename_test,"r"))
    dataset_test = list(lines) 
    headers_test = dataset_test.pop(0)
    return dataset_train,headers_train,dataset_test,headers_test