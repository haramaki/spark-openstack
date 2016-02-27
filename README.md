# spark-openstack
This is Cisco Spark and OpenStack integration software based on Python.
You can create and list VM on OpenStack from Cisco Spark.

# Getting Started

1. Clone repository
1. Get Cisco Spark User Token
1. Run script and post WebHook create request and Cisco Spark
1. Start webhook app and app wait trigger WebHook.
1. After app start post message to pre-confugured room.

## Clone this repository

```
git clone https://github.com/haramaki/spark-openstack.git
```

## Get Cisco Spark User token
Access to Spark developer Page and get User Token. 

https://developer.ciscospark.com/

After Login by Spark account click right upper your icon and get token. 

## Post Message
Before starting Cisco Spark / OpenStack integration,
Test your Token by *postmessage.py* script.

* ROOM is Spark ROOM Name or ID.
* TEXT is message post to Cisco Spark 

```
# python examples/postmessage.py -token TOKEN -room ROOM -text TEXT
```

## Post WebHook
Create WebHook.

* ROOM : Any Message is created at this room, WebHook is triggered
* URL : WebHook destination URL. URL should be public hostname or Global IP of OpenStack Webhook App running.

OpenStack integration app use following URL [http://GLOBAL_IP:8000/webhook]

```
# python examples/postwebhook.py -token TOKEN -room ROOM -url URL
```

## OpenStack WebHook App
Post request and add WebHook to Cisco Spark is required before starting this application.
This app wait request from Cisco Spark at [http://0.0.0.0:8000/webhook].

```
# python webhookapp.py -token SPARK_TOKEN -url OS_KEYSTONE_URL -project OS_PROJECT -user OS_USER -password OS_PASSWORD
```

Send help command to pre-configured room.


# License
This software is licensed under the Apache License, version 2 ("ALv2")
