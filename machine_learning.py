from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC


def get_score(predictions, correct_results):
    correct = 0
    for x in range(len(correct_results)):
        if predictions[x] == correct_results[x]:
            correct += 1

    return (float(correct)/float(len(predictions)))*100


def run_knn(xtrain, ytrain, xtest, ytest):
    """
    default settings ==> 45%
    algorithm='ball_tree' ==> 45%
    algorithm='kd_tree' ==> 46%
    n_neighbors=10 ==> 48.81%
    n_neighbors=20 ==> 48.84%
    n_neighbors=50 ==> 47%
    n_neighbors=100 ==> 45%
    weights='distance' ==> 46%
    n_neighbors=10, weights='distance' ==> 49%
    n_neighbors=20, weights='distance' ==> 50.9%
    algorithm='kd_tree', n_neighbors=20, weights='distance' ==> 51%
    """

    knn = KNeighborsClassifier(algorithm='kd_tree', n_neighbors=20, weights='distance')
    knn.fit(xtrain, ytrain)
    predictions = knn.predict(xtest)
    score = get_score(predictions, ytest)
    print 'knn:', score


def run_gnb(xtrain, ytrain, xtest, ytest):
    """
    default settings ==> 12%
    """

    gnb = GaussianNB()
    gnb.fit(xtrain, ytrain)
    predictions = gnb.predict(xtest)
    score = get_score(predictions, ytest)
    print 'gnb:', score


def run_svm(xtrain, ytrain, xtest, ytest):
    """
    default settings ==> 51%
    """

    svm = SVC(decision_function_shape='ovo')
    svm.fit(xtrain, ytrain)
    predictions = svm.predict(xtest)
    score = get_score(predictions, ytest)
    print 'svm:', score


def run_rfc(xtrain, ytrain, xtest, ytest):
    """
    default settings ==> 51%
    n_estimators=20 ==> 50%
    n_estimators=30 ==> 52%
    """

    rfc = RandomForestClassifier(n_estimators=30)
    rfc.fit(xtrain, ytrain)
    predictions = rfc.predict(xtest)
    score = get_score(predictions, ytest)
    print 'rfc:', score
