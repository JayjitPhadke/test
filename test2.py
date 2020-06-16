from scipy.stats import t

def t_test(mu1,mu2,std1,std2,n1,n2,dist=t,alternative='two-sided'):
    std_dev = (std1**2/(n1-1)+std2**2/(n2-1))**0.5
    test_stat = (mu2-mu1)/std_dev
    df = n1+n2-2
    if test_stat>0:
        p_val = 2*dist.sf(test_stat,df)
    else:
        p_val = 2*dist.cdf(test_stat,df)
    
    if (alternative == 'greater' and mu2>mu1) or\
        (alternative == 'less' and mu2<mu1):
        return p_val/2
    elif (alternative == 'greater' and mu2<mu1) or\
        (alternative == 'less' and mu2>mu1):
        return 1-p_val/2
    else:
        return p_val
        
result=df
result["p_value_two_sided"] = result.apply(lambda row : t_test(row.GroupA_mean, row.GroupB_mean, row.GroupA_StdDev, row.GroupB_StdDev, row.GroupA_Count, row.GroupB_Count), axis=1)
result["p_value"] = result.apply(lambda row : row.p_value_two_sided/2 if(row.GroupB_mean > row.GroupA_mean) else 1-(row.p_value_two_sided/2), axis=1)
result["p_value"] = result.apply(lambda row : (1- row.p_value) if (row.HigherValueIsBetter == 1) else (row.p_value), axis=1)
result["Confidence"] = result.apply(lambda row : (1-row.p_value)**.33, axis=1)
result["Confidence_two_sidex"] = result.apply(lambda row : (1-row.p_value_two_sided)**.33, axis=1)
