

def best_threshold(test_y,yhat):
    from sklearn.metrics import roc_curve
    from numpy import sqrt, argmax
    # calculate roc curves
    fpr, tpr, thresholds = roc_curve(test_y, yhat)
    # calculate the g-mean for each threshold
    gmeans = sqrt(tpr * (1-fpr))
    # locate the index of the largest g-mean
    ix = argmax(gmeans)
    return(thresholds[ix], gmeans[ix])
        

def best_threshold_YoudenJstatistic(test_y,yhat):
    from sklearn.metrics import roc_curve
    from numpy import argmax
    fpr, tpr, thresholds = roc_curve(test_y, yhat)
    # get the best threshold
    J = tpr - fpr
    ix = argmax(J)
    best_thresh = thresholds[ix]
    return(best_thresh)

