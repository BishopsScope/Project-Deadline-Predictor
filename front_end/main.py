import eel

eel.init("web")


@eel.expose
def test(num, name, cate):
    print(cate)
    return num, name, cate


# Start the index.html file
eel.start("index.html",  size=(500, 500), host="localhost", port=0)
