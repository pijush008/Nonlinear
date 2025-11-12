import sympy as sp
import math

# Define symbols
x, h = sp.symbols('x h')

# Take function input from user
expr_input = input("Enter the function f(x): ")
f_x = sp.sympify(expr_input)   # convert string to symbolic expression

# Compute derivative using limit definition
df_x = sp.limit((f_x.subs(x, x + h) - f_x) / h, h, 0)

# Print function and derivative
print(f"\nf(x) = {f_x}")
print(f"f'(x) = {df_x}")

# Convert symbolic functions to numerical functions
f = sp.lambdify(x, f_x, 'math')
df = sp.lambdify(x, df_x, 'math')

# Default values
x0 = 2.0
tol = 1e-6
max_iter = 20
xi = x0
converged = False

print("\nGet values from Newton-Raphson method.......\n")

# Newton-Raphson iteration loop
for i in range(1, max_iter + 1):
    fxi = f(xi)
    dfxi = df(xi)

    print(f"Iteration {i}: x = {xi}, f(x) = {fxi}, f'(x) = {dfxi}")

    if abs(dfxi) < 1e-10:
        print("Derivative is near zero. Stopping....")
        break

    xi_new = xi - fxi / dfxi

    if abs(f(xi_new)) < tol:
        converged = True
        xi = xi_new
        print("\nConverged!")
        break

    xi = xi_new

if converged:
    print(f"\nRoot ≈ {xi}")
else:
    print(f"\nDid not converge within {max_iter} iterations. Best estimate ≈ {xi}")
