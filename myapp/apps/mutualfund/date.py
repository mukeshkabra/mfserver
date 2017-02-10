import time

date = '21-Oct-2016'
pattern = '%d-%b-%Y'
epoch = int(time.mktime(time.strptime(date, pattern)))
print epoch


print epoch-(86400*7)
print epoch-2629743
print time.strftime("%d-%b-%Y", time.localtime(epoch))



