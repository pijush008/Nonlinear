import sympy as sp
import math


x, h = sp.symbols('x h')

f_x = 2*x-6-sp.log(x)

df_x = sp.limit((f_x.subs(x, x + h) - f_x) / h, h, 0)

print("f(x) =", f_x)
print("f'(x) =", df_x)


f = sp.lambdify(x, f_x, 'math')
df = sp.lambdify(x, df_x, 'math')


x0 = 2.0
tol = 1e-6
max_iter = 20

xi = x0
converged = False

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
        print("Converged ")
        xi = xi_new
        break
    
    xi = xi_new

if converged:
    print(f" value of : x = {xi}")
else:
    print(f"Did not converge within {max_iter} iterations. Best estimate = {xi}")