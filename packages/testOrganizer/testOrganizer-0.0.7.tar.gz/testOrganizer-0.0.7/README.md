How to use it:

```
from testOrganizer.TestDecorator import test, beforeEachTest, afterEachTest, print_result

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
print_html("LoginFeature", r"C:\Users\us\Desktop\htmlLogs\testOrganizer.html")
```

Important notes:
- beforeEachTest and afterEachTest must be defined first
- print_result() should be called so that result is printed to console (at the end of file)
- print_html() should be called to print result to html (at the end of file)
- for sharing variables over functions, python rules are applied
- code outside of given functions will also be executed as in standard python script



For sharing variables over functions example:

```
browser = webdriver.Chrome()

@test("First test")
def test1():
    global browser
    browser.get(url)
```

