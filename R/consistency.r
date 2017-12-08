library(ggmap)
setwd("/home/s/Dokumente/R&D/IoTTrace/data/")
data <- read.csv("taxi-big.csv")
names(data) <- c("id","taxiid","longitude","latitude","speed","angle","datetime","status","extendedstatus","reversed")
dataorig <- data
datacount <- nrow(data)
#number of read observations
datacount


plot(data$longitude, data$latitude, main="unfiltered Map", xlab="Longitude", ylab="Latitude")
#filter
data <- subset(data,longitude>121.38)
data <- subset(data,longitude<121.57)
data <- subset(data,latitude<31.32)
data <- subset(data,latitude>31.17)
plot(data$longitude, data$latitude, main="filtered Map", xlab="Longitude", ylab="Latitude", pch=".")
dropped <- datacount - nrow(data)
#number of dropped observations
dropped

#speed
boxplot(data$speed)
summary(data$speed)
#upper whisker
upq <- quantile(data$speed, 0.75)
# limit is 3x the interquartile range
limit <- upq + 3*(upq-quantile(data$speed, 0.25))
# limit <- 100
data <- subset(data, speed < limit)
summary(data$speed)
dropped <- datacount - nrow(data)
#number of dropped observations
dropped

map <- get_map(location = "Shanghai", zoom = 10)
ggmap(map)
ggmap(map) +
  geom_point(data = data, aes(x = longitude, y = latitude, fill="black", alpha=0.2), size = 1, shape = 21)

hist(data$status, xlab="status", ylab="frequency", main="Taxi status", xlim = c(-0.5,3.5), breaks=c(-0.5,0.5,1.5,2.5,3.5))

write.csv(data, file = "taxi_filtered.csv")