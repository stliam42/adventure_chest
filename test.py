numbers = [1,2,3,4,5,6,7,8]

def power(numbers_list: list, index: int) -> set:
    x = (numbers_list[index], numbers_list[index]**2)
    return x

print(power(numbers, 5))