# Cookie Jar

![Red Velvet Cookie Jar](red_velvet_cookie_jar.jpeg "Red Velvet looking for them cookies")
_Let's see what cookies we have got here..._

A CyberSec tool to help capture cookies from HTTP requests

## When to use
In situations where you need to capture cookies from either an server-side HTTP request (SSRF) or from a client-side HTTP request (SSTI/CSRF).   

For client-side use cases, tampering with the cookies would be needed to bypass the browser's in-built security, such as tampering with cookies or DNS bindings on subdomains. The app is also CORS-enabled which would allow for cross-origin calls.   

The use-case for client-side attacks are admittedly limited.   

## How to use 
Simply inject the URL of the deployed app into the vulnearable app to let it make calls to this app. 

## API docs
---

## `GET` - `/cookies`

### Parameters
No parameters. 

### Content
`application/json`

### Response

`200` - All cookies retrieved
```
{
    "code": 200, 
    "data": [
        {
            "key": "foo1", 
            "value": "bar1", 
            "timestamp": "Monday, 01 January 2021, UTC 00:00:01"
        }, 
        {
            "key": "foo1", 
            "value": "bar1", 
            "timestamp": "Monday, 01 January 2021, UTC 00:00:01"
        }
    ]
}
```

`500` - Failure to retrieve cookies
```
{
    "code": 500, 
    "message": "Failed to retrieve cookies. "
}
```

## `DELETE` - `/cookies`

### Parameters
No parameters. 

### Content
`application/json`

### Response

`200` - All cookies deleted
```
{
    "code": 200, 
    "message": "All cookies' details have been deleted. "
}
```

`500` - Failure to delete cookies
```
{
    "code": 500, 
    "message": "Failed to delete cookies. "
}
```

## `GET` - `/cookies/<key>`

### Parameters
key (`str`)   
_Stated in the URI_   
The query string to find the cookie wanted by matching for its key

### Content
`application/json`

### Response

`200` - Matching cookies retrieved
```
{
    "code": 200, 
    "data": [
        {
            "key": "foo1", 
            "value": "bar1", 
            "timestamp": "Monday, 01 January 2021, UTC 00:00:01"
        }, 
        {
            "key": "foo1", 
            "value": "bar1", 
            "timestamp": "Monday, 01 January 2021, UTC 00:00:01"
        }
    ]
}
```

`500` - Failure to retrieve matching cookies
```
{
    "code": 500, 
    "message": "Failed to retrieve cookies. "
}
```

---
## Attribution
[Cookies icons created by Smashicons - Flaticon](https://www.flaticon.com/free-icons/cookies "cookies icon")

[Image from '#cookie jar' by Red Velvet under SM Entertainment, SM Entertainment's Associates and Affiliates](https://redvelvet-jp.net/) - Reference for them Reveluvs