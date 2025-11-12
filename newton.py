import sympy as sp
import math

def solve_newton(fx_str, x0, tol=1e-6, max_iter=20):
    try:
        # Define symbols
        x = sp.symbols('x')
        
        # Parse the user input into a Sympy expression
        f_x = sp.sympify(fx_str)
        
        # Compute derivative
        df_x = sp.diff(f_x, x)

        # Create callable (numerical) functions
        f = sp.lambdify(x, f_x, 'math')
        df = sp.lambdify(x, df_x, 'math')
        
        # Newton-Raphson iteration
        iterations = []
        xi = x0
        
        for i in range(1, max_iter + 1):
            try:
                fxi = f(xi)
                dfxi = df(xi)
                
                iterations.append({
                    'iteration': i,
                    'x': float(xi),
                    'f(x)': float(fxi),
                    "f'(x)": float(dfxi),
                    'error': float(abs(fxi))
                })
                
                # Check for zero derivative
                if abs(dfxi) < 1e-15:
                    return {
                        'root': None,
                        'converged': False,
                        'iterations': iterations,
                        'error': 'Derivative is zero or too small. Cannot continue.'
                    }
                
                # Newton update
                xi_new = xi - fxi / dfxi
                
                # Check convergence
                if abs(f(xi_new)) < tol:
                    return {
                        'root': float(xi_new),
                        'converged': True,
                        'iterations': iterations,
                        'message': f'Converged after {i} iterations'
                    }
                
                xi = xi_new
                
            except Exception as e:
                return {
                    'root': None,
                    'converged': False,
                    'iterations': iterations,
                    'error': f'Error in iteration {i}: {str(e)}'
                }
        
        # If not converged
        return {
            'root': float(xi),
            'converged': False,
            'iterations': iterations,
            'message': f'Maximum iterations ({max_iter}) reached'
        }
        
    except Exception as e:
        return {
            'root': None,
            'converged': False,
            'error': f'Error in equation parsing: {str(e)}'
        }