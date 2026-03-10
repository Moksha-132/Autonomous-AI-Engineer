def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b
def div(a, b): 
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    else:
        return a / b

class Calculator:
    def pow(self, a, n): return a ** n
    def sqrt(self, a): 
        if a < 0: 
            raise ValueError("Square root of negative number is not defined")
        elif a == 0 or a == 1: 
            return a
        else:
            return (a + 1) / 2

def main():
    calc = Calculator()

    while True:
        print("\nScientific Calculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Power")
        print("6. Square Root")
        print("7. Quit")

        choice = input("Choose an operation (1-7): ")

        if choice == "1":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            print(f"{num1} + {num2} = {calc.add(num1, num2)}")
        elif choice == "2":
            num1 = float(input("Enter dividend: "))
            num2 = float(input("Enter divisor: "))
            try:
                result = calc.div(num2, num1)
                print(f"{num1} / {num2} = {result}")
            except ValueError as e:
                print(e)
        elif choice == "3":
            num1 = float(input("Enter dividend: "))
            num2 = float(input("Enter divisor: "))
            try:
                result = calc.mul(num2, num1)
                print(f"{num1} * {num2} = {result}")
            except ValueError as e:
                print(e)
        elif choice == "4":
            num1 = float(input("Enter dividend: "))
            num2 = float(input("Enter divisor: "))
            try:
                result = calc.div(num2, num1)  # Changed to div()
                print(f"{num1} / {num2} = {result}")
            except ValueError as e:
                print(e)
        elif choice == "5":
            exponent = int(input("Enter power: "))
            if exponent < 0:
                print("Power must be a non-negative integer.")
            else:
                result = calc.calc_pow(exponent)
                print(f"{exponent}^2 = {result}")
        elif choice == "6":
            num1 = float(input("Enter number: "))
            try:
                result = calc.sqrt(num1)  # Changed to sqrt()
                print(f"Square root of {num1} is {result}")
            except ValueError as e:
                print(e)
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please choose a valid operation.")

if __name__ == "__main__":
    main()
