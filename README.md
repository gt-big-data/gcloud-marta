# gcloud-marta

This is the home of the GT Big Data Club API for interacting with [Marta GTFS data](google_transit.zip). It's a work in progress, and this README will be updated as we zoom through the semester and make progress!

## Table of Contents

* [Database Manipulation](#database-manipulation)
  * [Connecting](#connecting-to-the-database)
  * [Manipulating](#writing-sql-statements)

## Database Manipulation

The most important part of any _"Big Data"_ project is the data itself.

For this first week, our dataset is Marta's [General Transit Feed Specification](https://www.itsmarta.com/app-developer-resources.aspx), which is a series of nicely unlabeled of CSV files dumped into a pretty little zipped folder on their website.

We've rehosted their data in a much more sensical MySQL database in Google Cloud.

### Connecting to the Database

1. Download [TeamSQL](https://teamsql.io/downloads).

TeamSQL is our cross-platform SQL GUI of choice because it allows easy collaboration with the team via Slack.

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

### Writing SQL Statements

We'll go over this during the meeting today :heart: