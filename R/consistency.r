setwd("/home/s/Dokumente/R&D/IoTTrace/data/")
data <- read.csv("taxi-medium-big.csv")
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

x_start = 121.38
x_end = 121.57
y_start = 31.15
y_end = 31.32

library(ggmap)
#take a sample of 100.000 data entries
mapdata <- data[sample(nrow(data),100000),]
map <- get_map(location = "Shanghai", zoom = 11)
ggmap(map) +
  geom_point(data = mapdata, aes(x = longitude, y = latitude, fill="red", alpha=0.1), size = 0.1, shape = 21) +
  geom_segment(aes(x=x_start, y=y_start, xend = x_end, yend = y_start),  color = "blue") +
  geom_segment(aes(x=x_start, y=y_end, xend = x_end, yend = y_end), colour ="blue") +
  geom_segment(aes(x=x_start, y=y_start, xend = x_start, yend = y_end), colour ="blue") +
  geom_segment(aes(x=x_end, y=y_start, xend = x_end, yend = y_end), colour ="blue")
#speed values before cutting off certain coordinates
summary(data$speed)

# speed filtering
boxplot(data$speed)
plot(density(data$speed), xlab="Speed", ylab="Density", main="")
summary(data$speed)
#upper whisker
upq <- quantile(data$speed, 0.75)
# limit is 3x the interquartile range
# limit <- upq + 3*(upq-quantile(data$speed, 0.25))
# limit <- 100
# data <- subset(data, speed < limit)
summary(data$speed)
dropped <- datacount - nrow(data)
#number of dropped observations
dropped
summary(data$speed)

#density of speed before the coordinate cut-off
plot(density(data$speed), xlab="Speed", ylab="Density", main="Speed density")
dataw0 <- subset(data, speed>0)
hist(dataw0$speed, xlab="Speed", ylab="Density", main="Adapted speed distribution before coordinate cut-off")
mean_before <- mean(dataw0$speed)
median_before <- median(data$speed)
u80_before <- nrow(subset(data, speed>=80))
plot(density(dataw0$speed), xlab="Speed", ylab="Density", main="Adapted speed density before coordinate cut-off") +
   abline(v=mean_before)

# coordinate filtering
plot(data$longitude, data$latitude, main="unfiltered Map", xlab="Longitude", ylab="Latitude")
datastat <- subset(data, longitude>=x_start)
data <- subset(data, longitude>=x_start)
datastat <- subset(data, longitude<=x_end)
data <- subset(data, longitude<=x_end)
datastat <- subset(data, latitude>=y_start)
data <- subset(data, latitude>=y_start)
datastat <- subset(data, latitude<=y_end)
data <- subset(data, latitude<=y_end)
plot(data$longitude, data$latitude, main="filtered Map", xlab="Longitude", ylab="Latitude", pch=".")
dropped <- datacount - nrow(data)
#number of dropped observations
dropped
datastat <- subset(data, speed > median_before)
nrow(datastat)/datacount
summary(data$speed)

#density of speed after the coordinate cut-off
dataw0_2 <- subset(data, speed > 0)
hist(dataw0_2$speed, xlab="Speed", ylab="Density", main="Adapted speed distribution after coordinate cut-off")
mean_after <- mean(dataw0_2$speed)
median_after <- median(data$speed)
u80_after <- nrow(subset(data, speed>=80))
plot(density(dataw0_2$speed), xlab="Speed", ylab="Density", main="Adapted speed density after coordinate cut-off") +
  abline(v=mean_after)

hist(data$status, xlab="status", ylab="frequency", main="Taxi status", xlim = c(-0.5,3.5), breaks=c(-0.5,0.5,1.5,2.5,3.5))
hist(data$extendedstatus, xlab="extended status", ylab="frequency", main="Extended taxi status", xlim = c(-0.5,3.5), breaks=c(-0.5,0.5,1.5,2.5,3.5))

summary(data$angle)

write.csv(data, file = "taxi_filtered.csv")