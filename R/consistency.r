library(ggmap)
setwd("/home/s/Dokumente/R&D/IoTTrace/data/")
data <- read.csv("taxi0228.csv")
dataorig <- data
names(data) <- c("id","taxiid","longitude","latitude","speed","angle","datetime","status","extendedstatus","reversed")
datacount <- nrow(data)
#number of read observations
datacount

#speed
boxplot(data$speed)
summary(data$speed)
#upper whisker
upq <- quantile(data$speed, 0.75)
# limit is 4x the interquartile range
limit <- upq + 4*(upq-quantile(data$speed, 0.25))
limit
data <- subset(data, speed < limit)
summary(data$speed)
dropped <- datacount - nrow(data)
#number of dropped observations
dropped

plot(data$longitude, data$latitude, main="unfiltered Map", xlab="Longitude", ylab="Latitude")
#filter
data <- subset(data,longitude>121.2)
data <- subset(data,latitude<32.0)
data <- subset(data,latitude>31.0)
plot(data$longitude, data$latitude, main="filtered Map", xlab="Longitude", ylab="Latitude", pch=".")
dropped <- datacount - nrow(data)
#number of dropped observations
dropped

map <- get_map(location = "Shanghai", zoom = 10)
ggmap(map)
ggmap(map) +
  geom_point(data = data, aes(x = longitude, y = latitude, fill="black", alpha=0.2), size = 1, shape = 21)

hist(data$status, xlab="status", ylab="frequency", main="Taxi status", xlim = c(-0.5,3.5), breaks=c(-0.5,0.5,1.5,2.5,3.5))

write.csv(data, file = "taxi_filtered.csv")