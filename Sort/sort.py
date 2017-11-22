# -*- coding: utf-8 -*-
'''
各类sort对比
@Author: AC
2017-11-8
'''
__author__ = 'AC'

##############################################
#------------------import--------------------#
############################################## 
import random

##############################################
#------------------常量定义------------------#
##############################################
if __name__ == '__main__':
	# 生成100个随机数
	NumNumbers = 300
	RandomNumbers = [random.uniform(0,10) for x in range(0,NumNumbers,1)]

##############################################
#------------------函数定义------------------#
##############################################


##############################################
#------------------类定义--------------------#
##############################################

###################################
# class sort
# sort类
################################### 
class sort:
	"""通用sort基类"""
	###################################
	# Variables
	################################### 
	__swapCount = 0
	__searchCount = 0

	###################################
	# Swap
	# 在List中交换两数
	################################### 
	def Swap(self, NumberList, i, j):
		tmp = NumberList[i]
		NumberList[i] = NumberList[j]
		NumberList[j] = tmp
		self.__swapCount += 1
		return NumberList

	###################################
	# ClearCount
	# 清除统计量
	################################### 
	def ClearCount(self):
		self.__swapCount = 0
		self.__searchCount = 0

	###################################
	# GetCount
	# 获取统计值（打印）
	################################### 
	def GetCount(self):
		print 'SwapCount = %d, SearchCount = %d' % (self.__swapCount, self.__searchCount)

	###################################
	# AddSearchCount
	# 检索统计值加一
	################################### 
	def AddSearchCount(self):
		self.__searchCount += 1

	###################################
	# BubbleSort
	# 检索统计值加一
	################################### 
	def AddSearchCount(self):
		self.__searchCount += 1

	###################################
	# Sort
	# 排序函数
	################################### 
	def Sort(self, NumberList):
		self.ClearCount()
		self.__Sort(NumberList)
		self.GetCount()
		return NumberList

	###################################
	# __Sort
	# 排序函数(内部实现)(基类实现以冒泡法为例)
	################################### 		
	def __Sort(self, NumberList):
		for i in range(0,len(NumberList)):
			for j in range(0,len(NumberList)-1):
				self.AddSearchCount()
				if NumberList[j]>NumberList[j+1]:
					self.Swap(NumberList,j,j+1)
		return NumberList

###################################
# class BubbleSort (基类sort)
# 冒泡排序，相邻两数，A>B则交换
################################### 
class BubbleSort(sort):
	"""冒泡排序，相邻两数，A>B则交换"""

	###################################
	# Sort
	# 排序函数
	###################################
	def Sort(self, NumberList):
		self.ClearCount()
		self.__Sort(NumberList)
		self.GetCount()
		return NumberList

	###################################
	# __Sort
	# 排序函数(内部实现)
	################################### 		
	def __Sort(self, NumberList):
		for i in range(0,len(NumberList)):
			for j in range(0,len(NumberList)-1):
				self.AddSearchCount()
				if NumberList[j]>NumberList[j+1]:
					self.Swap(NumberList,j,j+1)
		return NumberList


###################################
# class SelectSort (基类sort)
# 选择排序，依次找到最小值并交换
################################### 
class SelectSort(sort):
	"""选择排序，依次找到最小值并交换"""

	###################################
	# Sort
	# 排序函数
	###################################
	def Sort(self, NumberList):
		self.ClearCount()
		self.__Sort(NumberList)
		self.GetCount()
		return NumberList
	###################################
	# __Sort
	# 排序函数(内部实现)
	################################### 		
	def __Sort(self, NumberList):
		for i in range(0,len(NumberList)-1):
			minIdx = i
			for j in range(i+1,len(NumberList)):
				self.AddSearchCount()
				if NumberList[j]<NumberList[minIdx]:
					minIdx = j
			if minIdx != 1:
				self.Swap(NumberList,minIdx,i)
		return NumberList

###################################
# class InsertSort (基类sort)
# 插入排序，从第二个开始找啊到的第一个比自己小的值插在后面
################################### 
class InsertSort(sort):
	"""插入排序，从第二个开始找啊到的第一个比自己小的值插在后面"""

	###################################
	# Sort
	# 排序函数
	###################################
	def Sort(self, NumberList):
		self.ClearCount()
		self.__Sort(NumberList)
		self.GetCount()
		return NumberList


	###################################
	# __Sort
	# 排序函数(内部实现)
	################################### 		
	def __Sort(self, NumberList):
		for i in range(1,len(NumberList)):
			target = NumberList[i]
			j = i
			while (j > 0 and target < NumberList[j-1]):
				self.AddSearchCount()
				NumberList[j] = NumberList[j-1]
				j -= 1
			NumberList[j] = target
		return NumberList

###################################
# class QuickSort (基类sort)
# 快速排序（二分分治，将一个数组按照一个基准数分割，比基准数大的放基准数的右边，小的放左边。）
################################### 
class QuickSort(sort):
	"""快速排序（二分分治，将一个数组按照一个基准数分割，比基准数大的放基准数的右边，小的放左边。）"""

	###################################
	# Sort
	# 排序函数
	################################### 
	def Sort(self, NumberList):
		self.ClearCount()
		self.__Sort(NumberList, 0, len(NumberList)-1)
		self.GetCount()
		return NumberList

	###################################
	# __Sort
	# 排序函数(内部实现)
	################################### 		
	def __Sort(self, NumberList, left, right):
		if (left >= right):
			# 递归的终止条件
			return NumberList
		pivotIndex = self.__SortPartition(NumberList, left, right) # first time ( pivotIndex位置数字确定不再排序 )
		self.__Sort(NumberList, left, pivotIndex-1) # ( 左右分别再次排序 )
		self.__Sort(NumberList, pivotIndex+1, right)
		return NumberList

	def __SortPartition(self, NumberList, left, right):
		# pivot: 中心点
		pivot = NumberList[left]
		pivotIndex = left

		while (left < right):
			while (left < right and NumberList[right] >= pivot):
				self.AddSearchCount()
				right -= 1
			# self.Swap(NumberList, left, right)
			while (left < right and NumberList[left] <= pivot):
				self.AddSearchCount()
				left += 1
			self.Swap(NumberList, left, right)			
		self.Swap(NumberList, pivotIndex, left) # improve
		return left


##############################################
#------------------脚本开始------------------#
##############################################
if __name__ == '__main__':
	# 主线程
	print RandomNumbers
	# BubbleSort
	RandNum = list(RandomNumbers)
	cSort = BubbleSort()
	print 'BubbleSort: ',
	print cSort.Sort(RandNum)

	# SelectSort
	RandNum = list(RandomNumbers)
	cSort = SelectSort()
	print 'SelectSort: ',
	print cSort.Sort(RandNum)

	# InsertSort
	RandNum = list(RandomNumbers)
	cSort = InsertSort()
	print 'InsertSort: ',
	print cSort.Sort(RandNum)

	# QuickSort
	RandNum = list(RandomNumbers)
	cSort = QuickSort()
	print 'QuickSort: ',
	print cSort.Sort(RandNum)


