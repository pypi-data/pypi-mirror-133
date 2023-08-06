# ntfy-bark

[Bark](https://github.com/Finb/bark) backend for ntfy.

## Installation

``` cmd
pip install ntfy-bark
```

## Usage

Add following lines to your `ntfy.yml`:

``` yaml
ntfy_bark:
    push_url: https://api.day.app/...
```

Finally, send message to your devices with `ntfy -b ntfy_bark send MSG`.
