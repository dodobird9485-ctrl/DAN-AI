import math

def add(x, y):
    """Adds two numbers."""
    return x + y

def subtract(x, y):
    """Subtracts two numbers."""
    return x - y

def multiply(x, y):
    """Multiplies two numbers."""
    return x * y

def divide(x, y):
    """Divides two numbers. Handles division by zero."""
    try:
        return x / y
    except ZeroDivisionError:
        return "Error: Cannot divide by zero."

def power(x, y):
    """Calculates x to the power of y."""
    return x ** y

def square_root(x):
    """Calculates the square root of x. Handles negative input."""
    try:
        return math.sqrt(x)
    except ValueError:
        return "Error: Cannot calculate square root of a negative number."

def calculator():
    """Main calculator function."""
    print("Simple Python Calculator")
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Power")
    print("6. Square Root")

    while True:
        choice = input("Enter choice(1/2/3/4/5/6): ")

        if choice in ('1', '2', '3', '4', '5', '6'):
            try:
                if choice == '6':
                    num1 = float(input("Enter number: "))
                    result = square_root(num1)
                else:
                    num1 = float(input("Enter first number: "))
                    num2 = float(input("Enter second number: "))

                    if choice == '1':
                        result = add(num1, num2)
                    elif choice == '2':
                        result = subtract(num1, num2)
                    elif choice == '3':
                        result = multiply(num1, num2)
                    elif choice == '4':
                        result = divide(num1, num2)
                    elif choice == '5':
                        result = power(num1, num2)
                print("Result:", result)

            except ValueError:
                print("Invalid input. Please enter a number.")

            next_calculation = input("Let's do next calculation? (yes/no): ")
            if next_calculation.lower() == "no":
              break
        else:
            print("Invalid input. Please select a valid operation.")

if __name__ == "__main__":
    calculator()