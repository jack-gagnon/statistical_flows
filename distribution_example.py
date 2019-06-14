import pandas as pd

df = pd.read_excel('path')

mu, sigma = df['colname'].mean(), df['colname'].std()

import matplotlib.pyplot as plt
count, bins, ignored = plt.hist(s, 30, normed=True)
plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
         np.exp( - (bins - mu)**2 / (2 * sigma**2)),
         linewidth=2, color='r')

plt.show()
