import math
import random

import numpy as np




class SA:


	def __init__(self,T=500):
		self.x=[]
		self.y=[]
		self.E=0.0
		self.E=0.0
		self.shuffuleplace=[]
		
		self.path=[] #newest
		self.expath=[] #experiment
		self.bestpath=[] #best
		self.bestcost=(-1000)
		self.T=T
		self.acount=0



	def loadData(self,filename):

		for line in open(filename,"r"):
			if not line[0].isdigit(): continue
			px,py=map(float,line.split(","))
			self.x.append(px)
			self.y.append(py)

		return



	def dis(self,i,j):
		return math.sqrt(pow((self.x[i]-self.x[j]),2)+pow((self.y[i]-self.y[j]),2))

	def disall(self):
		#E=self.dis(self.path[0],self.path[-1])
		E=0
		for i,p in enumerate(self.path):
			if i>=len(self.path)-1: return E
			E+=self.dis(self.path[i],self.path[i+1])
		
		return

	def greedy(self):
		self.path.append(0)
		last=0
		pathlst=[i for i in range(len(self.x))]
		pathlst.remove(0)
		
		for i in range(len(self.x)-1):
			index=pathlst[0]
			mindis=self.dis(last,index)

			for j,p in enumerate(pathlst):
			
				newdis=self.dis(last,p)
				if mindis > newdis:
					index=p
					mindis=newdis

			pathlst.remove(index)
			self.path.append(index)
			last=index

		self.path.append(self.path[0])
		





	##reconect two_opt and randomshuffle for sa 


	def two_opt(self):
		N=len(self.path)
		cost=self.disall()

		#i and i+1
		



		for i in range(N-4):
			#j and j+1 (j>=i+2
			p1=self.path[i]
			p2=self.path[i+1]
			l1=self.dis(p1,p2)


			
			for j in range(i+2,N-1):
				q1=self.path[j]
				q2=self.path[j+1]

				l2=self.dis(q1,q2)
				L=l1+l2
				LL=self.dis(p1,q1)+self.dis(p2,q2)

				
				
				if LL<L:
					lc,rc=i+1,j
					
					while True:
						if lc>=rc: break
						tmp=self.path[lc]
						self.path[lc]=self.path[rc]
						self.path[rc]=tmp

						lc+=1
						rc-=1
					break

		
		
		if cost==self.disall(): return False
		#return path
		#prin
		else: return True
		

		
		
		

				
	def randomshuffle(self,per=0.5):
		self.path.pop()
		size=int(len(self.path)*per)
		r=random.randint(0,len(self.path)-size-1)

		shufflepath=[]
		for i in range(size):
			shufflepath.append(self.path.pop(r))

		
		random.shuffle(shufflepath)
		
		for p in shufflepath:
			self.path.insert(r,p)


		end=self.path[0]
		self.path.append(end)

	def p(self,path):
		path.append(10000)
		return
		



	def accept(self,denergy):
		if denergy<0: return True
		
		else:
			if np.random.binomial(1,math.exp(-(denergy)/self.T))==1: return True
			else: return False

	

	def cooling(self):
		self.T=self.T*0.8


	def itertion(self,roop):
		#inicialize path and cost
		self.bestpath=list(self.path)
		self.expath=list(self.path)
		excost=self.disall()
		self.bestcost=excost

		for i in range(roop):
			self.randomshuffle(0.8)
			
			for i in range(10):
				self.two_opt()
			cost=self.disall()

			denergy=cost-excost
			
			
			if cost<self.bestcost:
				
				self.bestpath=list(self.path)
				self.bestcost=cost

			if self.accept(denergy):
				
				self.cooling()
				self.acount+=1
			else:
				
				self.path=list(self.expath)

			
			excost=self.disall()


		return
	


if __name__=="__main__":

	
	filename="input_5.csv"
	print filename
	sa= SA(1000)
	sa.loadData(filename)
	sa.greedy()
	
	
	
	
	sa.itertion(1000)
	sa.path=list(sa.bestpath)
	sa.two_opt()
	print "best:",sa.path,sa.bestcost,sa.disall(),"accept:",sa.acount
	

	f=open("solution_yours_5.csv","w")
	f.write("index\n")
	for p in sa.path:
		f.write(str(p)+"\n")
	f.close()

	
	





	