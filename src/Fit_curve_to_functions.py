#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 12:14:13 2023

@author: synnoveronnekleiv
"""

# Fit curve to exponential function
# Exponential function: y = a * exp(b * x) + c
def exponential(x, a, b, c):
    return a * np.exp(b * x) + c

# Initial guesses:
a_init = y_smooth[0]
b_init = np.log(abs(y_smooth[-1]/y_smooth[0]) / (new_x[-1] - new_x[0]))
c_init = 0


params, covariance = curve_fit(exponential, new_x, y_smooth, p0=[a_init, b_init, c_init])
a_fit, b_fit, c_fit = params


# Plotting
plt.figure(figsize=(10,6))
plt.scatter(new_x, new_y, color='gray', label='Noisy Data', s=10)
#plt.plot(new_x, new_y, 'g-', label='Actual Function')
#plt.plot(new_x, y_smooth, 'r-', label='Smoothed Data')
plt.plot(new_x, exponential(new_x, a_fit, b_fit, c_fit), 'b--', label=f'Fitted Function: {a_fit:.2f} * exp({b_fit:.2f} * x)')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Fitting Smoothed Data to an Exponential Function')
plt.grid(True)
plt.show()


print(f'Fitted Function: {a_fit:.2f} * exp({b_fit:.2f} * x)')



## Fit curve to linear function
# Linear function: y= ax+b
def linear(x, a, b):
    return a * x + b

# Initial guesses:
a_init = (y_smooth[-1]/y_smooth[0]) / (new_x[-1] - new_x[0])
b_init = y_smooth[0]

params, covariance = curve_fit(linear, new_x, y_smooth, p0=[a_init, b_init])

a_fit, b_fit = params


# Plotting
plt.figure(figsize=(10,6))
plt.scatter(new_x, new_y, color='gray', label='Noisy Data', s=10)
#plt.plot(new_x, new_y, 'g-', label='Actual Function')
#plt.plot(new_x, y_smooth, 'r-', label='Smoothed Data')
plt.plot(new_x, linear(new_x, a_fit, b_fit), 'b--', label=f'Fitted Linear: {a_fit:.2f}x + {b_fit:.2f}')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Fitting Smoothed Data to an Linear Function')
plt.grid(True)
plt.show()


print(f'Fitted Linear: {a_fit:.2f}x + {b_fit:.2f}')


## Fit curve to second-order polynom function
# Second order polynom function: y= ax^2 + bx + c
# Given x values and the coefficients of the polynomial, compute y values
def quadratic(x, a, b, c):
    return a * x**2 + b * x + c


# Fit the data to a second-order polynomial function
coefficients = np.polyfit(new_x, y_smooth, 2)  # 2 indicates the degree of the polynomial (quadratic in this case)
a, b, c = coefficients

# Plotting
x_fit = np.linspace(min(new_x), max(new_x), 400)  # Create more x values for a smoother curve
y_fit = quadratic(x_fit, a, b, c)

# Plotting
plt.figure(figsize=(10,6))
plt.scatter(new_x, new_y, color='gray', label='Noisy Data', s=10)
#plt.plot(new_x, new_y, 'g-', label='Actual Function')
#plt.plot(new_x, y_smooth, 'r-', label='Smoothed Data')
plt.plot(x_fit, y_fit, 'b-', label=f'Fitted Quadratic: {a:.2f}x^2 + {b:.2f}x + {c:.2f}')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Fitting Smoothed Data to an Second-order polynomial Function')
plt.grid(True)
plt.show()


print(f'Fitted Quadratic: {a:.2f}x^2 + {b:.2f}x + {c:.2f}')



# Fit curve to sigmoide curve
# Sigmoid function
def sigmoid(x, L, k, x0):
    return L / (1 + np.exp(-k * (x - x0)))

# Initial guesses:
L_guess = max(y)
k_guess = 0.1
x0_guess = np.median(x)

# Fitting with initial guesses
params, covariance = curve_fit(sigmoid, x, y, p0=[L_guess, k_guess, x0_guess], bounds=([0,-np.inf,-np.inf], [np.inf,np.inf,np.inf]))
L_fit, k_fit, x0_fit = params

# Plotting
x_fit = np.linspace(min(x), max(x), 400)  # Create more x values for a smoother curve
y_fit = sigmoid(x_fit, L_fit, k_fit, x0_fit)

plt.figure(figsize=(10,6))
plt.scatter(x, y, color='gray', label='Data', s=40)
plt.plot(x_fit, y_fit, 'b-', label=f'Fitted Sigmoid: L={L_fit:.2f}, k={k_fit:.2f}, x0={x0_fit:.2f}')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Fitting Data to a Sigmoid Function')
plt.grid(True)
plt.show()

print("y = L / (1+e^(-k(x-x0))) where:")
print(f'L={L_fit:.2f}, k={k_fit:.2f}, x0={x0_fit:.2f}')