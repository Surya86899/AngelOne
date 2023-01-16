a=int(input("Enter no 1 : "))
b=int(input("Enter no 2 : "))
choice=int(input("Enter your choice \n1.Add\n2.Sub\n3.Multi\n4.Division : "))
def add(a,b):
    return a+b
def sub(a,b):
    return a-b
def multi(a,b):
    return a*b
def division(a,b):
    return a/b      
if choice==1 :
    print(add(a,b))
elif choice==2 :
    print(sub(a,b))
elif choice==3 :
    print(multi(a,b))
elif choice==4 :
    print(division(a,b))
else:
    print('Enter valid choice!!!')  
 

