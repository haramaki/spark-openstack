# spark-openstack

# Getting Started

## Clone this repository

```
git clone https://github.com/haramaki/spark-openstack.git
```

## Get Cisco Spark User token
Access to Spark developer Page and get User Token. 

https://developer.ciscospark.com/

After Login by Spark account click right upper your icon and get token. 

## Post Message

```
# python examples/postmessage.py -token TOKEN -room ROOM -text TEXT
```

## Post WebHook
Create WebHook.

```
# python examples/postwebhook.py -token TOKEN -room ROOM -url URL
```

## OpenStack WebHook App
Post request and add WebHook to Cisco Spark is required before starting this application.
This app wait request from Cisco Spark at [http://0.0.0.0:8000/webhook].

```
# python webhookapp.py -token SPARK_TOKEN -url OS_KEYSTONE_URL -project OS_PROJECT -user OS_USER -password OS_PASSWORD
```

# License
This software is licensed under the Apache License, version 2 ("ALv2")
