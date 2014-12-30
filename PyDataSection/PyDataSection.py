# -*- coding: gb18030 -*-
"""
write by penghuawei for python 3.x
PySection的基础类
"""
import sys

class PyDataSection( object ):
	"""
	section基础类，仅记录自身的名称、值以及父类
	"""
	DEBUG = False
	def __init__( self, name = "", value = "", parentNode = None ):
		self.name_ = name  # str；section 名称
		self.value_ = value  # str；section原始值
		self.parentNode_ = parentNode
		
	def debug_output( self, *args ):
		"""
		"""
		if not self.DEBUG:
			return;
		exceInfo = sys.exc_info()
		if exceInfo is None or exceInfo == ( None, None, None ) :
			print( "PyDataSection EXCEHOOK_MSG: no exception in stack!" )
		else :
			print( "PyDataSection EXCEHOOK_MSG: --" )
			for arg in args :
				print( arg )
			sys.excepthook( *exceInfo )
		
	def __str__( self ):
		return self.format()
		
	@property
	def name( self ):
		return self.name_
		
	def __setValue( self ):
		return self.value_
		
	def __getValue( self, value ):
		assert isinstance( value, str )
		self.value_ = value
		
	value = property(__setValue,		__getValue,		None, "I'm property.")
		
	def format( self, prefix = "" ):
		"""
		格式化输出自己
		@return: str
		"""
		return "%s<%s> %s </%s>" % (prefix, self.name_, self.value_, self.name_)
		
	###############################################
	# _as method                                  #
	###############################################
	def asBinary_( self ):
		return "this is base of PyDataSection instance, so no any value to format."
	
	def asBool_( self ):
		if self.value_.isdigit():
			return bool( int(self.value_) )
		else:
			return self.value_ in ("True", "true")
	
	def asFloat_( self ):
		try:
			return float(self.value_)
		except Exception as exc:
			self.debug_output( exc )
			return 0.0
	
	def asInt_( self ):
		try:
			return int(self.value_)
		except Exception as exc:
			self.debug_output( exc )
			return 0
	
	def asMatrix_( self ):
		raise "sorry, I don't support this function."
	
	def asString_( self ):
		return self.value_
	
	def asVector2_( self ):
		try:
			result = [ float(e) for e in self.value_.split(" ") if len(e.strip()) > 0 ][0:2]
		except Exception as exc:
			self.debug_output( exc )
			return (0.0, 0.0)

		if len( result ) < 2:
			result.extend( [0.0, 0.0, 0.0] )
			result = result[0:2]
		return tuple( result )

	def asVector3_( self ):
		try:
			result = [ float(e) for e in self.value_.split(" ") if len(e.strip()) > 0 ][0:3]
		except Exception as exc:
			self.debug_output( exc )
			return (0.0, 0.0, 0.0)

		if len( result ) < 3:
			result.extend( [0.0, 0.0, 0.0] )
			result = result[0:3]
		return tuple( result )
		
	def asVector4_( self ):
		try:
			result = [ float(e) for e in self.value_.split(" ") if len(e.strip()) > 0 ][0:4]
		except Exception as exc:
			self.debug_output( exc )
			return (0.0, 0.0, 0.0, 0.0)
		
		if len( result ) < 4:
			result.extend( [0.0, 0.0, 0.0, 0.0] )
			result = result[0:4]
		return tuple( result )

	def asIntArray_( self, separator = "," ):
		try:
			return tuple( [ int(e) for e in self.value_.split(separator) if len(e.strip()) > 0 ] )
		except Exception as exc:
			self.debug_output( exc )
			return ()

	def asIntArrays_( self, separator = ";", separator2 = "," ):
		try:
			result = []
			value = self.value_
			for v1 in value.split(separator):
				if len(v1.strip()) == 0:
					continue
				result.append( [ int(v2) for v2 in v1.split(separator2) if len(v2.strip()) > 0 ] )
			return result
		except Exception as exc:
			self.debug_output( exc )
			return []

	def asFloatArray_( self, separator = "," ):
		try:
			return tuple( [ float(e) for e in self.value_.split(separator) if len(e.strip()) > 0 ] )
		except Exception as exc:
			self.debug_output( exc )
			return ()
	
	def asFloatArrays_( self, separator = ";", separator2 = "," ):
		try:
			result = []
			value = self.value_
			for v1 in value.split(separator):
				if len(v1.strip()) == 0:
					continue
				result.append( [ float(v2) for v2 in v1.split(separator2) if len(v2.strip()) > 0 ] )
			return result
		except Exception as exc:
			self.debug_output( exc )
			return []

	def asStringArray_( self, separator = "," ):
		try:
			return tuple( [ e for e in self.value_.split(separator) if len(e.strip()) > 0 ] )
		except Exception as exc:
			self.debug_output( exc )
			return ()

	def asStringArrays_( self, separator = ";", separator2 = "," ):
		try:
			result = []
			value = self.value_
			for v1 in value.split(separator):
				if len(v1.strip()) == 0:
					continue
				result.append( [ v2 for v2 in v1.split(separator2) if len(v2.strip()) > 0 ] )
			return result
		except Exception as exc:
			self.debug_output( exc )
			return []


	def asWideString_( self ):
		raise "sorry, I don't support this function."
	
	###############################################
	# _to method                                  #
	###############################################
	def toBinary_( self, value ):
		raise "sorry, I don't support this function."
	
	def toBool_( self, value ):
		if bool(value):
			self.value_ = "true"
		else:
			self.value_ = "false"
	
	def toFloat_( self, value ):
		self.value_ = str( float(value) )
	
	def toInt_( self, value ):
		self.value_ = str( int(value) )
	
	def toMatrix_( self, value ):
		raise "sorry, I don't support this function."
	
	def toString_( self, value ):
		self.value_ = str( value )
	
	def toVector2_( self, value ):
		assert isinstance( value, ( tuple, list ) )
		assert len(value) == 2
		self.value_ = "".join( (str(float(value[0])), " ", str(float(value[1]))) )
		
	def toVector3_( self, value ):
		assert isinstance( value, ( tuple, list ) )
		assert len(value) == 3
		self.value_ = "".join( (str(float(value[0])), " ", str(float(value[1])), " ", str(float(value[2]))) )
		
	def toVector4_( self, value ):
		assert isinstance( value, ( tuple, list ) )
		assert len(value) == 4
		self.value_ = "".join( (str(float(value[0])), " ", str(float(value[1])), " ", str(float(value[2])), " ", str(float(value[3]))) )
	
	def toIntArray_( self, value, separator = "," ):
		assert isinstance( value, ( tuple, list ) )
		self.value_ = separator.join( [ str(e) for e in value ] )
	
	def toFloatArray_( self, value, separator = "," ):
		assert isinstance( value, ( tuple, list ) )
		self.value_ = separator.join( [ str(e) for e in value ] )
	
	def toStringArray_( self, value, separator = "," ):
		assert isinstance( value, ( tuple, list ) )
		self.value_ = separator.join( [ str(e) for e in value ] )
	
	def toWideString_( self, value ):
		raise "sorry, I don't support this function."
	
	
	###############################################
	# property                                    #
	###############################################
	asBinary		= property(asBinary_,		toBinary_,		None, "I'm property.")
	asBool			= property(asBool_,			toBool_,		None, "I'm property.")
	asFloat			= property(asFloat_,		toFloat_,		None, "I'm property.")
	asInt			= property(asInt_,			toInt_,			None, "I'm property.")
	asMatrix		= property(asMatrix_,		toMatrix_,		None, "I'm property.")
	asString		= property(asString_,		toString_,		None, "I'm property.")
	asVector2		= property(asVector3_,		toVector2_,		None, "I'm property.")
	asVector3		= property(asVector3_,		toVector3_,		None, "I'm property.")
	asVector4		= property(asVector4_,		toVector4_,		None, "I'm property.")
	asIntArray		= property(asIntArray_,		toIntArray_,	None, "I'm property.")
	asFloatArray	= property(asFloatArray_,	toFloatArray_,	None, "I'm property.")
	asWideString	= property(asWideString_,	toWideString_,	None, "I'm property.")
	
# end of class PyDataSection


class PyDataSectionNode( PyDataSection ):
	"""
	section的节点，一个节点下可以继续存在节点
	"""
	def __init__( self, name = "", value = "", parentNode = None ):
		PyDataSection.__init__( self, name, value, parentNode )
		self.childNodes_ = []
		
	def format( self, prefix = "" ):
		"""
		把自己以及子节点下所有的
		由于一个节点下还可以有多个节点，因此生成的数据以xml的形式来保存
		"""
		strData = [ e.format( "\t" + prefix ) for e in self.childNodes_ ]
		valData = ""
		heads = "<%s>" % self.name_
		if len( self.value_ ) > 0:
			if len( self.childNodes_ ) == 0:
				spv = self.value_.split( "\n" )
				if len( spv ) == 1:
					strB = prefix + heads
					strE = "</%s>\n" % ( self.name_ )
					valData = self.value_
				else:
					strB = prefix + heads + "\n"
					strE = "%s</%s>\n" % ( prefix, self.name_ )
					valList = []
					for e in spv:
						valList.append( "\t%s%s\n" % ( prefix, e ) )
					valData = "".join( valList )
			else:
				strB = prefix + heads + "\n"
				strE = "%s</%s>\n" % ( prefix, self.name_ )
				valList = []
				for e in self.value_.split( "\n" ):
					valList.append( "\t%s%s\n" % ( prefix, e ) )
				valData = "".join( valList )
		else:
			if len( self.childNodes_ ) == 0:
				strB = prefix + heads
				strE = "</%s>\n" % ( self.name_ )
			else:
				strB = prefix + heads + "\n"
				strE = "%s</%s>\n" % ( prefix, self.name_ )
		strData.insert( 0, strB )
		strData.insert( 1, valData )
		strData.append( strE )
		vd = "".join( strData )
		return vd
		
	def newSection_( self, name ):
		"""
		"""
		raise "you must impl this function in you own class"
		return PyDataSectionNode( name )
		
	def addSection_( self, name ):
		"""
		@param name: instance of PyDataSectionNode
		@type  name: PyDataSectionNode
		@return:     instance of PyDataSectionNode
		@rtype:      PyDataSectionNode
		"""
		assert isinstance( name, str ), "it's no str type."
		n = self.newSection_( name )
		n.parentNode_ = self
		self.childNodes_.append( n )
		return self.childNodes_[-1]
	
	def findChildIndex( self, name, startpos = 0 ):
		"""
		@return: int, 返回基于0的位置索引，-1表示没有找到符合条件的。
		"""
		length = len( self.childNodes_ )
		index = startpos
		while index < length:
			if self.childNodes_[index].name == name:
				return index
			index += 1
		return -1
	
	def getSection_( self, path, create = False ):
		"""
		@param create: if node not found then create it
		@type  create: bool
		@return: PyDataSectionNode or None
		@rtype:  PyDataSectionNode/None
		"""
		p = path.split( "/" )
		sec = self
		for e in p:
			i = sec.findChildIndex( e )
			if i > -1:
				sec = sec.childNodes_[i]
			else:
				if not create:
					return None
				sec = sec.addSection_( e )
		return sec
		
	def getSections_( self, path ):
		p = path.rsplit( "/", 1 )
		
		if len( p ) == 1:
			sec = self
			n = p[0]
		else:
			sec = self.getSection_( p[0] )
			n = p[1]
			
		nodes = []
		if sec is None:
			return nodes
			
		pos = 0
		while True:
			pos = sec.findChildIndex( n, pos )
			if pos > -1:
				nodes.append( sec.childNodes_[pos] )
				pos += 1
			else:
				break
		return nodes

		def getPrevSection_( path, createIfNotExisted ):
			"""
			取得路径指向的section的前一个section，并返最后一个key
			例如：getPrevSection_( "a/b/c/d", true ) 则返回“d, newSection”，并且section指向"a/b/c"
			@return: (last-section-name, last-section-instance)
			"""
			splitP = str.rsplit("/", 1)

			if len(splitP) == 1:
				section = self
				key = splitP[0]
			else:
				section = getSection_( splitP[0], createIfNotExisted );
				key = splitP[1];
			return (key, section)

	def __len__( self ):
		return len( self.childNodes_ )

	def child( self, index ):
		"""
		@return: instance of PyDataSectionNode
		@rtype:  PyDataSectionNode
		"""
		return self.childNodes_[index]
		
	def childName(self, index ):
		"""
		@return: name of child
		@rtype:  string
		"""
		return self.childNodes_[index].name
		
	def copy( self, source ):
		"""
		from source copy into me;
		all copy is reference, no real copy;
		
		@param source: instance of PyDataSectionNode
		@type  source: PyDataSectionNode
		"""
		if not isinstance( source, PyDataSectionNode ):
			raise "Unknow source"
		self.value_ = source._value
		for e in source.childNodes_:
			self.createSection( e.name ).copy( e )
	
	def createSection( self, path ):
		"""
		create new section from path.
		example:
		<root>
			<a> abc </a>
		</root>
		
		root.createSection( "a/b/c" )
		<root>
			<a> abc </a>
			<a>
				<b>
					<c></c>
				</b>
			</a>
		</root>
		
		
		@param path: string as "abc/def/node1"
		@type  path: string
		@return:            instance of PyDataSectionNode
		@rtype:             PyDataSectionNode
		"""
		splitP = path.split( "/" )
		
		sec = self
		if len( splitP ) == 1:
			key = splitP[0]
		else:
			key = splitP.pop( -1 )
			for p in splitP:
				sec = sec.addSection_( p )
			
		return sec.addSection_( key )
		
	def deleteSection( self, name ):
		"""
		@return: True or False
		@rtype:  bool
		"""
		p = name.rsplit( "/", 1 )
		
		if len( p ) == 1:
			sec = self
			n = p[0]
		else:
			sec = self.getSection_( p[0] )
			n = p[1]
			
		if sec is None:
			return False
			
		i = sec.findChildIndex( n )
		if i <= -1:
			return False
			
		del sec.childNodes_[i]
		return True
	
	def has_key( self, key ):
		return self.findChildIndex( key ) > -1
		
	def items( self ):
		for child in self.childNodes_:
			yield child.name, child
	
	def keys( self ):
		for child in self.childNodes_:
			yield child.name
	
	def values( self ):
		return self.childNodes_.__iter__()
		
	def __getitem__( self, name ):
		return self.getSection_( name )
	
	###############################################
	# read method                                 #
	###############################################
	def readBool( self, name ):
		try:
			return self.getSection_(name).asBool_()
		except Exception as exc:
			self.debug_output( exc )
			return False
		
	def readFloat( self, name ):
		try:
			return self.getSection_(name).asFloat_()
		except Exception as exc:
			self.debug_output( exc )
			return 0.0
	
	def readFloats( self, name ):
		try:
			return [ e.asFloat_() for e in self.getSections_( name ) ]
		except Exception as exc:
			self.debug_output( exc )
			return []
	
	def readInt( self, name ):
		try:
			return self.getSection_(name).asInt_()
		except Exception as exc:
			self.debug_output( exc )
			return 0
	
	def readInts( self, name ):
		try:
			return [ e.asInt_() for e in self.getSections_( name ) ]
		except Exception as exc:
			self.debug_output( exc )
			return []
	
	def readMatrix( self, name ):
		return self.getSection_(name).asMatrix_()
	
	def readString( self, name ):
		try:
			return self.getSection_(name).asString_()
		except Exception as exc:
			self.debug_output( exc )
			return ""
	
	def readStrings( self, name ):
		try:
			return [ e.asString_() for e in self.getSections_( name ) ]
		except Exception as exc:
			self.debug_output( exc )
			return []
	
	def readVector2( self, name ):
		try:
			return self.getSection_(name).asVector2_()
		except Exception as exc:
			self.debug_output( exc )
			return (0.0, 0.0)
	
	def readVector2s( self, name ):
		try:
			return [ e.asVector2_() for e in self.getSections_( name ) ]
		except Exception as exc:
			self.debug_output( exc )
			return []
	
	def readVector3( self, name ):
		try:
			return self.getSection_(name).asVector3_()
		except Exception as exc:
			self.debug_output( exc )
			return (0.0, 0.0, 0.0)
	
	def readVector3s( self, name ):
		try:
			return [ e.asVector3_() for e in self.getSections_( name ) ]
		except Exception as exc:
			self.debug_output( exc )
			return []
	
	def readVector4( self, name ):
		try:
			return self.getSection_(name).asVector4_()
		except Exception as exc:
			self.debug_output( exc )
			return (0.0, 0.0, 0.0, 0.0)
	
	def readVector4s( self, name ):
		try:
			return [ e.asVector4_() for e in self.getSections_( name ) ]
		except Exception as exc:
			self.debug_output( exc )
			return []

	def readIntArray( self, name, separator = "," ):
		try:
			return self.getSection_(name).asIntArray_( separator )
		except Exception as exc:
			self.debug_output( exc )
			return ()
	
	def readIntArrays( self, name, separator = ";", separator2 = "," ):
		try:
			return self.getSection_( name ).asIntArrays_( separator, separator2 )
		except Exception as exc:
			self.debug_output( exc )
			return []

	def readFloatArray( self, name, separator = "," ):
		try:
			return self.getSection_(name).asFloatArray_( separator )
		except Exception as exc:
			self.debug_output( exc )
			return ()
	
	def readFloatArrays( self, name, separator = ";", separator2 = "," ):
		try:
			return self.getSection_( name ).asFloatArrays_( separator, separator2 )
		except Exception as exc:
			self.debug_output( exc )
			return []

	def readStringArray( self, name, separator = "," ):
		try:
			return self.getSection_(name).asStringArray_( separator )
		except Exception as exc:
			self.debug_output( exc )
			return ()
	
	def readStringArrays( self, name, separator = ";", separator2 = "," ):
		try:
			return self.getSection_( name ).asStringArrays_( separator, separator2 )
		except Exception as exc:
			self.debug_output( exc )
			return []

	def readWideString( self, name ):
		return self.getSection_(name).asWideString_()
	
	def readWideStrings( self, name ):
		return [ e.asWideString_() for e in self.getSections_( name ) ]
	
	
	###############################################
	# write method                                #
	# return: PyDataSectionNode                       #
	###############################################
	def write( self, name, value ):
		sec = self.getSection_(name, True)
		sec.value_ = str( value )
		return sec

	def writeBool( self, name, value ):
		sec = self.getSection_(name, True)
		sec.toBool_( value )
		return sec
		
	def writeFloat( self, name, value ):
		sec = self.getSection_(name, True)
		sec.toFloat_( value )
		return sec
	
	def writeFloats( self, name, values ):
		assert isinstance( values, ( tuple, list ) )
		n, sec = self.getPrevSection_( name, True )
		for e in values:
			sec.createSection( n ).toFloat_( e )
	
	def writeInt( self, name, value ):
		sec = self.getSection_(name, True)
		sec.toInt_( value )
		return sec
	
	def writeInts( self, name, values ):
		assert isinstance( values, ( tuple, list ) )
		n, sec = self.getPrevSection_( name, True )
		for e in values:
			sec.createSection( n ).toInt_( e )
	
	def writeMatrix( self, name, value ):
		sec = self.getSection_(name, True)
		sec.toMatrix_( value )
		return sec
	
	def writeString( self, name, value ):
		sec = self.getSection_(name, True)
		sec.toString_( value )
		return sec
	
	def writeStrings( self, name, values ):
		assert isinstance( values, ( tuple, list ) )
		n, sec = self.getPrevSection_( name, True )
		for e in values:
			sec.createSection( n ).toString_( e )
	
	def writeVector2( self, name, value ):
		sec = self.getSection_(name, True)
		sec.toVector2_( value )
		return sec
	
	def writeVector2s( self, name, values ):
		assert isinstance( values, ( tuple, list ) )
		n, sec = self.getPrevSection_( name, True )
		for e in values:
			sec.createSection( n ).toVector2_( e )
	
	def writeVector3( self, name, value ):
		sec = self.getSection_(name, True)
		sec.toVector3_( value )
		return sec
	
	def writeVector3s( self, name, values ):
		assert isinstance( values, ( tuple, list ) )
		n, sec = self.getPrevSection_( name, True )
		for e in values:
			sec.createSection( n ).toVector3_( e )
	
	def writeVector4( self, name, value ):
		sec = self.getSection_(name, True)
		sec.toVector4_( value )
		return sec
	
	def writeVector4s( self, name, values ):
		assert isinstance( values, ( tuple, list ) )
		n, sec = self.getPrevSection_( name, True )
		for e in values:
			sec.createSection( n ).toVector4_( e )

	def writeIntArray( self, name, value, separator = "," ):
		sec = self.getSection_(name, True)
		sec.toIntArray_( value, separator )
		return sec
	
	def writeIntArrays( self, name, values, separator = ";", separator2 = "," ):
		self.writeStringArrays( name, values, separator, separator2 )

	def writeFloatArray( self, name, value, separator = "," ):
		sec = self.getSection_(name, True)
		sec.toFloatArray_( value, separator )
		return sec
	
	def writeFloatArrays( self, name, values, separator = ";", separator2 = "," ):
		self.writeStringArrays( name, values, separator, separator2 )

	def writeStringArray( self, name, value, separator = "," ):
		sec = self.getSection_(name, True)
		sec.toStringArray_( value, separator )
		return sec

	def writeStringArrays( self, name, values, separator = ";", separator2 = "," ):
		assert isinstance( values, ( tuple, list ) )
		s = []
		for intVS in values:
			s.append( separator2.join( [str(e) for e in intVS] ) )
			
		sec = self.getSection_(name, True)
		sec.toString_( separator.join( s ) )

	def writeWideString( self, name, value ):
		sec = self.getSection_(name, True)
		sec.toWideString_( value )
		return sec
	
	def writeWideStrings( self, name, values ):
		assert isinstance( values, ( tuple, list ) )
		n, sec = self.getPrevSection_( name, True )
		for e in values:
			sec.createSection( n ).toWideString_( e )

# end of class PyDataSectionNode

