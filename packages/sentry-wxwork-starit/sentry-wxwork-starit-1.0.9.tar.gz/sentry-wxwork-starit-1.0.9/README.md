# Sentry plugin for WxWork

Support WxWork, Modify from sentry-googlechat, Thanks Jonhnny Weslley.


## How will it look like

<img src="https://raw.githubusercontent.com/jweslley/sentry-googlechat/master/notification.png" width="500">


## Requirements

* Sentry 10.0.0 or newer


## Installation

In your `requirements.txt` file, add the below package name to install the WxWork Plugin.

```
sentry-wxwork-starit
```

Restart your Sentry instance: 

```
docker-compose restart
```

## Configuration

Go to your Sentry web interface and open ``Settings`` page of one of your projects. Locate the Integrations management screen and click 'Configure Plugin' below the 'sentry-wxwork-starit' item.

<img src="https://raw.githubusercontent.com/jweslley/sentry-googlechat/master/configuration.png" width="500">

Create a new Incoming Webhook bot in WxWork and paste the URL into the Webhook URL field, then click 'Save Changes'.
There are some other optional configuration options at the moment, but the WebHook URL is the only required field.

When ready, click 'Test Plugin' to generate an exception and send a message to your chosen WebHook URL.



## License

MIT License. Copyright (c) 2022 , Thanks Jonhnny Weslley.
