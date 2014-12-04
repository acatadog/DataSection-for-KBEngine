# -*- coding: gb18030 -*-

"""
write by penghuawei for python3.x
simple read and write tab table file like as ResMgr.pyDataSection of BigWorld

ʹ�÷�����
import PyTabTableSection
tableSection = PyTabTableSection.parse( r"e:/svnroots/xp_bin/trunk/server/GameData/NPC/ScnObjList.txt", "utf-16-le" )
for section in tableSection.values():
	print( section.readInt( "ID" ) )
	print( section.readInt( "HandleID" ) )
	print( section.readString( "Name" ) )
	print( section.readIntArray( "EffectID" ) )
"""

# �ָ�������
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
	��ͷ�����ࣻ
	���ڴ����ͷ���ֶε�Ĭ��ֵ
	"""
	def __init__( self ):
		"""
		"""
		# ��˳�򱣴��ͷ���ֶ���
		self._heads = []
		
		# ���ֶ�����Ϊkey����¼����self._heads�е�λ�ã����ڼӿ���ҵ��ٶ�
		self._head2index = {}
		
		# ��˳�򱣴����ͷ�ֶζ�Ӧ�����ͣ���ǰ�����棬��δ���κ���ص�ʵ�֣�
		self._typeDef = []
		
		# ��˳�򱣴����ͷ�ֶζ�Ӧ��Ĭ��ֵ
		self._defaultValues = []
		
	def initHeads( self, headStr ):
		"""
		��ʼ����ͷ
		
		@return: bool����ʾ��ʼ���ɹ���ʧ��
		"""
		headStr = headStr.rstrip( "\r\n" )	# ȥ�������\r\n
		for index, head in enumerate( headStr.split( SEPARATOR ) ):
			if len(head.strip()) == 0:
				return True
			self._heads.append( head )
			self._head2index[head] = index
		return True
		
	def initTypeDef( self, defStr ):
		"""
		��ʼ����ͷ�ֶε�����
		
		@return: bool����ʾ��ʼ���ɹ���ʧ��
		"""
		#defStr = defStr.rstrip( "\r\n" )	# ȥ�������\r\n
		#self._typeDef = defStr.split( SEPARATOR )
		return True

	def initDefaultValues( self, valueStr ):
		"""
		��ʼ����ͷ�ֶε�Ĭ��ֵ
		
		@return: bool����ʾ��ʼ���ɹ���ʧ��
		"""
		valueStr = valueStr.rstrip( "\r\n" )	# ȥ�������\r\n
		self._defaultValues = valueStr.split( SEPARATOR )
		vl = len(self._defaultValues)
		hl = len(self._heads)
		if vl > hl:
			self._defaultValues = self._defaultValues[0:hl]
		elif vl < hl:
			return False
		return True

	def name2index( self, fieldName ):
		"""
		ͨ���ֶ����������Ӧ��λ��
		
		@return: int32; С��0��ʾû���ҵ����Ӧ���ֶΣ������ʾ�ֶ��ڱ��е�λ��
		"""
		return self._head2index.get( fieldName, -1 )
		
	def index2name( self, index ):
		"""
		ͨ��������ȡ�ֶ���
		@return: str; ��Ӧ���ֶ��������Խ��������쳣
		"""
		return self._heads[index]
	
	def getDefaultValue( self, index ):
		"""
		��ȡĳλ�õ�Ĭ��ֵ
		
		@return: str; �������Խ��������쳣
		"""
		return self._defaultValues[index]

	def getDefaultValueByName( self, fieldName ):
		"""
		ͨ�����ֶζ�ȡ��Ӧ��Ĭ��ֵ
		
		@return: str; �����Ӧ���ֶβ����ڣ��򷵻ؿ��ַ�����""
		"""
		index = self.name2index( fieldName )
		if index < 0:
			return ""
		return self.readDefaultValue( index )
	
class _TabTableRow( object ):
	"""
	�����ݣ�����ÿһ�о���һ��ʵ��
	"""
	def __init__( self, head ):
		"""
		@param head: instance of _TabTableHead
		"""
		self._tableHead = head
		self._values = []
		
	def init( self, valueStr ):
		"""
		��ʼ��ֵ
		"""
		valueStr = valueStr.rstrip( "\r\n" )	# ȥ�������\r\n
		self._values = valueStr.split( SEPARATOR )
		
	def convertToSection( self, rootSection ):
		"""
		@param section: instance of PyTabTableSection
		"""
		parentSection = rootSection.createSection( "item" )
		for index, value in enumerate( self._values ):
			key = self._tableHead.index2name( index )
			val = len( value ) > 0 and value or self._tableHead.getDefaultValue( index )
			section = parentSection.createSection( key )
			section.value = val


def parse( filename, encoding = None ):
	"""
	open *.xml file to PyXMLSection
	
	@return: PyXMLSection
	"""
	print( "PyTabTableSection: start parse '%s'" % filename )
	file = open( filename, "rt", encoding = encoding )
	
	# ��ȡ�ļ�ͷ
	head = file.readline()
	if head[0] in ( "\ufeff", "\ufffe" ):
		head = head[1:]  # ��ȥunicode�ļ�ͷ
	
	
	
	eReadHead = 0
	eReadType = 1
	eReadDefault = 2
	eReadBody = 3
	
	
	
	# PyTabTableSection root
	root = PyTabTableSection( "root" )
	
	# ��ȡÿһ�����ò�ת��ΪPyTabTableSection
	tableHead = _TabTableHead()
	tableRow = _TabTableRow( tableHead )

	# �ѵ�1�д����
	if len( head.rstrip( "\r\n" ) ) == 0 or head[0] in "#;":
		state = eReadHead
	else:
		tableHead.initHeads( head )
		state = eReadType

	for row in file.readlines():
		if len( row.rstrip( "\r\n" ) ) == 0:
			continue	# ���Կ���
		
		if row[0] in "#;":
			continue	# ���Ա�ע
		
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

