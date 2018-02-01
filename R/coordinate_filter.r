start_lon <- 121.38
end_lon <- 121.57
start_lat <- 31.15
end_lat <- 31.32

setwd("/home/s/Dokumente/R&D/IoTTrace/data/")
data <- read.csv("taxi-medium-small.csv")
names(data) <- c("id","taxiid","longitude","latitude","speed","angle","datetime","status","extendedstatus","reversed")
data <- subset(data, latitude > start_lat)
data <- subset(data, latitude < end_lat)
data <- subset(data, longitude > start_lon)
data <- subset(data, latitude < end_lon)

write.table(data_sample, file="taxi_filtered_by_coordinates.csv", row.names=FALSE, col.names=FALSE, sep=",", quote=FALSE)