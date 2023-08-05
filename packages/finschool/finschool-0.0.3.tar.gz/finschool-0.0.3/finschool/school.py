# -*- coding: utf-8 -*-
#school.py

class Student:
	def __init__(self,name,lastname):
		self.name = name
		self.lastname = lastname
		self.exp = 0 #ค่าประสบการณ์นักเรียน
		self.lesson = 0 #จำนวนครั้งที่เรียน
		self.vehicle = 'Tesla'

	@property
	def fullname(self):
		return '{} {}'.format(self.name, self.lastname)

	def Coding(self):
		'''นี่คือวิชาเขียนโปรแกรม'''
		self.AddEXP()
		print('{}กำลังเขียนโปรแกรม... '.format(self.fullname))

	def ShowEXP(self):
		print('{} ได้คะแนน {} exp (เรียนไป {} ครั้ง): '.format(self.name,self.exp,self.lesson))

	def AddEXP(self):
		self.exp += 10
		self.lesson += 1

	def __str__(self):
		return self.fullname

	def __repr__(self):
		return self.fullname

	def __add__(self,other):
		return self.exp + other.exp


class Lambhorgini:
	def __init__(self):
		self.model = 'Lambhor Model S'

	def SelfDriving(self,st):
		print('Hello nice to meet you...กำลังพาคุณ{}กลับบ้าน'.format(st.name))

	def __str__(self):
		return self.model


class SpecialStudent(Student):
	def __init__(self,name,lastname,father):
		super().__init__(name,lastname)

		self.father = father
		self.vehicle = Lambhorgini()
		print('Do you know who is my Dad?..! My father\'s name is {}'.format(self.father))

	def AddEXP(self):
		self.exp += 30
		self.lesson += 2


class Teacher:
	def __init__(self,fullname):
		self.fullname = fullname
		self.students = []

	def CheckStudent(self):
		for i,st in enumerate(self.students):
			print('-------นักเรียนของครู: {}------'.format(self.fullname))
			print('{}--->{} [{} exp][เรียนไป {} ครั้ง]'.format(i+1, st.fullname, st.exp, st.lesson))

	def AddStudent(self,st):
		self.students.append(st)


#print('File:',__name__)
if __name__ == '__main__':
	
	#Day 0
	allstudent = []

	teacher1 = Teacher('Ada lovelace')
	teacher2 = Teacher('Bill Gates')
	print(teacher1.students)

	#Day 1
	print('---Day1---')
	st1 = Student('Albert','Einstein')
	allstudent.append(st1)
	teacher2.AddStudent(st1)
	print(st1.fullname)


	#Day2
	print('----Day2-----')
	st2 = Student('Steve','Jobs')
	allstudent.append(st2)
	teacher2.AddStudent(st2)
	print(st2.fullname)

	#Day3
	print('---Day3---')
	st1.Coding()
	st2.Coding()

	#Day4
	print('---Day4---')
	st1.ShowEXP()
	st2.ShowEXP()

	#Day5
	print('-----Day5-----')

	stp1 = SpecialStudent('Thomas','Edison','Hitler')
	allstudent.append(stp1)
	teacher1.AddStudent(stp1)
	print(stp1.fullname)
	print('ครูครับขอคะแนนฟรีสัก 20 คะแนนได้ไหม')
	stp1.exp = 20 #แก้ไขค่าไนคลาสได้
	stp1.ShowEXP()
	stp1.Coding()


	#Day6
	print('----Day6----')
	stp1.ShowEXP()
	for i in range(4):
		st1.Coding()
		st2.Coding()
		st1.ShowEXP()
		st2.ShowEXP()

	#Day7
	print('----Day7----')
	print('นักเรียนหบัยย้ายกันยังไงจ๋ะ?')
	print(allstudent)
	for st in allstudent:
		print('ผม: {} กลับบ้านด้วย {} ครับ'.format(st.name,st.vehicle))
		if isinstance(st,SpecialStudent):
			st.vehicle.SelfDriving(st)

	#Day 8
	print('-------Day8--------')

	teacher1.CheckStudent()
	teacher2.CheckStudent()

	print('two students exp', st1 + st2)