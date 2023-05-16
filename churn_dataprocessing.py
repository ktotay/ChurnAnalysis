# -*- coding: utf-8 -*-
"""Churn_DataProcessing.ipynb

Automatically generated by Colaboratory.

"""

# Analizler için gerekli kütüphaneler
import pandas as pd
from scipy.stats import shapiro
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

"""# ***Veri Setinin Durumu ve Değişken İsimlendirme***"""

df = pd.read_csv("churn_Demo.txt", delimiter=",", decimal=".")
# delimiter kısmı txt dosyasındaki sınıflandırma ayrımını virgüle göre yapar.
# decimal kısmı nümerik verilerde ondalıklı kısmın nokta ile ayrıldığını belirtir.

df.isnull().sum()

df.shape

df.dtypes

df= df.rename(columns= {"Roaming": "Yurtdisinda_Dolasim_Konusma"})
df= df.rename(columns= {"International": "Uluslararasi_Konusma"})
df= df.rename(columns= {"Local": "Yurtici_Konusma"})
df= df.rename(columns= {"Dropped": "Hat_Dusme_Sayisi"})
df= df.rename(columns= {"Paymethod": "Odeme_Yontemi"})
df= df.rename(columns= {"LocalPlan": "Yurtici_Tarifesi"})
df= df.rename(columns= {"RoamingPlan": "Dolasim_Tarifesi"})
df= df.rename(columns= {"Sex": "Cinsiyet"})
df= df.rename(columns= {"Status": "Medeni_Durum"})
df= df.rename(columns= {"Children": "Cocuk_Sayisi"})
df= df.rename(columns= {"Est_Income": "Tahmini_Gelir"})
df= df.rename(columns= {"Car_Owner": "Arac_Sahipliği"})
df= df.rename(columns= {"Usage": "Toplam_Konusma"})
df= df.rename(columns= {"Age": "Yas"})
df= df.rename(columns= {"Overall_Satisfaction": "Genel_Memnuniyet"})

df.dtypes

df.isnull().sum()

df.to_excel("Churn_Demo.xlsx", index=False)
# index=False kısmı sayesinde veri setinde yer alan başlıkların olduğu satır veri setine dahil edilmeyecek.

"""# ***Gereksiz Değişkenleri Silinmesi***"""

df = df.drop("ID", axis=1)

"""# ***Kategorik Değişkenler için:***

- Likert İsimlendirme (Faktörler) ve Değişken Seçimi

- Çapraz Tablolar

- Object Veri Tiplerini Kategorik Veri Tipi Haline Getirme
 
- Dummy Yöntemi
"""

df.head()

"""# ***Likert İsimlendirme (Faktörler) ve Değişken Seçimi***"""

df["Hat_Dusme_Sayisi"].value_counts()

# Hat_Dusme_Sayisi değişkenini binary forma getirildi. 
# 0:Hat Düşmedi, 1: Hat düştü
df["Hat_Dusme_Sayisi"] = df["Hat_Dusme_Sayisi"].apply(lambda x: "0" if x == 0 else "1")
df["Hat_Dusme_Sayisi"].value_counts()

df["Odeme_Yontemi"].value_counts()

df["Odeme_Yontemi"].replace({"CC": "Kredi_Kartı_Odeme", "Auto": "Otomatik_Odeme", "CH": "Nakit_Odeme"}, inplace=True)
df["Odeme_Yontemi"].value_counts()

df["Yurtici_Tarifesi"].value_counts()

df["Yurtici_Tarifesi"].replace({"Budget": "Yurtici_Sınırsız", "FreeLocal": "Yurtici_Sınırlı"}, inplace=True)
df["Yurtici_Tarifesi"].value_counts()

df["Dolasim_Tarifesi"].value_counts()

df["Dolasim_Tarifesi"].replace({"Standard": "Dolasim_Tarifesi_Standart", "Intnl_discount": "Dolasim_Tarifesi_Indirimli"}, inplace=True)
df["Dolasim_Tarifesi"].value_counts()

df["Cinsiyet"].value_counts()

df["Cinsiyet"].replace({"F": "Kadin", "M": "Erkek"}, inplace=True)
df["Cinsiyet"].value_counts()

df["Medeni_Durum"].value_counts()

df["Medeni_Durum"].replace({"M": "Evli", "S": "Bekar", "D": "Bosanmis"}, inplace=True)
df["Medeni_Durum"].value_counts()

df["Cocuk_Sayisi"].value_counts()

# Çocuğu olanlar: 1, Çocuğu olmayanlar:0
df["Cocuk_Sayisi"] = df["Cocuk_Sayisi"].apply(lambda x: "0" if x == 0 else "1")
df["Cocuk_Sayisi"].value_counts()

df["Arac_Sahipliği"].value_counts()

df["Arac_Sahipliği"].replace({"Y": "Evet", "N": "Hayır"}, inplace=True)
df["Arac_Sahipliği"].value_counts()

# "Yas" değişkenindeki nümerik verileri kategorik hale getirdik, binnig(sepetleme)
# 0-18:C, 18-25:G , 25-65:OY, 65+:Y
df["Yas"] = pd.cut(x=df["Yas"], bins=[0, 18, 25, 65, 120], labels=["C", "G", "OY", "Y"])
df["Yas"].value_counts()

df["Genel_Memnuniyet"].value_counts()

# I: iyi, O: orta, K: kötü
df["Genel_Memnuniyet"] = df["Genel_Memnuniyet"].replace({1: "I", 2: "O", 3: "O", 4:"K"})
df["Genel_Memnuniyet"].value_counts()

df["Churn"].value_counts()

df["Churn"].replace({"Current": "Hala_Müsteri", "Vol": "Terkeden_Musteri"}, inplace=True)
df["Churn"].value_counts()

df.dtypes

"""# ***Çapraz Tablolar***"""

Hat_Dusme_Sayisi = df["Hat_Dusme_Sayisi"]
Churn = df["Churn"]
HDS_C_crosstab = pd.crosstab(Hat_Dusme_Sayisi, Churn)
HDS_C_crosstab

Odeme_Yontemi = df["Odeme_Yontemi"]
Churn = df["Churn"]
OD_C_crosstab = pd.crosstab(Odeme_Yontemi, Churn)
OD_C_crosstab

Yurtici_Tarifesi = df["Yurtici_Tarifesi"]
Churn = df["Churn"]
YT_C_crosstab = pd.crosstab(Yurtici_Tarifesi, Churn)
YT_C_crosstab

Dolasim_Tarifesi = df["Dolasim_Tarifesi"]
Churn = df["Churn"]
DT_C_crosstab = pd.crosstab(Dolasim_Tarifesi, Churn)
DT_C_crosstab

Cinsiyet = df["Cinsiyet"]
Churn = df["Churn"]
C_C_crosstab = pd.crosstab(Cinsiyet, Churn)
C_C_crosstab

Medeni_Durum = df["Medeni_Durum"]
Churn = df["Churn"]
MD_C_crosstab = pd.crosstab(Medeni_Durum, Churn)
MD_C_crosstab

Cocuk_Sayisi = df["Cocuk_Sayisi"]
Churn = df["Churn"]
CS_C_crosstab = pd.crosstab(Cocuk_Sayisi, Churn)
CS_C_crosstab

Arac_Sahipliği = df["Arac_Sahipliği"]
Churn = df["Churn"]
AS_C_crosstab = pd.crosstab(Arac_Sahipliği, Churn)
AS_C_crosstab

Yas = df["Yas"]
Churn = df["Churn"]
Y_C_crosstab = pd.crosstab(Yas, Churn)
Y_C_crosstab

Genel_Memnuniyet = df["Genel_Memnuniyet"]
Churn = df["Churn"]
GM_C_crosstab = pd.crosstab(Genel_Memnuniyet, Churn)
GM_C_crosstab

"""# ***Object Veri Tiplerini Kategorik Veri Tipi Haline Getirme***

"""

# Object veri tipine sahip olan liketli değişkenler, modelin performansına etki edebileceği için kategorik veri tipine dönüştürülecek.
df["Hat_Dusme_Sayisi"] = pd.Categorical(df["Hat_Dusme_Sayisi"], categories=["0", "1"], ordered=True)
df["Odeme_Yontemi"] = pd.Categorical(df["Odeme_Yontemi"], categories=["Kredi_Kartı_Odeme", "Otomatik_Odeme", "Nakit_Odeme"], ordered=True)
df["Yurtici_Tarifesi"] = pd.Categorical(df["Yurtici_Tarifesi"], categories=["Yurtici_Sınırsız", "Yurtici_Sınırlı"], ordered=True)
df["Dolasim_Tarifesi"] = pd.Categorical(df["Dolasim_Tarifesi"], categories=["Dolasim_Tarifesi_Standart", "Dolasim_Tarifesi_Indirimli"], ordered=True)
df["Cinsiyet"] = pd.Categorical(df["Cinsiyet"], categories=["Kadin", "Erkek"], ordered=True)
df["Medeni_Durum"] = pd.Categorical(df["Medeni_Durum"], categories=["Evli", "Bekar", "Basanmis"], ordered=True)
df["Cocuk_Sayisi"] = pd.Categorical(df["Cocuk_Sayisi"], categories=["1", "0"], ordered=True)
df["Arac_Sahipliği"] = pd.Categorical(df["Arac_Sahipliği"], categories=["Y", "N"], ordered=True)
df["Genel_Memnuniyet"] = pd.Categorical(df["Genel_Memnuniyet"], categories=["O", "I", "K"], ordered=True)
df["Churn"] = pd.Categorical(df["Churn"], categories=["Hala_Müsteri", "Terkeden_Musteri"], ordered=True)

"""# ***Dummy Yöntemi***"""

# Kategorik veri tipindeki değişkenler için Dummy Yöntemi
df = pd.get_dummies(df, columns=["Hat_Dusme_Sayisi", "Odeme_Yontemi", "Yurtici_Tarifesi", "Dolasim_Tarifesi", "Cinsiyet", "Medeni_Durum", "Cocuk_Sayisi", "Arac_Sahipliği", 
                                 "Yas", "Genel_Memnuniyet", "Churn"])

df.head()

"""# ***Nümerik Değişkenler için:***

- Histogram grafiği

- Merkezi eğilim ölçüleri

- Aykırı değer kontrolü (boxplot)

- Shapiro-Wilk testi (Normallik)

- Aykırı değerlerin yerlerini bulma ve kontrol (Tukey method)

- Ölçeklendirme - Normalleştirme (Min-Max)
"""

# "Yurtdisinda_Dolasim_Konusma" değişkeninin histogramını çizilmesi
sns.histplot(data=df, x="Yurtdisinda_Dolasim_Konusma")
plt.show()

# Yurtdisinda_Dolasim_Konusma değişkeni için merkezi eğilim ölçüleri
Yurtdisinda_Dolasim_Konusma_mean = df["Yurtdisinda_Dolasim_Konusma"].mean()
Yurtdisinda_Dolasim_Konusma_median = df["Yurtdisinda_Dolasim_Konusma"].median()
Yurtdisinda_Dolasim_Konusma_mode = df["Yurtdisinda_Dolasim_Konusma"].mode()[0]

print("Aritmetik Ortalama: ", Yurtdisinda_Dolasim_Konusma_mean)
print("Medyan: ", Yurtdisinda_Dolasim_Konusma_median)
print("Mod: ", Yurtdisinda_Dolasim_Konusma_mode)

# Aykırı değerleri görmek için box plot grafiği
sns.boxplot(x=df["Yurtdisinda_Dolasim_Konusma"])

# Aykırı değerleri bulmak için kullanılacak yöntemin seçimi için değişkene Normallik testi
# Shapiro-Wilk testini uygulanması
Yurtdisinda_Dolasim_Konusma_stat, Yurtdisinda_Dolasim_Konusma_p = shapiro(df["Yurtdisinda_Dolasim_Konusma"])

# p değeri kontrolü
alpha = 0.05
if Yurtdisinda_Dolasim_Konusma_p > alpha:
    print("Yurtdisinda_Dolasim_Konusma sütunu normal dağılır.")
else:
    print("Yurtdisinda_Dolasim_Konusma sütunu normal dağılmaz.")

# Sütundaki değerlerin IQR değerini hesaplama
Yurtdisinda_Dolasim_Konusma_Q1 = df["Yurtdisinda_Dolasim_Konusma"].quantile(0.25)
Yurtdisinda_Dolasim_Konusma_Q3 = df["Yurtdisinda_Dolasim_Konusma"].quantile(0.75)
Yurtdisinda_Dolasim_Konusma_IQR = Yurtdisinda_Dolasim_Konusma_Q3 - Yurtdisinda_Dolasim_Konusma_Q1

# Aykırı değerleri bulma
Yurtdisinda_Dolasim_Konusma_outliers = []
for index, value in df["Yurtdisinda_Dolasim_Konusma"].items():
    if value < Yurtdisinda_Dolasim_Konusma_Q1 - 1.5 * Yurtdisinda_Dolasim_Konusma_IQR or value > Yurtdisinda_Dolasim_Konusma_Q3 + 1.5 * Yurtdisinda_Dolasim_Konusma_IQR:  # Tukey's IQR yöntemi
        Yurtdisinda_Dolasim_Konusma_outliers.append((index, value))
print("Aykırı Değerler: ", Yurtdisinda_Dolasim_Konusma_outliers)

# "Uluslararasi_Konusma" değişkeninin histogramını çizilmesi
sns.histplot(data=df, x="Uluslararasi_Konusma")
plt.show()

# Uluslararasi_Konusma değişkeni için merkezi eğilim ölçüleri
Uluslararasi_Konusma_mean = df["Uluslararasi_Konusma"].mean()
Uluslararasi_Konusma_median = df["Uluslararasi_Konusma"].median()
Uluslararasi_Konusma_mode = df["Uluslararasi_Konusma"].mode()[0]

print("Aritmetik Ortalama: ", Uluslararasi_Konusma_mean)
print("Medyan: ", Uluslararasi_Konusma_median)
print("Mod: ", Uluslararasi_Konusma_mode)

# Aykırı değerleri görmek için box plot grafiği
sns.boxplot(x=df["Uluslararasi_Konusma"])

# Aykırı değerleri bulmak için kullanılacak yöntemin seçimi için değişkene Normallik testi
# Shapiro-Wilk testini uygulanması
Uluslararasi_Konusma_stat, Uluslararasi_Konusma_p = shapiro(df["Uluslararasi_Konusma"])

# p değeri kontrolü
alpha = 0.05
if Uluslararasi_Konusma_p > alpha:
    print("Uluslararasi_Konusma sütunu normal dağılır.")
else:
    print("Uluslararasi_Konusma sütunu normal dağılmaz.")

# Sütundaki değerlerin IQR değerini hesaplama
Uluslararasi_Konusma_Q1 = df["Uluslararasi_Konusma"].quantile(0.25)
Uluslararasi_Konusma_Q3 = df["Uluslararasi_Konusma"].quantile(0.75)
Uluslararasi_Konusma_IQR = Uluslararasi_Konusma_Q3 - Uluslararasi_Konusma_Q1

# Aykırı değerleri bul ve yerlerini yazdırma
Uluslararasi_Konusma_outliers = []
for index, value in df["Uluslararasi_Konusma"].items():
    if value < Uluslararasi_Konusma_Q1 - 1.5 * Uluslararasi_Konusma_IQR or value > Uluslararasi_Konusma_Q3 + 1.5 * Uluslararasi_Konusma_IQR:  # Tukey's IQR yöntemi
        Uluslararasi_Konusma_outliers.append((index, value))
print("Aykırı Değerler: ", Uluslararasi_Konusma_outliers)

# "Yurtici_Konusma" değişkeninin histogramını çizilmesi
sns.histplot(data=df, x="Yurtici_Konusma")
plt.show()

# Yurtici_Konusma değişkeni için merkezi eğilim ölçüleri
Yurtici_Konusma_mean = df["Yurtici_Konusma"].mean()
Yurtici_Konusma_median = df["Yurtici_Konusma"].median()
Yurtici_Konusma_mode = df["Yurtici_Konusma"].mode()[0]

print("Aritmetik Ortalama: ", Yurtici_Konusma_mean)
print("Medyan: ", Yurtici_Konusma_median)
print("Mod: ", Yurtici_Konusma_mode)

# Aykırı değerleri görmek için box plot grafiği
sns.boxplot(x=df["Yurtici_Konusma"])

# Aykırı değerleri bulmak için kullanılacak yöntemin seçimi için değişkene Normallik testi
# Shapiro-Wilk testini uygulanması
Yurtici_Konusma_stat, Yurtici_Konusma_p = shapiro(df["Yurtici_Konusma"])

# p değeri kontrolü
alpha = 0.05
if Yurtici_Konusma_p > alpha:
    print("Yurtici_Konusma sütunu normal dağılır.")
else:
    print("Yurtici_Konusma sütunu normal dağılmaz.")

# Sütundaki değerlerin IQR değerini hesaplama
Yurtici_Konusma_Q1 = df["Yurtici_Konusma"].quantile(0.25)
Yurtici_Konusma_Q3 = df["Yurtici_Konusma"].quantile(0.75)
Yurtici_Konusma_IQR = Yurtici_Konusma_Q3 - Yurtici_Konusma_Q1

# Aykırı değerleri bul ve yerlerini yazdırma
Yurtici_Konusma_outliers = []
for index, value in df["Yurtici_Konusma"].items():
    if value < Yurtici_Konusma_Q1 - 1.5 * Yurtici_Konusma_IQR or value > Yurtici_Konusma_Q3 + 1.5 * Yurtici_Konusma_IQR:  # Tukey's IQR yöntemi
        Yurtici_Konusma_outliers.append((index, value))
print("Aykırı Değerler: ", Yurtici_Konusma_outliers)

# "Tahmini_Gelir" değişkeninin histogramını çizilmesi
sns.histplot(data=df, x="Tahmini_Gelir")
plt.show()

# Tahmini_Gelir değişkeni için merkezi eğilim ölçüleri
Tahmini_Gelir_mean = df["Tahmini_Gelir"].mean()
Tahmini_Gelir_median = df["Tahmini_Gelir"].median()
Tahmini_Gelir_mode = df["Tahmini_Gelir"].mode()[0]

print("Aritmetik Ortalama: ", Tahmini_Gelir_mean)
print("Medyan: ", Tahmini_Gelir_median)
print("Mod: ", Tahmini_Gelir_mode)

# Aykırı değerleri görmek için box plot grafiği
sns.boxplot(x=df["Tahmini_Gelir"])

# Aykırı değerleri bulmak için kullanılacak yöntemin seçimi için değişkene Normallik testi
# Shapiro-Wilk testini uygulanması
Tahmini_Gelir_stat, Tahmini_Gelir_p = shapiro(df["Tahmini_Gelir"])

# p değeri kontrolü
alpha = 0.05
if Tahmini_Gelir_p > alpha:
    print("Tahmini_Gelir sütunu normal dağılır.")
else:
    print("Tahmini_Gelir sütunu normal dağılmaz.")

# Sütundaki değerlerin IQR değerini hesaplama
Tahmini_Gelir_Q1 = df["Tahmini_Gelir"].quantile(0.25)
Tahmini_Gelir_Q3 = df["Tahmini_Gelir"].quantile(0.75)
Tahmini_Gelir_IQR = Tahmini_Gelir_Q3 - Tahmini_Gelir_Q1

# Aykırı değerleri bul ve yerlerini yazdırma
Tahmini_Gelir_outliers = []
for index, value in df["Tahmini_Gelir"].items():
    if value < Tahmini_Gelir_Q1 - 1.5 * Tahmini_Gelir_IQR or value > Tahmini_Gelir_Q3 + 1.5 * Tahmini_Gelir_IQR:  # Tukey's IQR yöntemi
        Tahmini_Gelir_outliers.append((index, value))
print("Aykırı Değerler: ", Tahmini_Gelir_outliers)

# "Toplam_Konusma" değişkeninin histogramını çizilmesi
sns.histplot(data=df, x="Toplam_Konusma")
plt.show()

# Toplam_Konusma değişkeni için merkezi eğilim ölçüleri
Toplam_Konusma_mean = df["Toplam_Konusma"].mean()
Toplam_Konusma_median = df["Toplam_Konusma"].median()
Toplam_Konusma_mode = df["Toplam_Konusma"].mode()[0]

print("Aritmetik Ortalama: ", Toplam_Konusma_mean)
print("Medyan: ", Toplam_Konusma_median)
print("Mod: ", Toplam_Konusma_mode)

# Aykırı değerleri görmek için box plot grafiği
sns.boxplot(x=df["Toplam_Konusma"])

# Aykırı değerleri bulmak için kullanılacak yöntemin seçimi için değişkene Normallik testi
# Shapiro-Wilk testini uygulanması
Toplam_Konusma_stat, Toplam_Konusma_p = shapiro(df["Toplam_Konusma"])

# p değeri kontrolü
alpha = 0.05
if Toplam_Konusma_p > alpha:
    print("Toplam_Konusma sütunu normal dağılır.")
else:
    print("Toplam_Konusma sütunu normal dağılmaz.")

# Sütundaki değerlerin IQR değerini hesaplama
Toplam_Konusma_Q1 = df["Toplam_Konusma"].quantile(0.25)
Toplam_Konusma_Q3 = df["Toplam_Konusma"].quantile(0.75)
Toplam_Konusma_IQR = Toplam_Konusma_Q3 - Toplam_Konusma_Q1

# Aykırı değerleri bul ve yerlerini yazdırma
Toplam_Konusma_outliers = []
for index, value in df["Toplam_Konusma"].items():
    if value < Toplam_Konusma_Q1 - 1.5 * Toplam_Konusma_IQR or value > Toplam_Konusma_Q3 + 1.5 * Toplam_Konusma_IQR:  # Tukey's IQR yöntemi
        Toplam_Konusma_outliers.append((index, value))
print("Aykırı Değerler: ", Toplam_Konusma_outliers)

"""# ***Normalleştirme***"""

from sklearn.preprocessing import MinMaxScaler
Normellestirme = ["Yurtdisinda_Dolasim_Konusma", "Uluslararasi_Konusma", "Yurtici_Konusma", "Tahmini_Gelir", "Toplam_Konusma"]
scaler = MinMaxScaler()
df[Normellestirme] = scaler.fit_transform(df[Normellestirme])

df.head()

df.dtypes

"""# ***Korelasyon Matrisleri ve Hesapları***

"""

corr_matrix = df.corr()

# Korelasyon matrisinin ısı haritasının çizilmesi
sns.heatmap(corr_matrix, cmap="coolwarm", annot=True)

important_features = corr_matrix[corr_matrix["Churn_Hala_Müsteri"] > 0.1].index.tolist()

# Önemli değişkenlerin yazdırılması
print(important_features)

"""# ***Feature Selection***"""

from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestRegressor
X = df.drop(["Churn_Hala_Müsteri", "Churn_Terkeden_Musteri"], axis=1)
y = df["Churn_Hala_Müsteri"]


# RFE yöntemi
estimator = RandomForestRegressor(n_estimators=100, random_state=42)
rfe = RFE(estimator, n_features_to_select=3)
rfe.fit(X, y)

selected_features = pd.DataFrame({"Feature": list(X.columns),
                                  "Ranking": rfe.ranking_})
selected_features = selected_features[selected_features["Ranking"]==1]
print(selected_features)

"""# ***Bağımsız(X) ve Bağımlı(y) Değişkenlerin Seçimi ve Önişlemesi Yapılmış Veri Seti***"""

# Feature selection yöntemine göre model için önemli olabilecek değişkeneler
# X = df[["Yurtdisinda_Dolasim_Konusma", "Tahmini_Gelir", "Toplam_Konusma"]]
# y = df["Churn_Hala_Müsteri"]

# Korelasyon matrisi yöntemine göre model için önemli olabilecek değişkenler
# X = df[["Uluslararasi_Konusma", "Odeme_Yontemi_Kredi_Kartı_Odeme", "Cinsiyet_Erkek", "Medeni_Durum_Evli"]]
# y = df["Churn_Hala_Müsteri"]

df.to_excel("Churn_PrePro.xlsx", index=False)

# Modellerde, her iki yöntem için analizler yapılacaktır. Daha başarılı olan modelin son halinde yer alacaktır.
# Önişleme sonucunda kısa bir yorum olarak veri setinin dengesiz olduğunu söyleyebilirim.