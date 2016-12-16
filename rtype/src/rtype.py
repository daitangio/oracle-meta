#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
######  #######
#     #    #      #   #  #####   ######
#     #    #       # #   #    #  #
######     #        #    #    #  #####
#   #      #        #    #####   #
#    #     #        #    #       #
#     #    #        #    #       ######

 --test
   Run unit test. 

Minimum Required:Python 2.7.6

Support
https://github.com/sixty-north/asq
linq-like for python (over 40 functions)



Demo:
 you organize a simple people/friend/place stuff
then you start filling it with data, and when data growth, the system accomodate it
 displacing data into different storages

"""

from __future__ import division, generators, with_statement
import sys,unittest

# Rtype V1
import inspect,itertools

### Low level function
def log(*args, **kwargs):
    if len(kwargs)==0:
        if len(args)==2:
            print "RTYPE LOG DEBUG %s %s "  % (args)
        else:
            print "RTYPE LOG DEBUG %s"  % (args)
    else:
        print "RTYPE LOG [KW:%s] %s" % (kwargs, args)

### Data source resolutin function
def resolveDataSource(uri):
    return uri
#########################

# See http://stackoverflow.com/questions/196960/can-you-list-the-keyword-arguments-a-python-function-receives
def view(iterableDataSource,selectFunction):
    log("Function signature:",inspect.getargspec(selectFunction))
    spec=inspect.getargspec(selectFunction)
    # Take the args and remap them
    # We can have
    # 'self', 'view', ....
    # or
    # 'view', .....
    # Anway the call works well in execute
    if spec.args[0] in ('self','view'):
        requiredProjection=spec.args[1:]
        if requiredProjection[0] in ('self','view'):
            requiredProjection=requiredProjection[1:]
    else:
        raise Exception('First parameter must called view or self')
    log("Param spec:",requiredProjection)
    # Set up a concrete view based on iterableDataSource and requiredProjection
    # This class is ACTUALIZED with the iterableDataSource just now...
    ###myDataView=buildView(uri,requiredProjection)    
    class DataView:
        def __init__(self,iterableDataSource):            
            self.iterableDataSource=iterableDataSource
        def execute(self):
            # Execute the task calling the selectFunction
            # Projection string are only just string so push them as they are
            # they will be used as index on data
            return selectFunction(self,*requiredProjection)
        def join(self,view2Join,joinConditionFunction):
            columns=inspect.getargspec(joinConditionFunction).args            
            if columns[0]=='view':
                columns=columns[1:]
            else:
                log(warn="joinCondition function has no view params...")
            log("Join condition signature:",columns)
            # do join somewhat....
            # build a new view....
            return view('bho',joinConditionFunction) 

        ### Following function yield data
        def __call__(self):
            return self.iterableDataSource()
            
        def orderby(self,columnName):
            """
             Sort and 'Unroll' data
             Consider also
             https://docs.python.org/2.7/library/itertools.html?highlight=itertools#module-itertools
            """                        
            
            myiterable=sorted(self.__call__(), key=lambda e: e[columnName]  )
            def fx():
                for elem in myiterable:
                    yield elem
            return view(fx,selectFunction)
        def reverse(self):
            def frev():
                for ex in reversed(list(self.__call__())):
                    yield ex
            return view(frev,selectFunction)
    dv=DataView(iterableDataSource)
    dv.__doc__="Data view based on "+str(selectFunction)+" SPEC:"+str(spec)
    return dv


########### TEST BEGIN
class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.success=False
        self.executionTimes=0
        #print "SETUP SELF="+str(self)
    def simpleSource(self):        
        yield {'fname':'foo.txt', 'size':-1}
        yield {'fname':'boo.txt', 'size':1}
        yield {'fname':'mazinga.txt', 'size':1}
        yield {'fname':'daitarn1.txt', 'size':1}
        yield {'fname':'afilefirst.txt', 'size':20}
    def tearDown(self):
        pass
    def test_testrun(self):
        assert True

    ## SELECT FUNCTION USED ON TESTS
    def selectFname(self,view,fname):
        for line in view():
            print line[fname]
            self.success=True
        self.executionTimes=self.executionTimes+1

    def test_norun(self):
        def select(view,fname,size):
            log("View="+str(view)+" Fname="+fname+" Size="+size)
            self.success=True
        # Pass the meta-select function to the viewbuilder
        v=view( self.simpleSource ,select);
        assert self.success==False, "No execution expected"
        # Try to force documentation printing and check no effect
        print "DOC "+str(v.__doc__)
        assert self.success==False, "No execution expected"
    def disab_test_stupid(self):
        def select(view,fname,size):
            log("View="+str(view)+" Fname="+fname+" Size="+size)
            self.success=True
        # Pass the meta-select function to the viewbuilder
        view( self.simpleSource  ,select).execute();
        assert self.success==True, "Select function not called at all"
    def test_fsview(self):
        def myselect(view,fname,size):
            for line in view():
                print repr(line)
                print "RECORD:",line[fname],line[size]
                if line[fname] == 'daitarn1.txt':
                    self.success=True                
        # Pass the meta-select function to the viewbuilder
        view( self.simpleSource ,myselect).execute();
        assert self.success==True, "Select function not found expected data"
    def test_orderby(self):
        def myselect(view,fname,size):
            for l in view():
                self.success= (l[fname]=='afilefirst.txt')
                #log(l[fname])
                break
        # Pass the meta-select function to the viewbuilder
        view( self.simpleSource ,myselect).orderby('fname').execute();
        assert self.success==True, "Ordering does not work"

    def test_orderby2(self):
        def myselect(view,fname,size):
            for l in view():
                self.success= (l[fname]=='foo.txt')
                log(l[fname])
                break
        # Pass the meta-select function to the viewbuilder
        view( self.simpleSource ,myselect).orderby('size').execute();
        assert self.success==True, "Ordering does not work"

    def test_reverse_orderby(self):
        def myselect(view,fname,size):
            for l in view():
                self.success= (l[fname]=='mazinga.txt')
                #log(l[fname])
                break
        # Pass the meta-select function to the viewbuilder
        view( self.simpleSource ,myselect).orderby('fname').reverse().execute();
        assert self.success==True, "Ordering does not work"

    def test_faker(self):
        # See https://github.com/joke2k/faker
        from faker import Factory,Faker
        f=Factory.create('it_IT')
        f.seed(23041974)
        
        for i in range(0,10):
            print f.name()
    # def test_fsview_nested(self):
    #     """Find files with the same name"""
    #     def s(view,fname):
    #         self.selectFname(view,fname)
    #     view( './test/dir1',s).execute()
    #     assert self.success==True, "Select function not called at all"
    # def test_fsview_plain(self):
    #     """Find files with the same name"""
    #     v=view('./test/dir1',self.selectFname)
    #     v.execute()
    #     assert self.success==True, "Select function not called at all"
    #     print "DOC=",v.__doc__
    
    def disab_test_simple_join(self):        
        """Find files with the same name
        Resee: join is wrong defined so
        """
        v1=view('./test/dir1',self.selectFname)
        v2=view('./test/dir2',self.selectFname)
        ## Join condition here is THE SAME of the select FNAME.
        ## Remember only signature is important
        v1.join(v2,self.selectFname).execute()
        assert self.executionTimes==1,"Execution time !=1 %s" % (self.executionTimes)

if __name__ == '__main__':
    import sys
    if len(sys.argv)==1:
        print __doc__   
        unittest.main(argv=["-v"])
    elif sys.argv[1]=="--test":
        print "Unit test verbose launching right now"
        unittest.main(argv=["-v"])

