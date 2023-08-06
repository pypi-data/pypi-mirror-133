def print_tree(node,level): 
        if node.answer!="":
            print("  "*level,node.answer)
            return
        
        print("  "*level,node.attribute) 
        for value,n in node.children:
            print("  "*(level+1),value)
            print_tree(n,level+2)