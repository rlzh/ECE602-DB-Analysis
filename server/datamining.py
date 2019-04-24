import pymysql
import credential
import tree
import tree2
import pandas as pd
import numpy as np

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

host = credential.host
user = credential.user
password = credential.password
database = credential.database

def categorize(df):
    for column in df:
        if len(df[column].unique().tolist()) < 4:
            continue
        cmax = df[column].max()
        cmin = df[column].min()
        #print(cmax)
        thres = (cmax - cmin)/4
        for index, row in df.iterrows():
            if row[column] - cmin > 3*thres + cmin:
                df.loc[index, column] = 3
            elif row[column] - cmin > 2*thres + cmin:
                df.loc[index, column] = 2
            elif row[column] - cmin > thres + cmin:
                df.loc[index, column] = 1
            else:
                df.loc[index, column] = 0
    return df

def newtrain(df):
    y = df.columns[-1]
    class_df = df.loc[df[y] == 1]
    non_class_df = df.loc[df[y] != 1]
    max_size = len(class_df)
    non_class_df = non_class_df.sample(n=max_size)
    result = pd.concat([class_df, non_class_df])
    result.columns = df.columns
    result = result.sample(frac=1)
    return result



# Open database connection
db = pymysql.connect(host,user,password,database)

# prepare a cursor object using cursor() method
cursor = db.cursor()

#sql = "select * from treesource limit 4000"
sql = "select * from treesource2 limit 2000"

try:
   # Execute the SQL command
    cursor.execute(sql)
   # Fetch all the rows in a list of lists.
    results = cursor.fetchall()
except:
    print ("Error: unable to fetch data")

# disconnect from server
db.close()

df = pd.DataFrame(list(results))
#df.columns = ['playerID','bG','bAB','bR','bH','b2B','b3B','bHR','bRBI','bSB','bCS','bBB','bSO','bIBB','bHBP','bSH','bSF','bpG','bpAB','bpR','bpH','bp2B','bp3B','bpHR','bpRBI','bpSB','bpCS','bpBB','bpSO','bpIBB','bpHBP','bpSH','bpSF','fPOS','fG','fGS','fIO','fPO','fA','fE','fDP','fWP','fPB','fSB','fCS','fZR','fpPOS','fpG','fpGS','fpIO','fpPO','fpA','fpE','fpDP','fpTP','fpPB','fpSB','fpCS','pW','pL','pG','pGS','pCG','pSHO','pSV','pIP','pH','pER','pHR','pBB','pSO','pBAO','pERA','pIBB','pWP','pHBP','pBK','pBFP','pGF','pR','pSH','pSF','ppW','ppL','ppG','ppGS','ppCG','ppSHO','ppSV','ppIP','ppH','ppER','ppHR','ppBB','ppSO','ppBAO','ppERA','ppIBB','ppWP','ppHBP','ppBK','ppBFP','ppGF','ppR','ppSH','ppSF','award','nom','hof','man']
df.columns = ['playerID','bG','bAB','bR','bH','b2B','b3B','bHR','bRBI','bSB','bCS','bBB','bSO','bIBB','bHBP','bSH','bSF','fPOS','fG','fGS','fIO','fPO','fA','fE','fDP','fWP','fPB','fSB','fCS','fZR','pW','pL','pG','pGS','pCG','pSHO','pSV','pIP','pH','pER','pHR','pBB','pSO','pBAO','pERA','pIBB','pWP','pHBP','pBK','pBFP','pGF','pR','pSH','pSF','award','nom','hof','man']
df.fillna(value=0, inplace=True)
y_nom = df['nom'].values.astype(int)
y_hof = df['hof'].values.astype(int)
y_man = df['man'].values.astype(int)

#cols = ['bG','bAB','bR','bH','b2B','b3B','bHR','bRBI','bSB','bCS','bBB','bSO','bIBB','bHBP','bSH','bSF','bpG','bpAB','bpR','bpH','bp2B','bp3B','bpHR','bpRBI','bpSB','bpCS','bpBB','bpSO','bpIBB','bpHBP','bpSH','bpSF','fPOS','fG','fGS','fIO','fPO','fA','fE','fDP','fWP','fPB','fSB','fCS','fZR','fpPOS','fpG','fpGS','fpIO','fpPO','fpA','fpE','fpDP','fpTP','fpPB','fpSB','fpCS','pW','pL','pG','pGS','pCG','pSHO','pSV','pIP','pH','pER','pHR','pBB','pSO','pBAO','pERA','pIBB','pWP','pHBP','pBK','pBFP','pGF','pR','pSH','pSF','ppW','ppL','ppG','ppGS','ppCG','ppSHO','ppSV','ppIP','ppH','ppER','ppHR','ppBB','ppSO','ppBAO','ppERA','ppIBB','ppWP','ppHBP','ppBK','ppBFP','ppGF','ppR','ppSH','ppSF','award']
cols = ['bG','bAB','bR','bH','b2B','b3B','bHR','bRBI','bSB','bCS','bBB','bSO','bIBB','bHBP','bSH','bSF','fPOS','fG','fGS','fIO','fPO','fA','fE','fDP','fWP','fPB','fSB','fCS','fZR','pW','pL','pG','pGS','pCG','pSHO','pSV','pIP','pH','pER','pHR','pBB','pSO','pBAO','pERA','pIBB','pWP','pHBP','pBK','pBFP','pGF','pR','pSH','pSF','award','nom','hof','man']
df = df[cols].applymap(np.int64)
#df = df[cols].round(decimals=-1)
#print(df)

########sklearn
# X_train, X_test, y_train, y_test = train_test_split(df, y_nom, random_state=1)
# model = DecisionTreeClassifier()
# model.fitv(X_train, y_train)
# y_predict = model.predict(X_test)
# print(f1_score(y_test,y_predict))

#############tree1
target = 'nom'

# df[target] = y_nom.tolist()
# print(df)
# #data = df.drop(columns=['nom','hof','man','playerID'], inplace = True)
# #nom_data = df.drop(columns=['hof','man','playerID'])
nom_data = df.drop(columns=['hof','man'])
nom_data = categorize(nom_data)
nom_data[target] = y_nom.tolist()
train, test = tree.train_test_split(nom_data)

train = newtrain(train)

print(train)
print(test)
# #print(df)
# #print ("count = %d" % (fname))

# def main():
# An example use of 'build_tree' and 'predict'
#df_train = clean('horseTrain.txt')
#attributes =  ['bG','bAB','bR','bH','b2B','b3B','bHR','bRBI','bSB','bCS','bBB','bSO','bIBB','bHBP','bSH','bSF','bpG','bpAB','bpR','bpH','bp2B','bp3B','bpHR','bpRBI','bpSB','bpCS','bpBB','bpSO','bpIBB','bpHBP','bpSH','bpSF','fPOS','fG','fGS','fIO','fPO','fA','fE','fDP','fWP','fPB','fSB','fCS','fZR','fpPOS','fpG','fpGS','fpIO','fpPO','fpA','fpE','fpDP','fpTP','fpPB','fpSB','fpCS','pW','pL','pG','pGS','pCG','pSHO','pSV','pIP','pH','pER','pHR','pBB','pSO','pBAO','pERA','pIBB','pWP','pHBP','pBK','pBFP','pGF','pR','pSH','pSF','ppW','ppL','ppG','ppGS','ppCG','ppSHO','ppSV','ppIP','ppH','ppER','ppHR','ppBB','ppSO','ppBAO','ppERA','ppIBB','ppWP','ppHBP','ppBK','ppBFP','ppGF','ppR','ppSH','ppSF','award']
attributes =  ['bG','bAB','bR','bH','b2B','b3B','bHR','bRBI','bSB','bCS','bBB','bSO','bIBB','bHBP','bSH','bSF','fPOS','fG','fGS','fIO','fPO','fA','fE','fDP','fWP','fPB','fSB','fCS','fZR','pW','pL','pG','pGS','pCG','pSHO','pSV','pIP','pH','pER','pHR','pBB','pSO','pBAO','pERA','pIBB','pWP','pHBP','pBK','pBFP','pGF','pR','pSH','pSF','award']
root = tree.build_tree(train, attributes, target)

print("Accuracy of test data")
# df_test = clean('horseTest.txt')
print(str(tree.test_predictions(root, test, target)*100.0) + '%')

print("F1 score of test data")
# df_test = clean('horseTest.txt')
print(str(tree.test_f1score(root, test, target)*100.0) + '%')


# ############tree2
# target = 'nom'
# df[target] = y_nom.tolist()
# # df = pd.DataFrame.from_csv('weather.csv')
# train, test = tree.train_test_split(df)
# X = train.iloc[:, :-1]
# y = train.iloc[:, -1]
# tree = tree2.DecisionTreeID3(max_depth = 3, min_samples_split = 2)
# tree.fit(X, y)
# print(tree.predict(X))