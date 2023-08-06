# lifeguard-notification-google-chat
Google Chat Notifications

## Usage

```python
@validation(
    "Description",
    actions=[notify_in_single_message],
    schedule={"every": {"minutes": 1}},
    settings={
        "notification": {
            "template": "jinja2 string template"
            "google": {
                "rooms": ["spacewebhookurl"],
            }
        },
    },
)
def a_validation():
    return ValidationResponse("a_validation", NORMAL, {}, {"notification": {"notify": True}})
```
