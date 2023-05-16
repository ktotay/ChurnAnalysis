# -*- coding: utf-8 -*-
"""Churn_XGBoost.ipynb

Automatically generated by Colaboratory.

"""

import pandas as pd
!pip install xgboost

"""# ***Veri Seti Kontrolü***"""

# Veri setini yükleme
df = pd.read_excel("Churn_PrePro.xlsx")

df.head()

df.dtypes

!pip install scipy
from scipy.stats.mstats import winsorize
df["Yurtdisinda_Dolasim_Konusma"] = winsorize(df["Yurtdisinda_Dolasim_Konusma"], limits=[0.05, 0.05])
df["Tahmini_Gelir"] = winsorize(df["Tahmini_Gelir"], limits=[0.05, 0.05])
df["Toplam_Konusma"] = winsorize(df["Toplam_Konusma"], limits=[0.05, 0.05])

# Feature selection yöntemine göre model için önemli olabilecek değişkeneler
X = df[["Yurtdisinda_Dolasim_Konusma", "Tahmini_Gelir", "Toplam_Konusma"]]
y = df["Churn_Hala_Müsteri"]

df[["Yurtdisinda_Dolasim_Konusma", "Tahmini_Gelir", "Toplam_Konusma"]].value_counts()

"""# ***XGBoost Modeli***

- Eğitim Seti ve Test Seti

- Model Eğitme

- Eğitim ve Test Setleri için ROC Eğrisi ve Değerleri

- Accuracy, Precision, Recall, F1 Score Hesapları

- Karmaşıklık Matrisi
"""

# Veri seti, %70 eğitim seti ve %30 test seti olarak ayrıldı.
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

import xgboost as xgb
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# XGBoost modeli oluşturma
model = xgb.XGBClassifier()
# Modeli train seti üzerinde eğitme
model.fit(X_train, y_train)

# Train ve validation setleri için accuracy hesaplama
train_acc = model.score(X_train, y_train)
val_acc = model.score(X_test, y_test)

# Train ve validation setleri için accuracy değerlerini yazdırma
print("Train accuracy: ", train_acc)
print("Validation accuracy: ", val_acc)

from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

# Eğitim seti üzerinde ROC eğrisi çizme
train_probs = model.predict_proba(X_train)[:, 1]
fpr_train, tpr_train, thresholds_train = roc_curve(y_train, train_probs)
roc_auc_train = auc(fpr_train, tpr_train)
plt.figure(figsize=(10, 6))
plt.plot(fpr_train, tpr_train, label="Eğitim Seti (AUC = %0.2f)" % roc_auc_train)

# Test seti üzerinde ROC eğrisi çizme
test_probs = model.predict_proba(X_test)[:, 1]
fpr_test, tpr_test, thresholds_test = roc_curve(y_test, test_probs)
roc_auc_test = auc(fpr_test, tpr_test)
plt.plot(fpr_test, tpr_test, label="Test Seti (AUC = %0.2f)" % roc_auc_test)
plt.plot([0, 1], [0, 1], "k--")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Eğrisi")
plt.legend(loc="lower right")
plt.show()

import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
import numpy as np

train_sizes, train_scores, valid_scores = learning_curve(model, X, y, train_sizes=[0.1, 0.3, 0.5, 0.7, 0.9], cv=5)

# Performans sonuçlarını yazdırma
train_mean = np.mean(train_scores, axis=1)
valid_mean = np.mean(valid_scores, axis=1)

plt.plot(train_sizes, train_mean, label="Train seti")
plt.plot(train_sizes, valid_mean, label="Validation seti")
plt.legend()
plt.show()

params = {
    "max_depth": 3,
    "eta": 0.1,
    "objective": "binary:logistic",
    "eval_metric": "auc"
}
num_round = 100
model = xgb.train(params, dtrain, num_round)

y_pred = model.predict(dtest)

import xgboost as xgb
from sklearn.model_selection import train_test_split


# DMatrix formatına dönüştürme
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# X_val'in DMatrix formatına dönüştürülmesi
dval = xgb.DMatrix(X_test)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Eğitim setindeki tahminleri alma
train_preds = model.predict(dtrain)

# Performans ölçümlerini hesaplama
accuracy = accuracy_score(y_train, train_preds.round())
precision = precision_score(y_train, train_preds.round())
recall = recall_score(y_train, train_preds.round())
f1 = f1_score(y_train, train_preds.round())

print("Accuracy: ", accuracy)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1 Score: ", f1)

from sklearn.metrics import confusion_matrix
import seaborn as sns

# y_pred değerlerini 0.5 eşik değerine göre eşikle
y_pred_binary = [1 if x >= 0.5 else 0 for x in y_pred]

# Karmaşıklık matrisini hesapla
conf_mat = confusion_matrix(y_test, y_pred_binary)

# Karmaşıklık matrisini ısı haritası olarak görselleştir
Karmasiklik_Matrisi = pd.DataFrame(conf_mat, columns=["Tahmin edilen_D", "Tahmin edilen_Y"], index=["Gercek_D", "Gercek_Y"])
print(Karmasiklik_Matrisi)
sns.heatmap(conf_mat, annot=True, cmap="Blues")

# Modeli daha iyi sonuç verdiği için Feature Selection yöntemi kullanılmıştır.
# Modelde aykırı değerler performansı düşürmemesi için "Winsorization" methodu ile kırpılmıştır. 
# Genel olarak daha fazla veri, veri seti için daha iyi bir önişleme ile bu sorunların çözüleceğini düşünüyorum. Tabi ki farklı methodlarda 
# denenebilir.
# Veri seti dengesiz olduğu için modelin son halinde F1 skoru üzerinden yorum yapmak iyi olacaktır.