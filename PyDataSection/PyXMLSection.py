# -*- coding: gb18030 -*-
"""
write by penghuawei for python3.x
一个简单访问 xml 配置的工具。
from PyDataSection import PyXMLSection
rootSection = PyXMLSection.parse( filename )
rootSection["key"] = value
rootSection.readString( "anykey" )

SXML["key"].save( filename )	# save as ...
SXML.save() # save to src file
"""
from PyDataSection.PyDataSection import PyDataSectionNode

class PyXMLSection( PyDataSectionNode ):
	"""
	"""
	def __init__( self, name = "", value = "", parentNode = None ):
		PyDataSectionNode.__init__( self, name, value, parentNode )
		self.attrs = {}
		# 指向原始的打开文件
		self.filename = None
		
	def format( self, prefix = "" ):
		"""
		format all PyXMLSection to string
		"""
		strData = [ e._format2str( "\t" + prefix ) for e in self.self.childNodeValue_ ]
		attrsStr = " ".join( [ "%s='%s'" % ( k, v ) for k, v in self.attrs.items() ] )
		valData = ""
		if len( attrsStr ) > 0:
			heads = "<%s %s>" % ( self.name_, attrsStr )
		else:
			heads = "<%s>" % self.name_
		if len( self.value_ ) > 0:
			if len( self.self.childNodeValue_ ) == 0:
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
			if len( self.self.childNodeValue_ ) == 0:
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
		return PyXMLSection( name )
	
	def save( self, filename = None ):
		"""
		"""
		assert filename is not None or self.filename is not None
		if filename is None:
			filename = self.filename
		saveTo( filename, self )
	

# end of class: PyXMLSection



from xml import sax
from xml.sax.handler import ContentHandler
from xml.sax.xmlreader import AttributesImpl

class SimpleXMLHandler( ContentHandler ):
	"""
	"""
	default_char_code = "gb18030"
	def __init__( self ):
		"""
		"""
		ContentHandler.__init__( self )
		
		self._t_nodes = []
		self._t_parent_node = None
		self.rootNode = None
	
	def startDocument( self ):
		"""
		"""
		#print("parse starting.")
		pass
		
	def endDocument( self ):
		"""
		"""
		#print("parse over.")
		pass
	
	def startElement( self, name, attrs ):
		"""
		"""
		#print "startElement", name, type( attrs ), attrs
		#creating new node
		if len( self._t_nodes ) == 0:
			node = PyXMLSection( str( name ) )
			self.rootNode = node
		else:
			node = self._t_nodes[-1].createSection( str( name ) )
		self._t_nodes.append( node )
		
		# process attrs
		for key in attrs.getNames():
			value = attrs.getValue(key)
			#print "--------> %s'%s':%s'%s'" % (type(key),key,type(value),value )
			node.attrs[key] = value
	
	def endElement( self, name ):
		"""
		"""
		#print "endElement", name
		if len( self._t_nodes ) > 0:
			node = self._t_nodes.pop()
		if len( node.value ) > 0:
			node.value = node.value.strip( " \n\r\t" )
		if node.name != str( name ):
			raise "element not match. element name = '%s', param name = '%s'" % ( node.name, name )

	def characters( self, content ):
		"""
		"""
		#print "characters", content
		#date = content.encode( self.default_char_code )
		data = content.strip("\t")
		if len( data ) == 0: return
		
		try:
			node = self._t_nodes[-1]
		except:
			raise "xml file not right."
		if len( node.value ) == 0:
			node.value = data
		else:
			node.value = node.value + data
		return
# end of class: SimpleXMLHandler


class pyXmlParser:
	"""
	自己定制的非xml标准的xml文件解析器。
	在不需要效率的环境下，可以使用此解释器做对一些非标准的xml进行解析。
	注意：这是一个没有attr的解析版本，即本解析器不会分析附加属性，且如果有了附加属性，就有可能会出错。
	"""
	PARSER_STATE_CHARACTER_DATA		= 0x0001	# <xxx> ... </xxx>
	PARSER_STATE_START_ELEMENT		= 0x0002	# <xxx>
	PARSER_STATE_END_ELEMENT		= 0x0003	# </xxx>
	PARSER_STATE_COMMENT			= 0x0004	# <!-- ... -->
	PARSER_STATE_XML_HEAD			= 0x0005	# <? ... ?>
	PARSER_STATE_OTHER				= 0x0006	# <! ... >
	
	def __init__( self ):
		pass
	
	def parseFile( self, filename, handler ):
		"""
		"""
		f = open(filename, "rt")
		self.parseString(f.read(), handler)
		f.close()
	
	def parseString( self, srcStr, handler ):
		"""
		"""
		state = self.PARSER_STATE_CHARACTER_DATA
		#print "state =", state
		strData = ""
		handler.startDocument()
		#print "parser string:", srcStr
		col = 0
		strlen = len(srcStr)
		while col < strlen:	# 遍历每一个字符
			c = srcStr[col]
			#print "c =", c
			if state == self.PARSER_STATE_CHARACTER_DATA:		# <xxx> ... </xxx>
				if c == "<":
					if len(strData) > 0:
						handler.characters( strData )
						strData = ""
					
					if srcStr[col+1] == "/":	# </
						state = self.PARSER_STATE_END_ELEMENT
						col += 1
						#print "state =", state
					elif srcStr[col+1] == "?":	# <?
						state = self.PARSER_STATE_XML_HEAD
						col += 1
						#print "state =", state
					elif srcStr[col+1] == "!":
						if srcStr[col+2] == "-" and srcStr[col+3] == "-":	# <!--
							state = self.PARSER_STATE_COMMENT
							col += 3
							#print "state =", state
						else:
							state = self.PARSER_STATE_OTHER
							col += 1
							#print "state =", state
					else:
						state = self.PARSER_STATE_START_ELEMENT
						#print "state =", state
				elif c == ">":
					raise "I can't pase this line: %s" % srcStr
				else:
					strData += c
			elif state == self.PARSER_STATE_START_ELEMENT:			# <xxx>
				if c == "/" and srcStr[col+1] == ">":	# />
					handler.startElement( strData, AttributesImpl({}) )
					handler.endElement( strData )
					state = self.PARSER_STATE_CHARACTER_DATA
					strData = ""
					col += 1
					#print "state =", state
				elif c == ">":	# >
					handler.startElement( strData, AttributesImpl({}) )
					state = self.PARSER_STATE_CHARACTER_DATA
					strData = ""
					#print "state =", state
				elif c in ["\r\n"]:	# ignore chars
					pass
				elif c.isalnum() or c == "_" or c == ".":
					strData += c
				else:
					raise "I can't pase this line: %s" % srcStr
			elif state == self.PARSER_STATE_END_ELEMENT:				# </xxx>
				if c == ">":
					handler.endElement( strData )
					state = self.PARSER_STATE_CHARACTER_DATA
					strData = ""
					#print "state =", state
				elif c.isalnum() or c == "_" or c == ".":
					strData += c
				else:
					raise "I can't pase this line: %s" % srcStr
			elif state == self.PARSER_STATE_COMMENT:					# <!-- ... -->
				if c == ">" and col >= 2 and srcStr[col-1] == "-" and srcStr[col-2] == "-":
					state = self.PARSER_STATE_CHARACTER_DATA
					#print "state =", state
			elif state == self.PARSER_STATE_XML_HEAD:				# <? ... ?>
				if c == ">" and col >= 1 and srcStr[col-1] == "?":
					state = self.PARSER_STATE_CHARACTER_DATA
					#print "state =", state
			elif state == self.PARSER_STATE_OTHER:					# <! ... >
				if c == ">":
					state = self.PARSER_STATE_CHARACTER_DATA
					#print "state =", state
			else:
				pass
			# 最后字符位置 +1
			col += 1
		# end while
		handler.endDocument()
		return # the end

def parse( filename, parser = None ):
	"""
	open *.xml file to PyXMLSection
	
	@return: PyXMLSection
	"""
	p = SimpleXMLHandler()
	if parser:
		dstParser = parser().parseFile
	else:
		dstParser = sax.parse
	dstParser( filename, p )
	root = p.rootNode
	root.filename = filename
	return root

def parseString( string, parser = None ):
	"""
	parse xml string file to PyXMLSection
	
	@return: PyXMLSection
	"""
	p = SimpleXMLHandler()
	if parser:
		dstParser = parser().parseString
	else:
		dstParser = sax.parseString
	dstParser( string, p )
	root = p.rootNode
	root.filename = None
	return root

def saveTo( filename, source ):
	"""
	save instance of PyXMLSection to file.
	
	@param filename: xml file name and path
	@type  filename: string
	@param   source: instance of PyXMLSection
	@type    source: PyXMLSection
	@return: no
	"""
	f = open( filename, "w" )
	f.write( str(source) )
	f.close()
	return

