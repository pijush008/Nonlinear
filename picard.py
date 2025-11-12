import sympy as sp
import math

def solve_picard(fx_str, x0, tol=1e-6, max_iter=20):
    try:
        x = sp.symbols('x')
        g = sp.sympify(fx_str)
        
        # Create callable function
        g_func = sp.lambdify(x, g, 'math')
        
        # Picard iteration
        iterations = []
        xi = x0
        
        for i in range(1, max_iter + 1):
            try:
                xi_next = g_func(xi)
                error = abs(xi_next - xi)
                
                iterations.append({
                    'iteration': i,
                    'x': float(xi),
                    'x_new': float(xi_next),
                    'error': float(error)
                })
                
                # Check convergence
                if error < tol:
                    return {
                        'root': float(xi_next),
                        'converged': True,
                        'iterations': iterations,
                        'message': f'Converged after {i} iterations'
                    }
                
                xi = xi_next
                
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