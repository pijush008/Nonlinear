

// Method descriptions
const methodDescriptions = {
    newton: "Newton-Raphson: Fast quadratic convergence for root finding.",
    picard: "Picard Iteration: Simple fixed-point iteration method.",
    euler: "Euler Method: Numerical integration for ODEs, finds equilibrium points."
};

console.log("✅ script.js loaded successfully!");

function toggleEulerFields() {
    console.log("toggleEulerFields called");
    const method = document.getElementById('method').value;
    const eulerParams = document.getElementById('eulerParams');
    
    if (method === 'euler') {
        eulerParams.style.display = 'block';
    } else {
        eulerParams.style.display = 'none';
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM Content Loaded - initializing form");
    
    // Set up method change listener
    document.getElementById('method').addEventListener('change', toggleEulerFields);
    
    // Initialize Euler fields visibility
    toggleEulerFields();
    
    // Set up form submission - MAKE SURE THIS IS WORKING
    const form = document.getElementById('solveForm');
    if (form) {
        console.log("Form found, attaching submit handler");
        form.addEventListener('submit', function(e) {
            console.log("Submit event triggered");
            e.preventDefault(); // THIS IS CRITICAL
            e.stopPropagation(); // Prevent any bubbling
            handleFormSubmit(e);
        });
    } else {
        console.error("Form not found!");
    }
});

async function handleFormSubmit(e) {
    console.log("🚀 handleFormSubmit function called");
    
    const equation = document.getElementById('equation').value.trim();
    const x0 = document.getElementById('x0').value;
    const method = document.getElementById('method').value;
    const step_size = document.getElementById('step_size').value;
    const steps = document.getElementById('steps').value;
    const output = document.getElementById('output');

    console.log("Form data:", { equation, x0, method, step_size, steps });

    // Clear previous results and errors
    output.innerHTML = '';
    
    // Reset border colors
    document.getElementById('equation').style.borderColor = '';
    document.getElementById('x0').style.borderColor = '';
    document.getElementById('method').style.borderColor = '';
    document.getElementById('step_size').style.borderColor = '';
    document.getElementById('steps').style.borderColor = '';

    // Validate inputs in JavaScript
    let errors = [];

    if (!equation) {
        errors.push("Equation is required");
        document.getElementById('equation').style.borderColor = 'red';
    }

    if (!x0) {
        errors.push("Initial value is required");
        document.getElementById('x0').style.borderColor = 'red';
    } else if (isNaN(parseFloat(x0))) {
        errors.push("Initial value must be a valid number");
        document.getElementById('x0').style.borderColor = 'red';
    }

    if (!method) {
        errors.push("Method selection is required");
        document.getElementById('method').style.borderColor = 'red';
    }

    // Euler-specific validation
    if (method === 'euler') {
        if (!step_size) {
            errors.push("Step size is required for Euler method");
            document.getElementById('step_size').style.borderColor = 'red';
        } else if (isNaN(parseFloat(step_size)) || parseFloat(step_size) <= 0) {
            errors.push("Step size must be a positive number");
            document.getElementById('step_size').style.borderColor = 'red';
        }

        if (!steps) {
            errors.push("Number of steps is required for Euler method");
            document.getElementById('steps').style.borderColor = 'red';
        } else if (isNaN(parseInt(steps)) || parseInt(steps) <= 0) {
            errors.push("Number of steps must be a positive integer");
            document.getElementById('steps').style.borderColor = 'red';
        }
    }

    // Show errors if any
    if (errors.length > 0) {
        output.innerHTML = '<div class="error"><strong>Please fix the following errors:</strong><ul>' +
            errors.map(error => `<li>${error}</li>`).join('') +
            '</ul></div>';
        return;
    }

    output.innerHTML = "<div class='loading'>🔄 Solving with " + method + " method... Please wait.</div>";

    try {
        const requestData = { 
            equation: equation, 
            x0: parseFloat(x0), 
            method: method 
        };
        
        // Add parameters for Euler method
        if (method === 'euler') {
            requestData.step_size = parseFloat(step_size);
            requestData.steps = parseInt(steps);
        }

        console.log("Sending POST request to /solve:", requestData);

        const response = await fetch('/solve', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });

        console.log("Response status:", response.status, response.statusText);

        if (!response.ok) {
            let errorMessage = `HTTP error! status: ${response.status}`;
            try {
                const errorData = await response.json();
                errorMessage = errorData.error || errorMessage;
            } catch (e) {
                // If response is not JSON, use text
                const errorText = await response.text();
                errorMessage = errorText || errorMessage;
            }
            throw new Error(errorMessage);
        }

        const data = await response.json();
        console.log("✅ Received response data:", data);

        if (data.error) {
            output.innerHTML = `<div class="error">Error: ${data.error}</div>`;
        } else {
            displayResults(data, method);
        }
    } catch (error) {
        console.error("❌ Fetch error:", error);
        output.innerHTML = `<div class="error">Network error: ${error.message}</div>`;
    }
}

function displayResults(data, method) {
    console.log("🎯 Displaying results for method:", method);
    
    const output = document.getElementById('output');
    let resultHTML = '';
    
    if (data.converged !== undefined) {
        if (data.converged) {
            resultHTML += `<div class="success">
                <h3>✅ ${data.message || 'Converged Successfully!'}</h3>
                <p><strong>Root:</strong> ${data.root !== undefined ? data.root.toFixed(6) : 'N/A'}</p>
                ${data.final_solution !== undefined ? `<p><strong>Final Solution:</strong> ${data.final_solution.toFixed(6)}</p>` : ''}
            </div>`;
        } else {
            resultHTML += `<div class="warning">
                <h3>⚠️ ${data.message || 'Did not converge'}</h3>
                ${data.root !== undefined ? `<p><strong>Best estimate:</strong> ${data.root.toFixed(6)}</p>` : ''}
                ${data.error ? `<p><strong>Error:</strong> ${data.error}</p>` : ''}
            </div>`;
        }
    } else if (data.error) {
        resultHTML += `<div class="error">Error: ${data.error}</div>`;
    } else {
        resultHTML += `<div class="warning">Unexpected response format</div>`;
    }

    // Display iterations if available
    if (data.iterations && data.iterations.length > 0) {
        resultHTML += '<h3>Iteration Details:</h3><table><thead><tr>';
        
        if (method === 'newton') {
            resultHTML += '<th>Iteration</th><th>x</th><th>f(x)</th><th>f\'(x)</th><th>Error</th>';
        } else {
            resultHTML += '<th>Iteration</th><th>x</th><th>x_new</th><th>Error</th>';
        }
        
        resultHTML += '</tr></thead><tbody>';
        
        data.iterations.forEach(iter => {
            if (method === 'newton') {
                resultHTML += `<tr>
                    <td>${iter.iteration}</td>
                    <td>${iter.x?.toFixed(6) || '0.000000'}</td>
                    <td>${iter['f(x)']?.toFixed(6) || '0.000000'}</td>
                    <td>${iter["f'(x)"]?.toFixed(6) || '0.000000'}</td>
                    <td>${iter.error?.toFixed(6) || '0.000000'}</td>
                </tr>`;
            } else {
                resultHTML += `<tr>
                    <td>${iter.iteration}</td>
                    <td>${iter.x?.toFixed(6) || '0.000000'}</td>
                    <td>${iter.x_new?.toFixed(6) || '0.000000'}</td>
                    <td>${iter.error?.toFixed(6) || '0.000000'}</td>
                </tr>`;
            }
        });
        
        resultHTML += '</tbody></table>';
    }

    output.innerHTML = resultHTML;
    console.log("✅ Results displayed successfully");
}