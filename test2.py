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
result["p_value"] = result.apply(lambda row : t_test(row.Events_B,row.Events_A + row.Events_B,row.Uptime_B/(row.Uptime_A +row.Uptime_B),alternative='greater'), axis=1)
