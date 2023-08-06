def classify(node,x_test,features): 
        if node.answer!="":
            print(node.answer)
            return node.answer
        pos=features.index(node.attribute)
        for value, n in node.children:
            if x_test[pos]==value:
                classify(n,x_test,features)