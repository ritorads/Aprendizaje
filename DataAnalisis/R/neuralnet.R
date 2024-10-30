library(caTools)
library(neuralnet)
library(NeuralNetTools)
library(corrplot)
library(ggplot2)


dataset <- datasets::mtcars

dataset_scaled <- as.data.frame(cbind(dataset$cyl, scale(dataset[ ,c(1,3:11)])))
e43sw
names(dataset_scaled)[1] = 'cyl'
sample <- sample.split(dataset_scaled$cyl, SplitRatio = 0.3)
train <- subset(dataset_scaled, sample == TRUE)
test <- subset(dataset_scaled, sample == FALSE)

model.net = neuralnet(
  formula = cyl ~ .,
  data = train,
  hidden = c(5,2,2),
  stepmax = 1e+05,
  linear.output = TRUE,
  act.fct = 'logistic'
  
)

#correlaciones
cor_matx <- cor(test)
corrplot(cor_matx, method = "circle")
pairs(cor_matx)

#El modelo
data_pred = compute(model.net, test)

data_pred = data_pred$net.result

test_df = as.data.frame(cbind(round(data_pred), test$cyl))

olden(model.net)
plotnet(model.net)

