import matplotlib.pyplot as plt
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

def plotConfusionMatrixForRandomSplit(clf, X,y, weight=None):
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    if weight==None:
        clf.fit(X_train, y_train)
    else:
        weights = y_train*(weight-1)+1
        clf.fit(X_train, y_train, weights)

    plt.figure()
    plot_confusion_matrix(clf, X_test, y_test, normalize='true')
    plt.show()
    return clf, X_train, X_test, y_train, y_test

def simpleDataPlot(df, channel_id="0", df_markers=None):
    plt.figure()
    plt.plot(df.index, df[channel_id])
    if df_markers is not None:
        addMarkers(df_markers)
    plt.show()

def wholeDataPlot(df, df_markers=None):
    plt.figure()
    for i in range(0, len(df.columns)):
        ax = plt.subplot(len(df.columns), 1, i+1)
        if i is not len(df.columns)-1:
            plt.setp(ax, xticklabels=[])
        plt.plot(df.index, df["EMG_" + str(i)], linewidth=.1)
        if df_markers is not None:
            addMarkers(df_markers)
    plt.show()


def addMarkers(df_markers):
    for x in df_markers.index:
        plt.axvline(x, c="r")