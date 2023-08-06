from node import Node
import math
from printTree import print_tree

def build_tree(data,features):

        node = build_tree_rec(data,features)
        print("The decision tree for the dataset using ID3 algorithm is")
        print_tree(node,0)
        return node

def build_tree_rec(data,features): 
        lastcol=[row[-1] for row in data] 
        if(len(set(lastcol)))==1: 
            node=Node("")
            node.answer=lastcol[0]
            return node
        
        n=len(data[0])-1 
        gains=[0]*n
        for col in range(n):
            gains[col]=compute_gain(data,col)
        split=gains.index(max(gains))
        node=Node(features[split])
        fea = features[:split]+features[split+1:]

        
        attr,dic=subtables(data,split,delete=True)
        
        for x in range(len(attr)):
            child=build_tree_rec(dic[attr[x]],fea)
            node.children.append((attr[x],child))
        return node

def compute_gain(data,col): 
        attr,dic = subtables(data,col,delete=False)
        
        total_size=len(data)
        entropies=[0]*len(attr)
        ratio=[0]*len(attr)
        
        total_entropy=entropy([row[-1] for row in data]) 
        for x in range(len(attr)):
            ratio[x]=len(dic[attr[x]])/(total_size*1.0)
            entropies[x]=entropy([row[-1] for row in dic[attr[x]]])
            total_entropy-=ratio[x]*entropies[x]
        return total_entropy

def subtables(data,col,delete): 
        dic={}
        coldata=[row[col] for row in data]
        attr=list(set(coldata))
        
        counts=[0]*len(attr)
        r=len(data) 
        c=len(data[0]) 
        for x in range(len(attr)):
            for y in range(r):
                if data[y][col]==attr[x]:
                    counts[x]+=1
            
        for x in range(len(attr)): 
            dic[attr[x]]=[[0 for i in range(c)] for j in range(counts[x])]
            pos=0
            for y in range(r):
                if data[y][col]==attr[x]:
                    if delete:
                        del data[y][col]
                    dic[attr[x]][pos]=data[y]
                    pos+=1
        return attr,dic

def entropy(S): 
        attr=list(set(S))
        if len(attr)==1:
            return 0
        
        counts=[0,0] 
        for i in range(2):
            counts[i]=sum([1 for x in S if attr[i]==x])/(len(S)*1.0)
        
        sums=0
        for cnt in counts:
            sums+=-1*cnt*math.log(cnt,2)
        return sums