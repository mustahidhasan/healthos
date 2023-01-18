import random


def generate_number():
    # 11 degit number "01"+ "random 1 degit beween 5 to 9" + "random 8 degit between 0 to 9"
    first_part = '01'
    second_part = random.randint(5, 9)
    thid_part = []
    for idx in range(0, 8):
        thid_part.append(random.randint(0,9))

    merge_all = first_part + str(second_part)
    for idx in thid_part:
        merge_all += str(idx)
    return merge_all




# if __name__ == "__main__":
#     generate_number()
#     print(generate_number())