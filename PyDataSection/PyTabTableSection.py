# -*- coding: gb18030 -*-

"""
write by penghuawei for python3.x
simple read and write tab table file like as ResMgr.pyDataSection of BigWorld

使用方法：
import PyTabTableSection
tableSection = PyTabTableSection.parse( r"e:/svnroots/xp_bin/trunk/server/GameData/NPC/ScnObjList.txt", "utf-16-le" )
for section in tableSection.values():
	print( section.readInt( "ID" ) )
	print( section.readInt( "HandleID" ) )
	print( section.readString( "Name" ) )
	print( section.readIntArray( "EffectID" ) )
"""

# 分隔符定义
SEPARATOR = "\t"

from PyDataSection.PyDataSection import PyDataSectionNode

class PyTabTableSection( PyDataSectionNode ):
	def __init__( self, name = "", parentNode = None ):
		PyDataSectionNode.__init__( self, name, parentNode )
		
	def newSection_( self, name ):
		"""
		"""
		return PyTabTableSection( name, None )
		





class _TabTableHead( object ):
	"""
	表头处理类；
	用于处理表头和字段的默认值
	"""
	def __init__( self ):
		"""
		"""
		# 按顺序保存表头的字段名
		self._heads = []
		
		# 用字段名做为key，记录其在self._heads中的位置，用于加快查找的速度
		self._head2index = {}
		
		# 按顺序保存与表头字段对应的类型（当前仅保存，并未做任何相关的实现）
		self._typeDef = []
		
		# 按顺序保存与表头字段对应的默认值
		self._defaultValues = []
		
	def initHeads( self, headStr ):
		"""
		初始化表头
		
		@return: bool；表示初始化成功或失败
		"""
		headStr = headStr.rstrip( "\r\n" )	# 去除多余的\r\n
		for index, head in enumerate( headStr.split( SEPARATOR ) ):
			if len(head.strip()) == 0:
				return True
			self._heads.append( head )
			self._head2index[head] = index
		return True
		
	def initTypeDef( self, defStr ):
		"""
		初始化表头字段的类型
		
		@return: bool；表示初始化成功或失败
		"""
		#defStr = defStr.rstrip( "\r\n" )	# 去除多余的\r\n
		#self._typeDef = defStr.split( SEPARATOR )
		return True

	def initDefaultValues( self, valueStr ):
		"""
		初始化表头字段的默认值
		
		@return: bool；表示初始化成功或失败
		"""
		valueStr = valueStr.rstrip( "\r\n" )	# 去除多余的\r\n
		self._defaultValues = valueStr.split( SEPARATOR )
		vl = len(self._defaultValues)
		hl = len(self._heads)
		if vl > hl:
			self._defaultValues = self._defaultValues[0:hl]
		elif vl < hl:
			return False
		return True

	def getHeadFields( self ):
		"""
		"""
		return self._heads

	def name2index( self, fieldName ):
		"""
		通过字段名查找相对应的位置
		
		@return: int32; 小于0表示没有找到相对应的字段，否则表示字段在表中的位置
		"""
		return self._head2index.get( fieldName, -1 )
		
	def index2name( self, index ):
		"""
		通过索引获取字段名
		@return: str; 对应的字段名，如果越界则产生异常
		"""
		return self._heads[index]
	
	def getDefaultValue( self, index ):
		"""
		读取某位置的默认值
		
		@return: str; 如果索引越界则产生异常
		"""
		return self._defaultValues[index]

	def getDefaultValueByName( self, fieldName ):
		"""
		通过表字段读取对应的默认值
		
		@return: str; 如果相应的字段不存在，则返回空字符串：""
		"""
		index = self.name2index( fieldName )
		if index < 0:
			return ""
		return self.readDefaultValue( index )
	
class _TabTableRow( object ):
	"""
	表内容，表中每一行就是一个实例
	"""
	def __init__( self, head ):
		"""
		@param head: instance of _TabTableHead
		"""
		self._tableHead = head
		self._values = []
		
	def init( self, valueStr ):
		"""
		初始化值
		"""
		valueStr = valueStr.rstrip( "\r\n" )	# 去除多余的\r\n
		self._values = valueStr.split( SEPARATOR )
		
	def convertToSection( self, rootSection ):
		"""
		@param section: instance of PyTabTableSection
		"""
		parentSection = rootSection.createSection( "item" )
		for index, key in enumerate( self._tableHead.getHeadFields() ):
			val = len( self._values[index] ) > 0 and self._values[index] or self._tableHead.getDefaultValue( index )
			section = parentSection.createSection( key )
			section.value = val
			#print( "_TabTableRow::convertToSection(), key = '%s', value = '%s'" % (key, val) )


def parse( filename, encoding = None ):
	"""
	open *.xml file to PyXMLSection
	
	@return: PyXMLSection
	"""
	print( "PyTabTableSection: start parse '%s'" % filename )
	file = open( filename, "rt", encoding = encoding )
	
	# 读取文件头
	head = file.readline()
	if head[0] in ( "\ufeff", "\ufffe" ):
		head = head[1:]  # 裁去unicode文件头
	
	
	
	eReadHead = 0
	eReadType = 1
	eReadDefault = 2
	eReadBody = 3
	
	
	
	# PyTabTableSection root
	root = PyTabTableSection( "root" )
	
	# 读取每一行配置并转化为PyTabTableSection
	tableHead = _TabTableHead()
	tableRow = _TabTableRow( tableHead )

	# 把第1行处理掉
	if len( head.rstrip( "\r\n" ) ) == 0 or head[0] in "#;":
		state = eReadHead
	else:
		tableHead.initHeads( head )
		state = eReadType

	for row in file.readlines():
		if len( row.rstrip( "\r\n" ) ) == 0:
			continue	# 忽略空行
		
		if row[0] in "#;":
			continue	# 忽略备注
		
		if state == eReadHead:
			tableHead.initHeads( row )
			state = eReadType
		elif state == eReadType:
			tableHead.initTypeDef( row )
			state = eReadDefault
		elif state == eReadDefault:
			tableHead.initDefaultValues( row )
			state = eReadBody
		elif state == eReadBody:
			tableRow.init( row )
			tableRow.convertToSection( root )
		else:
			assert False
	
	file.close()
	print( "PyTabTableSection: end parse '%s'" % filename )
	return root

