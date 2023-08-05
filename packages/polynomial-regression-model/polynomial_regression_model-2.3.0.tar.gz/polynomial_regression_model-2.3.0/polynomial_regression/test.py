import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from sklearn.metrics import r2_score

year=np.arange(0,24,2)
population=np.array([10.2,11.1,12,11.7,10.6,10,10.6,11.7,12,11.1,10.2,10.2])
def sinfunc(x, a, b, c, d):
    return a * np.sin(b * (x - np.radians(c)))+d
popt, pcov = curve_fit(sinfunc, year, population, p0=[1,0.4,1,5])
def prediction(x):
    a, b, c, d = popt
    return a * np.sin(b * (x - np.radians(c)))+d
x_data = np.linspace(0, 25, num=100)
plt.scatter(year,population,label='Population')
plt.plot(x_data, sinfunc(x_data, *popt), 'r-',label='Fitted function')
plt.title("Year vs Population")
plt.xlabel('Year')
plt.ylabel('Population')
plt.legend()
print(r2_score([10.2,11.1,12,11.7,10.6,10,10.6,11.7,12,11.1,10.2,10.2], prediction(year)))
plt.show()
a, b, c, d = popt
print(f'The equation of regression line is y={a:.3f} * sin({b:.3f}(x-{np.radians(c):.3f}))+{d:.3f}')