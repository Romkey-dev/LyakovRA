# Задание 2.
# Распараллельте фрагмент кода, представленный ниже, используя вычислительный
# кластер:
# for(iter in seq_len(50))
#  result[iter] <- mean_of_rnorm(10000)
# Для решения подгрузите функцию
# mean_of_rnorm <- function(n) {
#  random_numbers <- rnorm(n)
#  mean(random_numbers)
# }

mean_of_rnorm <- function(n) {
  random_numbers <- rnorm(n)
  mean(random_numbers)
}

ncores <- detectCores(logical = FALSE)

cl <- makeCluster(ncores)

clusterExport(cl, varlist = "mean_of_rnorm")

# Параллельный
system.time({
  result_parallel <- parSapply(cl, seq_len(50), function(x) mean_of_rnorm(10000))
})

#  кластер
stopCluster(cl)

#  результат
summary(result_parallel)

# Последовательный
system.time({
  result_seq <- numeric(50)
  for (iter in seq_len(50))
    result_seq[iter] <- mean_of_rnorm(10000)
})

summary(result_seq)
