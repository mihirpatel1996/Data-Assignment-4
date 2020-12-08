timestamp = read.csv("D:\\Dalhousie\\Sem-3\\Database Management and Warehousing\\Assignments\\Assignment-4\\timestamp.csv")

View(timestamp)
result=kmeans(timestamp,8)
print(result)
timestamp$cluster <- as.character(result$cluster)
head(timestamp)

ggplot() + geom_point(data = timestamp, mapping = aes(x = created_at, y = created_at, colour = cluster))+
geom_point(mapping = aes_string(x = result$centers, 
                                y = result$centers),
           color = "red", size = 4)
