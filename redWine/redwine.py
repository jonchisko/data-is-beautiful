from sklearn import svm
import numpy as np
import pandas as pd
import scipy.stats as stats
from matplotlib import pyplot as plt

df = pd.read_csv("wineQualityReds.csv.xls", encoding="latin1")

print(df.head())

for x in df.columns:
    print(x)
    print("mean:", np.mean(df[x]))
    print("std:", np.std(df[x]))
    print("Ali je to normalna distribucija:", stats.normaltest(df[x]))
"""
Unnamed: 0
mean: 800.0
std: 461.5914499497003
Ali je to normalna distribucija: NormaltestResult(statistic=1255.5660015661529, pvalue=2.2767058698004423e-273)
fixed.acidity
mean: 8.319637273295838
std: 1.7405518001102782
Ali je to normalna distribucija: NormaltestResult(statistic=224.53087840457746, pvalue=1.7528277735470436e-49)
volatile.acidity
mean: 0.5278205128205131
std: 0.17900370424468975
Ali je to normalna distribucija: NormaltestResult(statistic=143.4193435598286, pvalue=7.1925890397566919e-32)
citric.acid
mean: 0.2709756097560964
std: 0.1947402144523329
Ali je to normalna distribucija: NormaltestResult(statistic=152.039214793795, pvalue=9.6628222592810181e-34)
residual.sugar
mean: 2.5388055034396517
std: 1.4094871124880504
Ali je to normalna distribucija: NormaltestResult(statistic=1520.3239698236891, pvalue=0.0)
chlorides
mean: 0.08746654158849257
std: 0.04705058260331576
Ali je to normalna distribucija: NormaltestResult(statistic=1783.1059225626427, pvalue=0.0)
free.sulfur.dioxide
mean: 15.874921826141339
std: 10.456885614930723
Ali je to normalna distribucija: NormaltestResult(statistic=342.25914842512378, pvalue=4.779365332171477e-75)
total.sulfur.dioxide
mean: 46.46779237023139
std: 32.88503665178367
Ali je to normalna distribucija: NormaltestResult(statistic=487.42725648953467, pvalue=1.4338908343435381e-106)
density
mean: 0.9967466791744833
std: 0.0018867437008323923
Ali je to normalna distribucija: NormaltestResult(statistic=30.707749940958617, pvalue=2.1473202738030206e-07)
pH
mean: 3.311113195747343
std: 0.15433818141060152
Ali je to normalna distribucija: NormaltestResult(statistic=33.684697471483915, pvalue=4.8468645347727716e-08)
sulphates
mean: 0.6581488430268921
std: 0.16945396724179526
Ali je to normalna distribucija: NormaltestResult(statistic=906.89444792270365, pvalue=1.1759065222978855e-197)
alcohol
mean: 10.422983114446502
std: 1.0653343003437463
Ali je to normalna distribucija: NormaltestResult(statistic=154.17806951912516, pvalue=3.3163288473185496e-34)
quality
mean: 5.6360225140712945
std: 0.8073168769639486
Ali je to normalna distribucija: NormaltestResult(statistic=17.262400816355541, pvalue=0.00017845030333854989)
_______
Vidimo, da nobena od kategorij ne pripada normalni distribuciji
Za standardiziranje kategorij bom uporabil kar rescale?
"""




# rescale data to 0  - 1
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

#sel = VarianceThreshold(threshold=(0.8*(1-0.8)))
#sel = SelectKBest(chi2, k=11)
#trainAtributi = sel.fit_transform(trainAtributi, trainRazred)
#testAtributi = sel.fit_transform(testAtributi, testRazred)

### VEČINSKI KLASIFIKATOR
from collections import defaultdict
from sklearn.neural_network import MLPClassifier

indices = np.random.permutation(len(df))
#len(df)*7//10 === len(df) * 7/10 === len(df) * 0.7
train = df.iloc[indices[:len(df)*7//10], :]
test = df.iloc[indices[-len(df)*7//10:], :]

trainAtributi = train.iloc[:, 1:-1]
trainRazred = train.iloc[:, -1]

testAtributi = test.iloc[:, 1:-1]
testRazred = test.iloc[:, -1]

slovar = defaultdict(int)
for x in trainRazred:
    slovar[x] += 1
maksimalni = 0
kdo = ""
for key in slovar:
    if slovar[key] > maksimalni:
        maksimalni = slovar[key]
        kdo = key
print("Večinski razred je", kdo)
večinski = np.array(trainRazred) == kdo
vec = sum(večinski)/len(večinski)
print("Večinski klasifikator, točnost:",vec)

svmTocnost = []
nevronTocnost = []

for k in range(1):
    #razdelimo na train in test
    indices = np.random.permutation(len(df))
    #len(df)*7//10 === len(df) * 7/10 === len(df) * 0.7
    train = df.iloc[indices[:len(df)*7//10], :]
    test = df.iloc[indices[-len(df)*7//10:], :]

    trainAtributi = train.iloc[:, 1:-1]
    trainRazred = train.iloc[:, -1]

    testAtributi = test.iloc[:, 1:-1]
    testRazred = test.iloc[:, -1]

    scaler = MinMaxScaler(feature_range=(0, 1))
    trainRescaled = scaler.fit_transform(trainAtributi)


    svc = svm.SVC(kernel="linear")
    svmTocnost.append(svc.fit(trainRescaled, trainRazred).score(scaler.transform(testAtributi), testRazred))

    ### NEVRONSKE MREŽE

    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=2)
    nevronTocnost.append(clf.fit(trainRescaled, trainRazred).score(scaler.transform(testAtributi), testRazred))

sT = np.mean(svmTocnost)
nT = np.mean(nevronTocnost)
print("SVM:",sT , "\nNevronske:", nT)

"""
Večinski razred je 5
Večinski klasifikator, točnost: 0.430741733691
SVM: 0.589285714286 
Nevronske: 0.627678571429
"""


from pandas.tools.plotting import scatter_matrix

scatter_matrix(df, alpha=0.2, figsize=(20,10), diagonal="kde")
plt.show()

fig, ax = plt.subplots(figsize=(20,20))
ax.hist(df.iloc[:, -1], color="blue", alpha=0.8, align="mid")
ax.set_title("Quality")
ax.set_xlabel("Quality")
fig.savefig("Quality.pdf", bbox_inches="tight")

# Izrisi se nekaj atributov, ki korelirajo :)

#fixed.acidity
#density

fig, ax = plt.subplots(figsize=(20,20))
ax.scatter(df["fixed.acidity"], df["density"], color="blue", alpha=0.8)
ax.set_title("Correlation between f. acid. and density")
ax.set_ylabel("Density")
ax.set_xlabel("Fixed Acidity")

#calculate correlation
from scipy.stats import pearsonr

korelacija = pearsonr(df["fixed.acidity"], df["density"])
korelacija = np.round(korelacija, 4)
ax.text(6, max(df["density"]), "Korelacija: "+ str(korelacija[0]), size=10)

coeficienti, covarianca = np.polyfit(df["fixed.acidity"], df["density"], deg=3, cov=True)

# interpolacija
inter = np.linspace(min(df["fixed.acidity"]), max(df["fixed.acidity"]), 500)
# n je stopnja polinoma
n = 3
# matrix with rows 1, inter, inter**2, ...
INTER = np.vstack( [inter**(n-1) for n in range(n+1)] ).T
## matrix multiplication calculates the polynomial values
yi = np.dot(INTER, coeficienti)
# C_y = INTER*COVARIANCA*INTER.T
C_y = np.dot(INTER, np.dot(covarianca, INTER.T))
# Standard deviations are sqrt of diagonal
sig_y = np.sqrt(np.diag(C_y))

funkcija = np.poly1d(coeficienti)
ax.plot(np.unique(df["fixed.acidity"]), funkcija(np.unique(df["fixed.acidity"])), linewidth=2, color="red", alpha=0.6)
#ax.fill_between(inter, yi+sig_y, yi-sig_y, color="red", alpha=0.6)
fig.savefig("korelacija.pdf", bbox_inches="tight")
plt.show()
