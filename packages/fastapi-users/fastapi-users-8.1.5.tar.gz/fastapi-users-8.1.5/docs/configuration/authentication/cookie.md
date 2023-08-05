# Cookie

Cookies are an easy way to store stateful information into the user browser. Thus, it is more useful for browser-based navigation (e.g. a front-end app making API requests) rather than pure API interaction.

## Configuration

```py
from fastapi_users.authentication import CookieAuthentication

SECRET = "SECRET"

cookie_authentication = CookieAuthentication(secret=SECRET, lifetime_seconds=3600)
```

As you can see, instantiation is quite simple. It accepts the following arguments:

* `secret` (`Union[str, pydantic.SecretStr]`): A constant secret which is used to encode the cookie. **Use a strong passphrase and keep it secure.**
* `lifetime_seconds` (`int`): The lifetime of the cookie in seconds.
* `cookie_name` (`fastapiusersauth`): Name of the cookie.
* `cookie_path` (`/`): Cookie path.
* `cookie_domain` (`None`): Cookie domain.
* `cookie_secure` (`True`): Whether to only send the cookie to the server via SSL request.
* `cookie_httponly` (`True`): Whether to prevent access to the cookie via JavaScript.
* `cookie_samesite` (`lax`): A string that specifies the samesite strategy for the cookie. Valid values are `lax`, `strict` and `none`. Defaults to `lax`.
* `name` (`Optional[str]`): Name of the backend. It's useful in the case you wish to have several backends of the same class. Each backend should have a unique name. Defaults to `cookie`.

```py
cookie_authentication = CookieAuthentication(
    secret=SECRET,
    lifetime_seconds=3600,
    name="my-cookie",
)
```

!!! tip
    The value of the cookie is actually a JWT. This authentication backend shares most of its logic with the [JWT](./jwt.md) one.

## Login

This method will return a response with a valid `set-cookie` header upon successful login:

!!! success "`200 OK`"

> Check documentation about [login route](../../usage/routes.md#post-loginname).

## Logout

This method will remove the authentication cookie:

!!! success "`200 OK`"

> Check documentation about [logout route](../../usage/routes.md#post-logoutname).

## Authentication

This method expects that you provide a valid cookie in the headers.
