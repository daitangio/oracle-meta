# -*- mode: org ; mode: visual-line; coding: utf-8 -*- -*
#+Title: RType: Recursive Set type NoSQL DB
#+Author: Giovanni Giorgi
#+Email: jj@gioorgi.com
# ^c^v t to export code

* RType: your fastest Relational database :tryout:

** A table is described as a /set/ of column names only
Internally the system can be meta-described by ordered set.

#+BEGIN_SRC js
  db=RType.openDB(":memory:");
  db.createTable("person", "person_id","name","surname","birdth_dt");
  // II  declaration form:
  db.createTable({
      "house":[
          "location",
          "owner_person_id"
      ],
      "car": [
          "engine_cc_n",
          "year_dt",
          "owner_person_id"
      ]    
  });
  w=db.getInsertWorker(); // <- Autobild a magical interface to your tables, baby
  w.insertOnPerson(1,"Bob","Testy", "19740423");
#+END_SRC
Please observe:
1) For every database a Worker is provided
2) The worker is a typed (somewhat) interface, so you must /know/ at
"design" (compile) time the table names (at least).
3) You must always provide your table declaration, or your system will
   not work at all.
4) You can provide a partial table declaration (only the segment you
   need):
#+BEGIN_SRC js2
  db=RType.openDB(":memory:").getWorkerFor(
      {    "car":
           [ "engine_cc_n","year_dt","model","owner_person_id"]
      }
  ).insertOnCar(1200,"19990101","FordFiesta",1);
#+END_SRC

** You must define a set of Regular expression to tie your model
Foreign keys and type are identified by convention:
For example:
*** $name_id -> integer, primary key or foriegn key
*** $n_flg   -> boolean (0,1)
*** $number_n -> number value (internally stored as string)
*** $date_dt -> iso date  (internally stored as string yyyymmdd)
*** $timestamp_ts -> date + time n GMT format yyymmdd-hhmmss.xyz...
*** $othername -> strings with 4000 char limit






** Foreign Key are not enforced
You can proibit insert (dev mode) or allow them (production, less-rigid mode).
** RType is a relationa database supporting joins
RType core is based on embedded SQLite
** RType did not delete :beta:
RType mark elements for deletation only. 
An async job re-build tables when system is on low load.
** RType system can manage load peaks, but not constant load peaks
In low-load condition RType do the following actions:
1. Try to reduce to zero the async queue
2. 
** No polling: Simple Event engine
RType provide also a event-listener model to attach event to set modifications like:
+ addition of a new element
+ mark-removal of an element
** RType has no transactional semantic :beta:
Storing data has a fixed, predictive cost.
** RType has no replication policy :beta:
Client library manage a pool of replicated RType system.
RType has a async operation model in which all operations are asyncronous.
A standard way of ensuing operation is to do a cascate set of async
operation, one after one.

** RType storage engine is pluggable. 
The reference implementation provide a very fast engine
** Symbolic language support
RType is based on /atoms/ which are unique in the system.


* TODO RType secret trick: optimal for simple relational database     :resee:
If you have a simple relational database, with a lot of one-to-many relations you can use RType to get the job done.
A small SQL-like declarative language is provided in RType for easy access:

#+begin_src js
 db=RType.openDB("RType","root","toor")
 db.add("myfriends", "jresig","bgates")
 db.add("yourfirends", "jresing", "gking")
 db.add("guy-description:jresing", "JQuery Master and Commander")
 db.select("gui-description:*").from(db.select("*").from("myfriend"))
=>
 ["JQuery Master and Commander"]
#+end_src

Many2Many relations can be mapped via two pairs of one-to-many relations.


* Reference

1) http://research.swtch.com/sparse
2) http://www.bradblock.com/Experimental_Analysis_of_a_Fast_Intersection_Algorithm_for_Sorted_Sequences.pdf
3) [[http://research.microsoft.com/pubs/173795/vldb11intersection.pdf][Fast Set Intersection in Memory]]
4) [[http://www.fc.up.pt/dcc/Pubs/TReports/TR06/dcc-2006-06.pdf][Efficient representation of integer sets]]
5) [[http://www.50ply.com/blog/2012/07/21/introducing-fast/][Introducing Fast, Persistent Sets in Ruby]]
6) http://ricerca.mat.uniroma3.it/users/colanton/concise.html
