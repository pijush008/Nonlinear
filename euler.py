# euler.py - CORRECTED version
import sympy as sp
import numpy as np
import math

def solve_euler(fx_str, x0, step_size=0.1, num_steps=10):
    """
    Euler Method for solving ordinary differential equations
    """
    try:
        x, t = sp.symbols('x t')
        
        # Parse the equation with better error handling
        try:
            f_x = sp.sympify(fx_str)
        except Exception as e:
            return {
                'root': None,
                'converged': False,
                'error': f'Error parsing equation: {str(e)}'
            }
        
        # Check if the equation depends on t
        depends_on_t = t in f_x.free_symbols
        
        try:
            if depends_on_t:
                f_func = sp.lambdify((x, t), f_x, modules=['math', 'numpy'])
            else:
                f_func = sp.lambdify(x, f_x, modules=['math', 'numpy'])
        except Exception as e:
            return {
                'root': None,
                'converged': False,
                'error': f'Error creating function: {str(e)}'
            }
        
        # Euler method integration
        solutions = []
        x_current = float(x0)
        
        for i in range(num_steps):
            try:
                t_val = i * step_size
                
                if depends_on_t:
                    derivative = float(f_func(x_current, t_val))
                else:
                    derivative = float(f_func(x_current))
                
                # Euler update
                x_next = x_current + step_size * derivative
                
                solutions.append({
                    'step': i + 1,
                    'time': float(t_val),
                    'x': float(x_current),
                    'dx_dt': float(derivative),
                    'x_next': float(x_next)
                })
                
                x_current = x_next
                
            except (ValueError, TypeError, ZeroDivisionError) as e:
                return {
                    'solutions': solutions,
                    'error': f'Numerical error at step {i+1}: {str(e)}',
                    'converged': False,
                    'root': float(x_current) if solutions else None
                }
        
        # Check for convergence (where dx/dt ≈ 0)
        final_derivative = solutions[-1]['dx_dt'] if solutions else None
        converged = final_derivative is not None and abs(final_derivative) < 1e-6
        
        return {
            'root': float(x_current),
            'converged': converged,
            'final_solution': float(x_current),
            'step_size': float(step_size),
            'total_steps': num_steps,
            'solutions': solutions,
            'message': 'Euler method completed successfully',
            'method': 'Euler Method'
        }
        
    except Exception as e:
        return {
            'root': None,
            'converged': False,
            'error': f'Unexpected error in Euler method: {str(e)}'
        }