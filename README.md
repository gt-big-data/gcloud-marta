# gcloud-marta

This is the home of the GT Big Data Club API for interacting with [Marta GTFS data](google_transit.zip).

## Table of Contents

* [Database Manipulation](#database-manipulation)
  * [Connecting](#connecting-to-the-database)
  * [Understanding](#understanding-the-data)
    * [Agency](#agency)
    * [Calendar](#calendar)
    * [Calendar Dates](#calendar-dates)
    * [Routes](#routes)
    * [Shapes](#shapes)
    * [Stop Times](#stop-times)
    * [Stops](#stops)
    * [Trips](#trips)
  * [Manipulating](#manipulating-the-data)

## Database Manipulation

The most important part of any _"Big Data"_ project is the data itself.

For this first week, our dataset is Marta's [General Transit Feed Specification](https://www.itsmarta.com/app-developer-resources.aspx), which is a series of nicely unlabeled of CSV files dumped into a pretty little zipped folder on their website.

We've rehosted their data in a much more sensical MySQL database in Google Cloud.

### Connecting to the Database

1. Download [TeamSQL](https://teamsql.io/downloads).

TeamSQL is our cross-platform SQL GUI of choice because it allows easy collaboration with the team via Slack.

Once you download, it'll ask you to register for an account using your email and password. Tell me which email you use so I can add you to the Backend team.

2. Download the [Cloud SQL Proxy](https://cloud.google.com/sql/docs/mysql/connect-admin-proxy).

For your convenience, I have already downloaded the [Windows](/db/proxies/cloud_sql_proxy_win.exe), [Linux](/db/proxies/cloud_sql_proxy_linux), and [Mac](/db/proxies/cloud_sql_proxy_mac) clients to this repository. You need to have this proxy running in order to connect to the database from your local machine.

###### _Note for Mac and Linux users: You may have to `chmod +x` the proxy to make it executable._

3. Start the proxy.

From your terminal, launch the proxy. If you've cloned this repo, then the command should be

```cmd
./db/proxies/cloud_sql_proxy_<PLATFORM> -instances=<INSTANCE_CONNECTION_NAME>=tcp:3306
```

where `<PLATFORM>` is the appropriate platform suffix and `<INSTANCE_CONNECTION_NAME>` is a secret string that I'll reveal at our meeting today.

###### _Please don't commit this string to our repo, that could cause our GCP bill to spike which is bad news._

4. Connect to the proxied database via TeamSQL.

To connect, click the plus button next to Connections and select MySQL as your database format. Then, configure the database with the following options:

![Configuration options](/db/teamsql-config.png)

###### _Again, I'll tell you the username at the meeting._

Now, you should be connected! So long as your proxy is running, you'll have real-time updates, I think.

###### _Note for those who hate Google: I've created an [SQL Dump](/db/sqldumpfile) which you can use to recreate your own offline version of the database. I do not promise to keep this updated._

###### _In fact, I promise to keep it not updated._

### Understanding the Data

Luckily for us, this data isn't very intuitive. [There's a full reference here](https://developers.google.com/transit/gtfs/reference/), but I've put an abbreviated version below specific to our dataset.

#### Quick Reference

* [Agency](#agency)
* [Calendar](#calendar)
* [Calendar Dates](#calendar-dates)
* [Routes](#routes)
* [Shapes](#shapes)
* [Stop Times](#stop-times)
* [Stops](#stops)
* [Trips](#trips)

#### Agency

There's only one row in this table, so I'm just replicating it here. This table contains information about MARTA.

| agency_id | agency_name                                  | agency_url              | agency_timezone  | agency_lang | agency_phone  | agency_email          |
|-----------|----------------------------------------------|-------------------------|------------------|-------------|---------------|-----------------------|
| MARTA     | Metropolitan Atlanta Rapid Transit Authority | [http://www.itsmarta.com](http://www.itsmarta.com) | America/New_York | en          | (404)848-5000 | custserv@itsmarta.com |

#### Calendar

The calendar table reflects the operating schedule of different MARTA services.

| service_id | monday | tuesday | ... | saturday | sunday | start_date | end_date |
|------------|---------|---------|-----|----------|---------|------------|----------|
| int: 3-5 | boolean | boolean | ... | boolean | boolean | 20180818 | 20181207 |

* service_id
  * An ID that uniquely identifies a set of dates when service is available for one or more routes. Referenced in [trips](#trips).
* monday [...] friday
  * A boolean value (either 1 or 0) indicating whether the service is available on a given day during the time frame
* start_date
  * A date (string) indicating when the time frame begins. In our dataset, it's always "20180818" (August 18 2018).
* end_date
  * A date (string) indicating when the time frame ends. In our dataset, it's always "20181207" (December 7 2018).

#### Calendar Dates

This table specifies dates where the normal operating schedule (specified in [Calendar](#calendar)) is changed for some reason.

| service_id | date | exception_type |
|------------|------|----------------|
| int | str | int: 1-2 |

* service_id
  * An ID that uniquely identifies a set of dates when service is available for one or more routes. Referenced in [trips](#trips).
* date
  * A string specifying the date where service is excepted.
* exception_type
  * An integer, either one or two, where
    * 1 means that service is added for the specified date, and
    * 2 means that service is removed for the specified date.

#### Routes

This table contains information about all of the routes MARTA offers.

| route_id | route_short_name | route_long_name | route_desc | route_type | route_url | route_color | route_text_color |
|----------|------------------|-----------------|------------|-------------|-----------|-------------|------------------|
| int | str | str | \<empty> | int: 1 or 3 | \<empty> | str | \<empty> |

* route_id
  * Uniquely identifies a route.
* route_short_name
  * A short, usually numeric (but not always, _annoyingly_) text identifier for the route
* route_long_name
  * A longer, human-readable route name.
* route_desc
  * Always empty.
* route_type
  * An integer, either 1 or 3, where
    * 1 indicates a subway line and
    * 3 indicates a bus line.
* route_url
  * Always empty.
* route_color
  * A hex code indicating the color assigned to the route.
* route_text_color
  * Always empty.

#### Shapes

Shapes describe the physical path that a vehicle takes. Shapes consist of a sequence of points, where tracing the points in order provides the path of the vehicle.

| shape_id | shape_pt_lat | shape_pt_lon | shape_pt_sequence |
|----------|--------------|--------------|--------------|
| int | decimal | decimal | int |

* shape_id
  * Uniquely identifies a shape. This ID can be cross-referenced with [Trips](#trips) (in the shape_id column, **not** the trip_id column) to bind a shape to a trip.
* shape_pt_lat
  * A WSG 84 latitude of where to place the point on a map.
* shape_pt_lon
  * A WSG 84 longitude of where to place the point on a map.
* shape_pt_sequence
  * An integer representing where in the shape the point should go - for example, a row with shape_pt_sequence 4 would go immediately after shape_pt_sequence 3.

#### Stop Times

Contains information about when vehicles on routes stop at stops.

| trip_id | arrival_time | departure_time | stop_id | stop_sequence |
|---------|--------------|----------------|---------|---------------|
| int | HH:MM:SS | HH:MM:SS | int | int |

* trip_id
  * Uniquely identifies the trip which makes these stops.
* arrival_time
  * A 24-hour timestamp in the format HH:MM:SS that specifies when a vehicle arrives at a stop during a specific trip along a route.
* departure_time
  * A 24-hour timestamp in the format HH:MM:SS that specifies when a vehicle departs from a stop during a specific trip along a route.
* stop_id
  * Identifies which stop the vehicle is stopping at.
* stop_sequence
  * An integer specifying which stop along the trip this particular stop is. For example, a bus will travel directly from a stop with stop_sequence 3 to stop_sequence 4 if those stops have the same trip_id.

#### Stops

This dataset contains information on all of the stops in the entire MARTA ecosystem.

| stop_id | stop_code | stop_name | stop_lat | stop_lon |
|---------|-----------|-----------|----------|----------|
| int | int | string | decimal | decimal |

* stop_id
  * Uniquely identifies a single stop, which may be used by multiple routes.
* stop_code
  * Another unique identifier, used internally with MARTA (and maybe displayed on the stops themselves)
* stop_name
  * A human readable name for a stop.
* stop_lat
  * WSG 84 latitude of the stop
* stop_lon
  * WSG 84 longitude of the stop

#### Trips

This dataset contains information about all the trips made by vehicles across all of MARTA.

| route_id | service_id | trip_id | trip_headsign | direction_id | block_id | shape_id |
|----------|------------|---------|---------------|--------------|----------|----------|
| int | int | int | string | boolean | int | int |

* route_id
  * Contains an ID that uniquely identifies a route.
* service_id
  * Contains an ID that represents when the route is in service. The details of when this route runs are given by [Calendar](#calendar) and [Calendar Dates](#calendar-dates).
* trip_id
  * An ID tied to the trip. These are unique; each trip has a different ID
* trip_headsign
  * A message that's displayed somehow during the trip to identify it - think the big block letters on the front of the bus.
* direction_id
  * A boolean value (represented as int 1 or 0) that indicates which direction a trip is going. It's arbitrarily assigned ([source](https://developers.google.com/transit/gtfs/reference/#tripstxt)), so we'll have to figure out what this means in the context of each trip. It could be used to represent inbound/outbound, eastbound/westbound, southbound/northbound, etc.
* block_id
  * An ID for a particular vehicle, i.e. all trips with the same block ID use the same bus or train
* shape_id
  * References a [shape](#shapes) that can be drawn on a map to represent the route this trip takes.
