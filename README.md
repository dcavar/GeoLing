# GeoLing

Authors:
- [Damir Cavar] <damir@linguistlist.org>
- [Malgosia Cavar] <gosia@linguistlist.org>
- [Peace Han] <peace@linguistlist.org>
- [Nils Hjortnaes] <nils@linguistlist.org>
- [Lwin Moe] <lwin@linguistlist.org>

Many more volunteers and helpers were involved over the years, here are some:
- Julian Dietrich
- Noah Kaufman

The LINGUIST List [GeoLing] service and app is available online at:

[https://geoling.linguistlist.org/](https://geoling.linguistlist.org/)



## Background

Back in 2013 [Damir Cavar] and [Lwin Moe] had the idea to develop a visualization service for all jobs, events, institutions announced via [The LINGUIST List] that maps those as pins on the global map.

Whenever a conference is announced, or a job, summer school, new project, the information is processed, marked up with geo coordinate information, and displayed on [GeoLing].

[LINGUIST List] had policies that did not allow sending out information about local events, talks at institutions of just regional or local relevance, etc. As a solution we designed [GeoLing] with an interface to submit local events and display them on a world map, without breaking the [LINGUIST List] policy of general relevance for the global linguistic community.


## Features

Issues posted on [The LINGUIST List] mailing list are augmented with geo coordinates and displayed on a global map. The map is location sensitive on devices with GPS or similar location services. If you use it on your mobile phone, it will show you all events and institutions
around your location.

Local events can be added freely after registration by users. All local events have to be approved by moderators of the system.

Event dates and locations are linked to a CalDav and CardDav server. This means that all events can be augmented with a vCal and vCard entry that can be clicked and downloaded by the users.

Only future events are displayed. We would like to have a user interface to display past event as well. This is some functionality that we wanted to work on.

The code is linked to all the specific [LINGUIST List] infrastructure, database, feeds, connectors to the Amazon Alexa system, to social media posting, etc. With a few tweaks this can be adapted to serve your needs.


## Code

The app is written in:

-	Python 3.x
-	Django 2.x

[Nils Hjortnaes] ported it from Django 1.x to 2.x.

It makes use of various JavaScript libraries.

We use it with PostgreSQL 9.x in the backend. It should work fine with any other SQL database that is supported by Python and Django.

The backend uses a CalDav and CardDav server.



[GeoLing]: https://geoling.linguistlist.org/ "GeoLing"
[Peace Han]: https://linguistlist.org/people/peace.html "Peace Han"
[Nils Hjortnaes]: https://linguistlist.org/people/nils.html "Nils Hjortnaes"
[Lwin Moe]: https://linguistlist.org/people/lwin.html "Lwin Moe"
[Damir Cavar]: https://linguistlist.org/people/damir.html "Damir Cavar"
[Malgosia Cavar]: https://linguistlist.org/people/gosia.html "Malgosia Cavar"
[The LINGUIST List]: https://new.linguistlist.org/ "The LINGUIST List"
[LINGUIST List]: https://new.linguistlist.org/ "The LINGUIST List"
