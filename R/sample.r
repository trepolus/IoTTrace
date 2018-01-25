setwd("/home/s/Dokumente/R&D/IoTTrace/data/")
data <- read.csv("taxi-medium-bigbig.csv")
names(data) <- c("id","taxiid","longitude","latitude","speed","angle","datetime","status","extendedstatus","reversed")
nrow(data)

data_sample <- data[sample(nrow(data),7000),]

write.table(data_sample, file="taxi_heatmap.csv", row.names=FALSE, col.names=FALSE, sep=",", quote=FALSE)
summary(data_sample$status)