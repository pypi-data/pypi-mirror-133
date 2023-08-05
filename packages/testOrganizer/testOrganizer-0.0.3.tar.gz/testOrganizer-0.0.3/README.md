How to use it:


from testOrganize.TestDecorator import test, beforeEachTest, afterEachTest, print_result

@beforeEachTest()
def be():
print("before each test")

@afterEachTest()
def ae():
print("after each test")


@test("First test", should_execute=False, info="Bug found")
def test1():
print("test")

@test("Second test")
def test2():
print("test")

print_result()


Important notes:
-beforeEachTest and afterEachTest must be defined first
-at the end of file print_result() must be called so that result is printed to console
-for sharing variables over functions, python rules are applied


