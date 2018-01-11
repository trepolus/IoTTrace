setwd("/home/s/Dokumente/R&D/IoTTrace/python/")
data <- read.csv("distances.csv")
dataorig <- data
datacount <- nrow(data)
#number of read observations
datacount

data$timeToNextTrip <- abs(data$timeToNextTrip)
data$timeToNextTrip <- data$timeToNextTrip / 60
data <- subset(data, data$timeToNextTrip > 0)
data <- subset(data, data$timeToNextTrip < 100)
data <- subset(data, data$distance > 0)
mean <- mean(data$timeToNextTrip)
hist(data$timeToNextTrip, xlab = "Time to the next trip in minutes", ylab = "Frequency", main = "Time gap distribution")
plot(density(data$timeToNextTrip), xlab="time to the next trip", ylab="Density", main="Time gap density") +
  abline(v = mean)
