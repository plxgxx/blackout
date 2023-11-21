
def decorator(func):
    def wrap(text):
        text += "wow"
        return func(text) 
    return wrap



def test(text):
    print(text)

test("Hi!")

decorator(test)("Hi")

print(test)
print(type(test))
