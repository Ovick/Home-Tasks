import enum


class MyEnum(enum.Enum):
    One = 1
    Two = 2
    Three = 3


my_enum = MyEnum.Three

print(my_enum.value)
print(my_enum.name)
