import pymysql
import shared
import tree
import pandas as pd
import numpy as np


class AllTables:
    def __init__(self):
        self.sql = "select * from treesource limit 1000"
        self.cols = ['playerID','bG','bAB','bR','bH','b2B','b3B','bHR','bRBI','bSB','bCS','bBB','bSO','bIBB','bHBP','bSH','bSF','fPOS','fG','fGS','fIO','fPO','fA','fE','fDP','fWP','fPB','fSB','fCS','fZR','pW','pL','pG','pGS','pCG','pSHO','pSV','pIP','pH','pER','pHR','pBB','pSO','pBAO','pERA','pIBB','pWP','pHBP','pBK','pBFP','pGF','pR','pSH','pSF','award','nom','hof','man']
class BattingTables:
    def __init__(self):
        self.sql = "select * from battingtree limit 1000"
        self.cols = ['playerID','bG','bAB','bR','bH','b2B','b3B','bHR','bRBI','bSB','bCS','bBB','bSO','bIBB','bHBP','bSH','bSF','award','nom','hof','man']
class FieldingTables:
    def __init__(self):
        self.sql = "select * from fieldingtree limit 1000"
        self.cols = ['playerID','fPOS','fG','fGS','fIO','fPO','fA','fE','fDP','fWP','fPB','fSB','fCS','fZR','award','nom','hof','man']
class PitchingTables:
    def __init__(self):
        self.sql = "select * from pitchingtree limit 1000"
        self.cols = ['playerID','pW','pL','pG','pGS','pCG','pSHO','pSV','pIP','pH','pER','pHR','pBB','pSO','pBAO','pERA','pIBB','pWP','pHBP','pBK','pBFP','pGF','pR','pSH','pSF','award','nom','hof','man']


def removezero(df):
    for column in df:
        #print("Column %s max is %s" % (column,df[column].max()))
        if df[column].max() == 0:
            df.drop(columns=[column], inplace = True)
        # elif column == "pBK" or column == "award":
        #     df.drop(columns=[column], inplace = True)
    return df

# Open database connection

def databaseconnection(sql):
    host = shared.host
    user = shared.user
    password = shared.password
    database = shared.database

    db = pymysql.connect(host,user,password,database)
    print("connecting to db..")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
    except:
        print ("Error: unable to fetch data")
        db.close()
        return None

    # disconnect from server
    db.close()
    print("disconnecting to db..")
    return results

def AnalyzeMining(target, tables):

    if tables == "All":
        tables = AllTables()
    elif tables == "Batting":
        tables = BattingTables()
    elif tables == "Fielding":
        tables = FieldingTables()
    elif tables == "Pitching":
        tables = PitchingTables()
    # else:
    #     raise

    sql = tables.sql
    dfcols = tables.cols

    results = databaseconnection(sql)
    print("get result from db..")

    df = pd.DataFrame(list(results))

    df.columns = dfcols
    df.fillna(value=0, inplace=True)
    df = removezero(df)
    y = df[target].values.astype(int)
    # y_hof = df['hof'].values.astype(int)
    # y_man = df['man'].values.astype(int)
    df.drop(columns=['playerID','nom','hof','man'], inplace=True)

    cols = list(df.columns.values)
    df = df[cols].applymap(np.int64)
    df = df[cols].round(decimals=-1)
    #print(df)

    ########tree algorithm

    #nom_data = df
    df[target] = y.tolist()
    train, test = tree.train_test_split(df)

    ##
    attributes = cols
    print("Generating decision tree..")
    root = tree.build_tree(train, attributes, target)

    print("Accuracy of test data")
    # df_test = clean('horseTest.txt')
    acc = str(tree.test_predictions(root, test, target)*100.0) + '%'
    print(acc)

    print("F1 score of test data")
    # df_test = clean('horseTest.txt')
    f1_score = str(tree.test_f1score(root, test, target)*100.0) + '%'
    print(f1_score)

    return acc, f1_score

def ValidationMining(target, fn, ln):

    print("target: %s, fn: %s, ln: %s" % (target,fn,ln))
    # get real value for input
    r_sql = "select * from validtree where nameFirst = \'" + fn + "\' and nameLast = \'" + ln + "\' limit 1;"

    realdata = databaseconnection(r_sql)
    if realdata == None or len(realdata) == 0:
        print("No record exists for %s %s" % (fn,ln))
        pred = "No result"
        real = "No record exists for " + fn +" " +ln
        #exit()
        return pred, real
    else:
        r_df = pd.DataFrame(list(realdata))
        r_df.columns = ['playerID','nameFirst','nameLast','nom','hof','man']
        r_df.fillna(value=0, inplace=True)
        real = r_df[target].iloc[0]
        real = "Y" if int(real) == 1 else "N"
        print("real value is ", real)

    # get corresponding row
    playerid = r_df['playerID'].iloc[0]

    tables = AllTables()
    dfcols = tables.cols

    row_sql = "select * from treesource where playerID = \'" + playerid + "\'"
    rowdata = databaseconnection(row_sql)
    rowdf = pd.DataFrame(list(rowdata))

    rowdf.columns = dfcols
    rowdf.fillna(value=0, inplace=True)

    #######decision tree data
    sql = tables.sql

    results = databaseconnection(sql)
    print("get result from db..")
    df = pd.DataFrame(list(results))

    df.columns = dfcols
    df.fillna(value=0, inplace=True)
    df = removezero(df)
    y = df[target].values.astype(int)
    df.drop(columns=['playerID','nom','hof','man'], inplace=True)

    cols = list(df.columns.values)
    df = df[cols].applymap(np.int64)
    df = df[cols].round(decimals=-1)

    rowdf = rowdf[cols].applymap(np.int64)
    rowdf = rowdf[cols].round(decimals=-1)
    row = rowdf.iloc[0]

    df[target] = y.tolist()
    train, test = tree.train_test_split(df)

    ##
    attributes = cols
    print("Generating decision tree..")
    root = tree.build_tree(train, attributes, target)

    print("Start to predict..")
    pred = str(tree.predict(root, row))
    pred = "Y" if int(pred) == 1 else "N"

    return pred, real
