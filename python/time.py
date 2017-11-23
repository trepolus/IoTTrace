from datetime import datetime, time

oldTime = "2006-02-27 17:34:31"

timeFormat = datetime.strptime(oldTime, "%Y-%m-%d %H:%M:%S")

nanoTime = time.mktime(timeFormat.timetuple())
nanoTime = nanoTime * 1000000000

print(nanoTime)



