from scipy.stats import binom_test
from scipy.stats import binom

def binom_test_v2(x, n=None, p=0.5, alternative='two-sided'):
    n = np.int_(n)
    if (p > 1.0) or (p < 0.0):
        raise ValueError("p must be in range [0,1]")

    if alternative not in ('two-sided', 'less', 'greater'):
        raise ValueError("alternative not recognized should be 'two-sided', 'less' or 'greater'")
    if alternative == 'less':
        pval = binom.cdf(x, n, p)
        return pval
    if alternative == 'greater':
        pval = binom.sf(x-1, n, p)
        return pval
    d = binom.pmf(x, n, p)
    rerr = 1 + 1e-7
    a_fn = lambda x1:binom.pmf(x1,n,p)
    if x == p * n:
        pval = 1.
    elif x < p * n:
        y = n-binary_search(a_fn,d*rerr,np.ceil(p * n),n)+1
        pval = (binom.cdf(x, n, p) +
                binom.sf(n - y, n, p))
    else:
        y = binary_search(a_fn,d*rerr,0,np.floor(p*n) + 1,True)+1
        pval = (binom.cdf(y-1, n, p) +
                binom.sf(x-1, n, p))
    return min(1.0, pval)

  
def binary_search(a, d, lo, hi, asc_order=False):
    while lo < hi:
        mid = (lo+hi)//2
        midval = a(mid)
        if midval < d:
            if asc_order:
                lo = mid+1
            else:
                hi = mid-1
        elif midval > d:
            if asc_order:
                hi = mid-1
            else:
                lo = mid+1
        else:
            return mid
    if a(lo)<=d:
        return lo
    else:
        return lo-(asc_order-0.5)*2

result=df
result["p_value"] = result.apply(lambda row : binom_test(row.Events_B,row.Events_A + row.Events_B,row.Days_A/(row.Days_A +row.Days_B),alternative='greater'), axis=1)
result["p_value_two_sided"] = result.apply(lambda row : binom_test_v2(row.Events_B,row.Events_A + row.Events_B,row.Days_B/(row.Days_A +row.Days_B),alternative='two-sided'), axis=1 )
