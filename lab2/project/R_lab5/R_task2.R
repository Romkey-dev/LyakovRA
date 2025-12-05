# Задание 2. Используя документацию пакета purrr опишите отличия и особенности
# функций семейства map_*. Приведите примеры реализации с использование различных
# тестовых данных. Данные можно брать из пакета datasets или создав свои тестовые наборы.
# Для просмотра данных из пакета datasets выполните код library(help = "datasets")


library(purrr)

nums <- list(1:3, 4:6, 7:9)
txt <- list("a", "bb", "ccc")
logi <- list(c(TRUE, FALSE), c(FALSE, TRUE))

map(nums, ~ .x * 2)
map_chr(txt, toupper)
map_dbl(nums, mean)
map_int(nums, length)
map_lgl(nums, ~ any(.x > 5))
map2(1:3, 4:6, ~ .x + .y)
pmap(list(a=1:3, b=4:6), ~ ..1 + ..2)
map_if(nums, ~ length(.x) > 2, sum)
map_at(nums, c(1,3), ~ .x * 10)
modify(nums, ~ .x + 1)
walk(nums, print)
deep <- list(list(1:2), list(3:4))
map_depth(deep, 2, sum)
map_vec(nums, mean)
imap(nums, ~ paste(.y, ":", .x[1]))
