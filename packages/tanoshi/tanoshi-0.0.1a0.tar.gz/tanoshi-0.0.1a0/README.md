<h1 align="center">
<sub>
    <img src="https://i.imgur.com/O8dSQLD.png" height="36">
</sub>
&nbsp;
Tanoshi
</h1>
<p align="center">
<sup>
A fast, asyncio based web-framework, that you'll enjoy using.
</sup>
<br>
<sup>
    <a href="">Read the docs.</a>
</sup>
</p>

## Why Tanoshi and what is it?

Tanoshi is a fast, asyncio based web-framework, that you'll really enjoy using. Tanoshi is built to revolve around your design decisions, not ours. Tanoshi has no boiler-plate code what so ever, allowing you to have an extremely flexible code base structure. Tanoshi can also be a heavy-weight framework if you choose to opt-in to it's heavy-weight features, such as a database ORM, as well as adaptable authentication. Tanoshi allows you to quickly prototype, as well as expand and scale quickly!

It's in the name! - *Tanoshi* (楽しい) - Enjoyable

## Key Features

- Modern `async` and `await` syntax.
- Seriously impressive performance thanks to Starlette.
- Opt-in heavy-weight features such as a fully-fledged database ORM.
- Extremely flexible.
- Jinja Templating Support.
- Session and Cookie Middleware.
- Quick and easy to get started with.

## Examples

```py
from tanoshi import Tanoshi
from tanoshi.shortcuts import render, redirect


app = Tanoshi(
    name="MyTanoshiApplication",
    debug=True,
    templates_directory="templates/"
)

@app.route("/", methods=["GET", "POST"])
async def index(request):
    context = {
        "message": "Hello Tanoshi!",
        "moreData": ["guido", "van", "rossum"]
    }
    return render(request, "index.html", context)

@app.route("/redirect")
async def redirect_route(request):
    return redirect("https://www.python.org/")
```

## Running tanoshi

Running `tanoshi` on a production server is super simple. Let's use the example above to learn how to run tanoshi. First, you'll need to install a production server such as `uvicorn`, which is the one I personally recommend. Simply run `pip instal uvicorn` to install uvicorn. Now, if you placed the example code into a file called `main.py`, you'd need to run `uvicorn main:app` inside the directory where your `main.py` file is housed.

This process is exactly the same as other asgi frameworks, no changes there!