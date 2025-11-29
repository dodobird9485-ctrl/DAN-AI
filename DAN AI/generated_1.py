```python
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
  """Divides two numbers."""
  if y == 0:
    return "Cannot divide by zero"
  return x / y

# Main calculator function
def calculator():
  """A simple calculator."""

  print("Select operation:")
  print("1. Add")
  print("2. Subtract")
  print("3. Multiply")
  print("4. Divide")

  while True:
    choice = input("Enter choice(1/2/3/4): ")

    if choice in ('1', '2', '3', '4'):
      try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
      except ValueError:
        print("Invalid input. Please enter a number.")
        continue

      if choice == '1':
        print(num1, "+", num2, "=", add(num1, num2))

      elif choice == '2':
        print(num1, "-", num2, "=", subtract(num1, num2))

      elif choice == '3':
        print(num1, "*", num2, "=", multiply(num1, num2))

      elif choice == '4':
        print(num1, "/", num2, "=", divide(num1, num2))
      
      next_calculation = input("Let's do next calculation? (yes/no): ")
      if next_calculation == "no":
        break
    else:
      print("Invalid input")

if __name__ == "__main__":
  calculator()
```