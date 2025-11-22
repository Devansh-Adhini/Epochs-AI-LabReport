library(bnlearn)
library(e1071)

course.grades <- read.table("2020_bn_nb_data.txt", header = TRUE)


course.grades[] <- lapply(course.grades, function(x) {
  if (is.character(x)) factor(x) else x
})


if (!"QP" %in% colnames(course.grades)) {
  stop("The 'QP' variable does not exist in the dataset.")
}


course.grades.net <- hc(course.grades)
plot(course.grades.net)
course.grades.net.fit <- bn.fit(course.grades.net, course.grades)


print(nodes(course.grades.net))


input_grades <- data.frame(
  EC100 = factor("DD", levels = levels(course.grades$EC100)),
  IT101 = factor("CC", levels = levels(course.grades$IT101)),
  MA101 = factor("CD", levels = levels(course.grades$MA101))
)


predicted_ph100 <- predict(
  course.grades.net.fit,
  node = "PH100",
  data = input_grades,
  method = "bayes-lw"
)


cat("Predicted grade in PH100:", predicted_ph100, "\n")


set.seed(26)
n_trials <- 20
accuracy_results <- numeric(n_trials)


for (i in 1:n_trials) {
  idx <- sample(1:nrow(course.grades), size = 0.7 * nrow(course.grades))
  train <- course.grades[idx, ]
  test <- course.grades[-idx, ]
  
  nb_classifier <- naiveBayes(QP ~ ., data = train)
  predictions <- predict(nb_classifier, newdata = test)
  accuracy_results[i] <- mean(predictions == test$QP)
}


cat("Mean accuracy of Naive Bayes:", mean(accuracy_results), "\n")


bayes_accuracy_results <- numeric(n_trials)


for (i in 1:n_trials) {
  idx <- sample(1:nrow(course.grades), size = 0.7 * nrow(course.grades))
  train <- course.grades[idx, ]
  test <- course.grades[-idx, ]
  
  bayes_net <- hc(train)
  bayes_net_fit <- bn.fit(bayes_net, train)
  
  predictions_bn <- predict(
    bayes_net_fit,
    node = "QP",
    data = test,
    method = "bayes-lw"
  )
  
  valid <- !is.na(predictions_bn)
  bayes_accuracy_results[i] <- mean(predictions_bn[valid] == test$QP[valid])
}

cat("Mean accuracy of Bayesian Network:", mean(bayes_accuracy_results), "\n")
