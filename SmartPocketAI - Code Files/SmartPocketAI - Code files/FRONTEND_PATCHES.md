# Required async call-site patches

The backend replacements use `fetch()`, so the existing synchronous page handlers must become async.

## register.html
- Change the submit listener to `async (e) =>`.
- Change `const result = PS.register(...)` to `const result = await PS.register(...)`.

## login.html
- Change `function doLogin(...)` to `async function doLogin(...)`.
- Change `const result = PS.login(...)` to `const result = await PS.login(...)`.
- In both event listeners, call `await doLogin(...)` from an `async` callback.

## home-planner.html / party-planner.html / jewelry-planner.html
- Change each submit listener to `async (e) =>`.
- Change `const result = PSRecommend.generate...` to `const result = await PSRecommend.generate...`.
- Change `PS.saveHistory(...)` to `await PS.saveHistory(...)`.
- Wrap recommendation/save calls in try/catch and show `PS.toast(error.message, "error")`.

## dashboard.html
- Put the page's history/session rendering code in an async function.
- Use `const si = await PS.getSessionInfo()` and `const history = await PS.getHistory()`.

## history.html
- Put initial loading in an async function and use `let history = await PS.getHistory()`.
- Make `removeItem` async, await `PS.deleteHistory(id)`, then await `PS.getHistory()`.
- Make the Clear All callback async, await `PS.clearAllHistory()`, then await `PS.getHistory()`.
- IDs are numeric now. In `viewDetail`, `reuseItem`, and `removeItem`, compare with `String(x.id) === String(id)`.
