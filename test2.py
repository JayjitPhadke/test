from scipy.stats import t
def t_test(mu1,mu2,std1,std2,n1,n2,variance=1,dist=t,alternative='two-sided'):
    if (std1 == std2 == 0 and (n1 > 30 and n2 > 30) and (mu1 != mu2)):
        return 0,0
    if (n1 == 0 or n2 == 0 or (std1 == 0 and n1 < 20) or (std2 == 0 and n2 < 20) or (std1 == 0 and std2 == 0)):
        return 1,1
    std_dev = (std1**2/(n1-1)+std2**2/(n2-1))**0.5
    test_stat = (mu2-mu1)/std_dev
    df = n1+n2-2
    if test_stat>0:
        p_val = 2*dist.sf(test_stat,df)
        p_val_adj = 2*dist.sf(dist.isf(p_val/2,df,0,1), df,0,variance)
    else:
        p_val = 2*dist.cdf(test_stat,df)
        p_val_adj = 2*dist.cdf(dist.ppf(p_val/2,df,0,1), df,0,variance)
    return p_val, p_val_adj
        
result=df
result[[\"p_value_two_sided_old\",\"p_value_two_sided\"]] = result.apply(lambda row : pd.Series(t_test(row.GroupA_mean, row.GroupB_mean, row.GroupA_StdDev, row.GroupB_StdDev, row.GroupA_Count, row.GroupB_Count,row.ConfidenceScoreScaleFactore)), axis=1)
result[\"p_value\"] = result.apply(lambda row : row.p_value_two_sided/2 if(row.GroupB_mean > row.GroupA_mean) else 1-(row.p_value_two_sided/2), axis=1)
result[\"p_value\"] = result.apply(lambda row : (1- row.p_value) if (row.HigherValueIsBetter == 1) else (row.p_value), axis=1)
result[\"Confidence\"] = result.apply(lambda row : (1-row.p_value), axis=1)
result[\"Confidence_two_sided\"] = result.apply(lambda row : (1-row.p_value_two_sided), axis=1)
