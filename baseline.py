from util import *
import csv
import random


def loss(p, y):
    return max(0, 1 - p * y)


def dloss_scale(p, y):
    return 0 if loss(p, y) == 0 else -y


def sign(n):
    if n < 0:
        return -1
    elif n > 0:
        return 1
    else:
        return 0


def predict(features, w):
    return sign(dotProduct(w, features))


def learnPredictor(trainExamples, testExamples, featureExtractor, numIters, eta, normalize=False):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, the step size |eta|, return the weight vector (sparse
    feature vector) learned.
    '''
    weights = {}  # feature => weight
    trainFeatures = [featureExtractor(example) for example in trainExamples]
    def predictor(x):
        return predict(featureExtractor(x), weights)
    for t in range(numIters):
        for i in range(len(trainExamples)):
            p = predict(trainFeatures[i], weights)
            y = trainExamples[i][2]
            gradient_scale = dloss_scale(p, y)
            increment(weights, -gradient_scale * eta, trainFeatures[i])
        if t == numIters - 1:
            print('Training:')
            trainError, trainErrorN, trainErrorP = evaluatePredictor(trainExamples, predictor, printmetrics=True,\
                title='Baseline Train Confusion Matrix', matrixfilename='confusion_matrices/baseline_train_matrix.pdf', normalize=normalize)
            print('Testing:')
            testError, testErrorN, testErrorP = evaluatePredictor(testExamples, predictor, printmetrics=True,\
                title='Baseline Test Confusion Matrix', matrixfilename='confusion_matrices/baseline_test_matrix.pdf', normalize=normalize)
        #print("iteration {}, train error: {}, test error: {}, train error (-): {}, test error (-): {}, train error (+): {}, test error (+): {}".format(t,
        #    trainError, testError, trainErrorN, testErrorN, trainErrorP,
        #    testErrorP))
    return weights


def extractFeatures(row):
    smiles, protein, potent = row
    result = {}
    for n in [1, 2, 3]:
        charFeatures = extractCharacterFeatures(n)(smiles)
        for key in charFeatures:
            result[(protein, key)] = charFeatures[key]
    return result


def extractCharacterFeatures(n):
    '''
    Return a function that takes a string |x| and returns a sparse feature
    vector consisting of all n-grams of |x| without spaces mapped to their n-gram counts.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    '''
    def extract(x):
        result = {}
        spaceless = x.replace(' ', '')
        for i in range(len(spaceless) - n + 1):
            key = spaceless[i:i+n]
            result[key] = result.get(key, 0) + 1
        return result
    return extract


def readDataset():
    result = []
    with open('data.txt', 'r') as csvfile:
        ind = 0
        for line in csvfile:
            row = line.split('\t')
            if ind != 0:
                result.append((
                    row[2],
                    row[3],
                    -1 if int(row[7]) == 0 else 1
                ))
            else:
                ind = 1
    return result


def main(normalize=False):
    dataset = readDataset()
    random.shuffle(dataset)

    splitInd = int(len(dataset) * .8)
    trainExamples = dataset[:splitInd]
    testExamples = dataset[splitInd:]

    weights = learnPredictor(trainExamples, testExamples, extractFeatures,
            numIters=50, eta=0.01, normalize=normalize)

if __name__ == '__main__':
    main()
