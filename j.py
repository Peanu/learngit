#-*- coding: utf-8 -*-
#coding=utf-8
import os

'''
#import sys;
import time
import support
"""
 while True :
     print 1111
     print 'hellow word!'
     print  '你好！！'
     pass  
print"""hellow Jack:
"""
					
		i ros how aer you?"""
#raw_input("\n\nPress the enter key to exit.")
a,b,c=1,2,'john'
print a
print b
print c
s='ilovepython'
print s[5:]
print s*2
print s+"\n"+"yes"
list=['abcd',786,2.23,'john',70.2]
tinylist=[123,'john']
list[0]=111

print list
print list[0]

print list[1:3]
print list[2:]
print tinylist*2
print list+tinylist

dict={}
dict['one']='this is one'
dict[2]="this is two"
tinydict={'name':'john','code':6734,'depct':'sales'}

print dict['one']
print dict[2]
print tinydict
print tinydict.keys
print tinydict.values

a=10
b=20
c=0

c**=a
print "6-c=",c

c//=a
print "7-c=",c

list=[1,2,3,4,5]
a=3 
b=4
if (a in list):
	print 'a in the list'
else:
	print "a don't in the list"

if (b not in list):
	print 'true'
else:
	print 'false'

a=20
b=30
if (a is b):
	print 'true'
else:
	print 'false'

if (id(a)==id(b)):
	print 'true'
else:
	print 'false'

flag=False 
name='luren'
if name=='python':
	flag=True
	print "pass"
else:
	print name

count=0
while (count<9):
	print 'the count is:',count
	count+=1	
print "Good bye"
			

i=1
while i<10:
	i+=1
	if i%2>0:
		continue
	print i


i=1
while 1:
	if i>10:
		break
	print i
	i+=1
"""var=1
while var==1:
	num=raw_input("Enter a number:")
	print "you enter:",num
print 'Goodbye!'"""

count=1
while count<5:
	print count,'is less then 5'
	count+=1
else:
	print count,'is not less then 5'


for letter in 'python':
	print 'The current letter is:',letter

fruites=['banana','apple','mango']
for fruite in fruites:
	print 'the current fruite is:',fruite
for index in range(len(fruites)):
	print 'the current fruite is:',fruites[index]


for num in range(10,20):
	for i in range(2,num):
		if num%i==0:
			j=num/i
			print '%d=%d*%d'%(num,i,j)
			break
	else:
		print '%d is ...'%(num)


i=2
while (i<100):
	j=2
	while (j<=(i/j)):
		if not(i%j):break
		j+=1
	if (j>(i/j)):print i,"是素数"
	i+=1
print 'Goodbye！'

dict={'name':'xuzefeng','age':'21','ciass':'first'}
print dict
print dict['name']
dict['name']='xuyuechen'
print dict['name']
dict['school']='SUMHS'
print dict
dict1 = {'Name': 'Zara', 'Age': 7};
dict2 = {'Name': 'Mahnaz', 'Age': 27};
dict3 = {'Name': 'Abid', 'Age': 27};
dict4 = {'Name': 'Zara', 'Age': 7};
print "Return Value : %d" %  cmp (dict1, dict2)
print "Return Value : %d" %  cmp (dict2, dict3)
print "Return Value : %d" %  cmp (dict1, dict4)
print len(dict4)
print str(dict4)
print type(dict4)
print 'value :%s'%dict4.items()
dict4.update(dict2)
print dict4
t=time.localtime()
print '%s'% time.asctime(t)

def procedure():
	time.sleep(2.5)
t0=time.clock()
print t0
procedure()
print time.clock()
print time.clock()-t0,"seconds process time"

t0=time.time()
print t0
procedure()
print time.time()
print time.time()-t0,"seconds wall time"

print 'time.ctime():%s'%time.ctime()
#print time.gmtime()
print time.asctime(time.localtime())
print time.strftime("%Y-%m-%d %H:%M:%S ",time.localtime())

def printme(str):
	print str
	return

printme('my name is xuzefeng')
printme('print again')

def changeme(mylist):
	mylist.append([1,2,3,4])
	print "indoor value",mylist
	mylist=[0]
	print mylist
	return mylist
mylist=[1,2,3,4]
changeme(mylist)
print "outdoor value",mylist

sum=lambda arg1,arg2:arg1+arg2
print "result is :",sum('xuzefeng','wwww')

def sum(arg1,arg2):
	total=arg1+arg2
	print "indoor value :",total
	return 1
total=sum(10,20)
print "outdoor value :",total

support.print_func("xu")

Money = 2000
def AddMoney():
   # 想改正代码就取消以下注释:
   global Money
   Money = Money + 1
 
print Money
AddMoney()
print Money

times=dir(time)
print times
support.print_func("dddddddd")
'''

fo=open("foo.txt","wb")
fo.write("www.runoob.com!\n Very good site!\n")
fo.write("xuzefeng")
fo=open("foo.txt","r+")
str=fo.read(15)
print "read value is :",str
position=fo.tell()
print "new area is:",position
position=fo.seek(0,1)
str=fo.read(30)
print str

fo.close
id=os.getcwd()
print id

try:
	fh=open("testfile","w")
	try:
		fh.write("zhe shi yi ge che shi wen jian")
	finally:
		print "close files"
		fh.close()
except :
	print "Error:don't find files"
else:
	print "sccessed!!!"
	fh.close
# 定义函数
def temp_convert(var):
    try:
        return int(var)
    except ValueError, Argument:
        print "参数没有包含数字\n", Argument

# 调用函数
temp_convert("xyz");


def mye(level):
		if level<1:
				raise Exception("Invalid level!",level)
try:
	mye(0)
except:
	print 1
else:
	print 2
	
class Employee(object):
	"""docstring for Employee"""
	employeeCount=0
	def __init__(self,name,salary):
		self.name=name
		self.salary=salary
		Employee.employeeCount+=1
	def displayCount(self):
		print "Total Employee %d" % Employee.employeeCount

	def displayEmployee(self):
		print "Name :",self.name,",Salary :", self.salary

		
emp1=Employee("Zara",2000)
emp2=Employee("Manni",5000)
emp1.displayEmployee()
emp2.displayEmployee()
print "Total Employee %d" %Employee.employeeCount

'''
class Point:
   def __init__( self, x=0, y=0):
      self.x = x
      self.y = y
   def __del__(self):
      class_name = self.__class__.__name__
      print class_name, "销毁"

pt1 = Point()
pt2 = pt1
pt3 = pt1
print id(pt1), id(pt2), id(pt3) # 打印对象的id
del pt1
del pt2
del pt3
'''

class Parent:
	parentAttr=100
	def __init__(self):
		print "调用父类构造函数"
	def parentMethod(self):
		print "调用父类方法"
	def setAttr(self,attr):
		Parent.parentAttr=attr
	def getAttr(self):
		print "父类属性 :",Parent.parentAttr

class Child(Parent):
	def __init__(self):
		print "调用子类构造方法"
	def childMethod(self):
		print "调用子类方法 child method"
c=Child()
c.childMethod()
c.parentMethod()
c.setAttr(200)
c.getAttr()


class Vector:
	def __init__(self,a,b):
		self.a=a
		self.b=b

	def _str_(self):
		return "Vector (%d,%d)" %(self.a,self.b)
	def _add_(self,other):
		return Vector(self.a+other.a,self.b+other.b)

v1=Vector(2,10)
v2=Vector(5,-2)
print v1,v2
		
class JustCount:
	__secretCount=0
	publicCount=0

	def count(self):
		self.__secretCount+=1
		self.publicCount+=1
		print self.__secretCount
count=JustCount()
count.count()
count.count()
print count.publicCount
print count._JustCount__secretCount
print r'xuvvv"ddd"ddd ccc'
print chr(19940608)
print chr(19960616)