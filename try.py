

def area():
    b = int(input("Enter the base: "))
    h = int(input("Enter the height: "))
    a = 1/2*b*h
    print(a)


# area()

def number():
    n = int(input("Enter number: "))
    if n > 0:
        if n % 2 == 0:
            if n % 4 == 0:
                print("multiple of 4")
            else:
                print("even")
        else:
            print("odd")
    else:
        print("number is less than 0")


# number()

def phone():
    n = input("Enter phone number: ")
    if n.startswith("+254"):
        print(n)
    elif n.startswith("07"):
        print("+254"+n[1:])
    elif n.startswith("01"):
        print("+254"+n[1:])
    elif n.startswith("7"):
        print("+254"+n)
    elif n.startswith("254"):
        print("+"+n)
    else:
        print("Invalid number")


# phone()

def email():
    e = str(input("Enter email: "))
    x = e.count("@" and ".")
    if x > 0:
        print("Valid email")
    else:
        print("Invalid email")


# email()

def number():
    a = int(input("Enter number: "))
    b = int(input("Enter number: "))
    c = int(input("Enter number: "))
    if a > b and a > c:
        print("A is the largest")
    elif b > a and b > c:
        print("B is the largest")
    elif c > a and c > b:
        print("C is the largest")
    else:
        print("Invalid number")


# number()

def password():
    tries = 4
    pas = "admin@123"
    while tries > 0:
        p = input("password: ")
        if p == pas:
            print("Granted")
            break
        else:
            tries = tries-1
            print("Wrong", tries)
    if tries == 0:
        print("Blocked")

