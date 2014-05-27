# -*- mode: org ; mode: visual-line; coding: utf-8 -*- -*
#+Title: RType: Recursive Set type NoSQL DB
#+Author: Giovanni Giorgi
#+Email: jj@gioorgi.com
# ^c^v t to export code
*  Wellcome to RType!



+ Data are opaque entity, without nulls, and with distinct values
+ Data are accessed via /Views/
+ Views are bi-dimensional relations
For instance, the file system can be accessed via a View:

#+BEGIN_SRC python :tangle rtypeV1.py
  #!/bin/env python
  # Example1
  import sys
  sys.path.append("src")
  
  from rtype import view
  def select(view,fname,size):
      result=view.orderby(fname)
      for line in result:
          print line.fname,line.size      
  # Pass the meta-select function to the viewbuilder
  view('filesystem:/var/',select);
  
  # Example2
  # Gropup people by birthplace:
  #def group(view,name,  
#+END_SRC
In RType, data can grow to disk without problem.
The RType system will provide the best relational adapter system (memory, RDBMS, NoSQL db, etc) based on growth usage

Internally RType will guarantee the best efficent way to store the data.
RType is aimed to provied maximum performance for the following operation: put, get, intersect, union
Removal is a lazy operation, and will be performed as suboptimal task.



* No polling: Simple Event engine
RType provide also a event-listener model to attach event to set modifications like:
+ addition of a new element
+ removal of an element

* Concurrent: multi process on shared file system




When you define a RType database you must specify the maximum key length you care about.
The key length is fixed for performance reason and will directly affect some storage performance.





RType storage engine is pluggable. 
The reference implementation provide a very fast engine and a trasactional-optional engine (altrougth based on a Global Lock).

* RType secret trick: optimal for simple relational database
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


* API




* IDEA2
** Symbol is a declarative language...
with imperative nature.


The expression can contain 2-dimensional relation

#+BEGIN_SRC text

Hello_world.string().print()
=> "Hello world"


person[name,age] = 'Nick,'47, 'Clara,'23
person[name,age].orderby(age).count()

// Lambda guy:
(int x) -> x * x
(int x) -> { ..... }

#+END_SRC


comma ',' is used to separate data.
' is used to quote symbol. Quoted symbol can be seen as string (anyway they are unique).

Escape is obtained via the '\' char
So a comma string is 

'\,, 


Quoted symbol are string.
String can be transformed into symbol with the symbol function

Nick == ('Nick).symbol()

And symbol can be stringified via string() function so

Nick.string() == "Nick" == 'Nick

Nick.string().symbol() == Nick


Function are directly applied to types, 

** File are data, data are files
In symbol file system primitive and data is the same.
You can usually access to file system via a relational view, using a special function wich remap file system:

#+BEGIN_SRC text
fs('/home/jj')[name,creation_time].print()
#+END_SRC

The [ ] is the "select" operator which remap











* Reference

1) http://research.swtch.com/sparse
2) http://www.bradblock.com/Experimental_Analysis_of_a_Fast_Intersection_Algorithm_for_Sorted_Sequences.pdf
3) [[http://research.microsoft.com/pubs/173795/vldb11intersection.pdf][Fast Set Intersection in Memory]]
4) [[http://www.fc.up.pt/dcc/Pubs/TReports/TR06/dcc-2006-06.pdf][Efficient representation of integer sets]]
5) [[http://www.50ply.com/blog/2012/07/21/introducing-fast/][Introducing Fast, Persistent Sets in Ruby]]
6) http://ricerca.mat.uniroma3.it/users/colanton/concise.html
