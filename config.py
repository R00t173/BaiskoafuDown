# Baiskoafu loagin details
username = ""
password = ""

def media_quality(quality='medium'):

    q = ['high', 'low', 'medium']

    if quality == q[0]: return q[0]
    if quality == q[1]: return q[1]
    if quality == q[2]: return q[2]
    return q[2] # < --- default is medium

media_quality() # ['high', 'low', 'medium']
ASK_BEFORE_DOWNLOAD = True	# set 'False' for automatic download
IS_PRIMARY_DEVICE   = True	# set 'True' only if you have premium subscription
