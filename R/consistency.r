library(ggmap)
setwd("/home/s/Dokumente/R&D/IoTTrace/data/")
data <- read.csv("taxi-medium.csv")
names(data) <- c("id","taxiid","longitude","latitude","speed","angle","datetime","status","extendedstatus","reversed")
dataorig <- data
datacount <- nrow(data)
#number of read observations
datacount


#bullshit value filtering
data <- subset(data, speed >= 0 && speed < 300)
data <- subset(data, angle >= 0 && angle < 180)
data <- subset(data, status >= 0 && status <= 3)
data <- subset(data, taxiid >= 0)
data <- subset(data, longitude >= -180 && longitude <= 180)
data <- subset(data, latitude >= -90 && latitude <= 90)
data$datetime <- as.POSIXct(data$datetime)
begin <- as.POSIXct('2006-01-01')
end <- as.POSIXct('2007-12-31')
data <- subset(data, datetime >= begin && datetime <= end)
dropped <- datacount - nrow(data)
dropped


#density of speed before the coordinate cut-off
plot(density(data$speed), xlab="Speed", ylab="Density", main="Speed density")
dataw0 <- subset(data,speed>0)
dataw0 <- subset(dataw0,speed<150)
hist(dataw0$speed, xlab="Speed", ylab="Density", main="Adapted speed distribution without zero values")
plot(density(dataw0$speed), xlab="Speed", ylab="Density", main="")

plot(data$longitude, data$latitude, main="unfiltered Map", xlab="Longitude", ylab="Latitude")
#filter
x_start = 121.38
x_end = 121.57
y_start = 31.15
y_end = 31.32
data <- subset(data,longitude>x_start && longitude<x_end)
data <- subset(data,latitude>y_start && latitude<y_end)
plot(data$longitude, data$latitude, main="filtered Map", xlab="Longitude", ylab="Latitude", pch=".")
dropped <- datacount - nrow(data)
#number of dropped observations
dropped

#speed
boxplot(data$speed)
plot(density(data$speed), xlab="Speed", ylab="Density", main="")
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

map <- get_map(location = "Shanghai", zoom = 12)
ggmap(map) +
  geom_point(data = data, aes(x = longitude, y = latitude, fill="black", alpha=0.1), size = 0.3, shape = 21) +
  geom_segment(aes(x=x_start, y=y_start, xend = x_end, yend = y_start)) +
  geom_segment(aes(x=x_start, y=y_end, xend = x_end, yend = y_end)) +
  geom_segment(aes(x=x_start, y=y_start, xend = x_start, yend = y_end)) +
  geom_segment(aes(x=x_end, y=y_start, xend = x_end, yend = y_end))

hist(data$status, xlab="status", ylab="frequency", main="Taxi status", xlim = c(-0.5,3.5), breaks=c(-0.5,0.5,1.5,2.5,3.5))
hist(data$extendedstatus, xlab="extended status", ylab="frequency", main="Extended taxi status", xlim = c(-0.5,3.5), breaks=c(-0.5,0.5,1.5,2.5,3.5))

summary(data$angle)

write.csv(data, file = "taxi_filtered.csv")