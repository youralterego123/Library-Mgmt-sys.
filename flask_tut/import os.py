def compi(m,n):
    add=m+n
    sub=m-n
    mult=m*n
    div=m%n
    return add,sub,mult,div
m=int(input("Enetr m"))    
m=int(input("Enetr n"))
add,sub,mult,div= compi(m,n) 
print(add,sub,mult,div)   