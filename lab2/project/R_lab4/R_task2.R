# Задание 2. Напишите функцию get_negative_values, которая получает на вход dataframe
# произвольного размера. Функция должна для каждой переменной в данных проверять, есть ли
# в ней отрицательные значения. Если в переменной отрицательных значений нет, то эта
# переменная нас не интересует, для всех переменных, в которых есть отрицательные значения
# мы сохраним их в виде списка или матрицы, если число элементов будет одинаковым в каждой
# переменной (смотри пример работы функции).

get_negative_values <- function(x) {
  neg_list <- list()
  
  for(col_name in names(x)) {
    col_data <- x[[col_name]]
    neg_vals <- col_data[col_data < 0 & !is.na(col_data)]
    
    if(length(neg_vals) > 0) {
      neg_list[[col_name]] <- neg_vals
    }
  }
  
  lengths <- sapply(neg_list, length)
  if(length(unique(lengths)) == 1 & length(neg_list) > 0) {
    max_len <- max(lengths)
    result <- matrix(NA, nrow = max_len, ncol = length(neg_list))
    colnames(result) <- names(neg_list)
    
    for(i in seq_along(neg_list)) {
      result[1:length(neg_list[[i]]), i] <- neg_list[[i]]
    }
    return(result)
  }
  
  return(neg_list)
}

test_data <- as.data.frame(list(V1 = c(NA, -0.5, -0.7, -8), V2 = c(-0.3, NA, -2, -1.2),
V3 = c(1, 2, 3, NA)))
print(get_negative_values(test_data))
test_data <- as.data.frame(list(V1 = c(-9.7, -10, -10.5, -7.8, -8.9), V2 = c(NA, -10.2,
-10.1, -9.3, -12.2), V3 = c(NA, NA, -9.3, -10.9, -9.8)))
print(get_negative_values(test_data))
