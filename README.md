oracle-meta
===========

Alpha stage

A set of experimental script to deal with Oracle database 
and some new idea about meta programming.


pocket-oracle
==============
Dockerized oracle


RType
==============
Python experimental new data system. See relative folder

Excel export
=============
To generate an excel export try out
table2excel  scott/tiger@orcl emp dep myviewz | tr '\t' \, >my.csv

Credits: Tom Kyte 
http://tkyte.blogspot.co.at/2009/10/httpasktomoraclecomtkyteflat.html



Unindexed Foreign Keys
==========================
In some situation an unindexed foreign key cause oracle to do a table lock.
*missed-fk-indexes.sql* help you finding out such issues


# Local variables:
# mode:markdown
# End:
