using UnityEngine;
using System.IO;
using System.Collections;
using System.Collections.Generic;

/*
write by penghuawei in 2014-09-18
simple read and write tab table file like to ResMgr.pyDataSection of BigWorld.

use example：
TabTableSection tableSection = TabTableLoader.parse( "config/xxx.txt" );
foreach ( TabTableSection section in tableSection.values() )
{
	Debug.Log( this + ":: - " + section.readInt( "ID" ) );
	Debug.Log( this + ":: - " + section.readInt( "HandleID" ) );
	Debug.Log( this + ":: - " + section.readString( "Name" ) );
	Debug.Log( this + ":: - " + section.readIntArray( "EffectID" ) );
}
*/

namespace DataSection
{
	public class TabTableSection : SectionNode<TabTableSection>
	{
		private string filename_ = "";

		public TabTableSection() : base( "", "", null ) {}
		public TabTableSection( string name ) : base( name, "", null ) {}
		public TabTableSection( string name, string value ) : base( name, value, null ) {}
		public TabTableSection( string name, string value, TabTableSection parent ) : base( name, value, parent ) {}

		public string filename
		{
			get {
				return filename_;
			}
			set {
				filename_ = value;
			}
		}

	}

	public class TabTableLoader
	{
		public static TabTableSection loadFile( string file )
		{
			return loadString( Resources.Load( file ).ToString() );
		}
		
		public static TabTableSection loadString(string str)
		{
			return Parse (new StringReader (str));
		}

		public static TabTableSection Parse (TextReader input)
		{
			_TabTableHead tableHead = new _TabTableHead();

			string head = input.ReadLine();
			tableHead.initHeads( head );

			string typeDef = input.ReadLine();
			tableHead.initTypeDef( typeDef );

			string defaultValue = input.ReadLine();
			tableHead.initDefaultValues( defaultValue );

			TabTableSection root = new TabTableSection("root");
			_TabTableRow tableRow = new _TabTableRow( tableHead );

			while (true)
			{
				string row = input.ReadLine();
				if (row == null)
					break;

				if (row.Length > 0)
				{
					tableRow.read ( row );
					tableRow.convertToSection( root );
				}
			}


			return root;
		}
	}

	class _TabTableHead
	{
		public static string[] SEPARATOR = new string[1] { "\t", };

		List<string> m_heads = new List<string>();
		Dictionary<string, int> m_head2index = new Dictionary<string, int>();

		List<string> m_defaultValues = new List<string>();

		public _TabTableHead(){}

		public static bool splitField(string line, List<string> fieldValues, Dictionary<string, int> fieldValue2index)
		{
			string[] valueSplits = line.Split(SEPARATOR, System.StringSplitOptions.None);
			int index = 0;
			foreach (string h in valueSplits)
			{
				fieldValues.Add( h );

				if (fieldValue2index !=null)
					fieldValue2index[h] = index;
				index++;
			}
			return true;
		}

		public bool initHeads(string input)
		{
			return splitField( input, m_heads, m_head2index );
		}

		public bool initTypeDef(string input)
		{
			// do something here...
			return true;
		}

		public bool initDefaultValues(string input)
		{
			return splitField( input, m_defaultValues, null );
		}

		public int name2Index( string fieldName )
		{
			int result;
			if (m_head2index.TryGetValue( fieldName, out result ))
				return result;
			return -1;
		}

		public string index2Name( int index )
		{
			return m_heads[index];
		}

		public string getDefaultValue( int index )
		{
			return m_defaultValues[index];
		}
	}

	class _TabTableRow
	{
		_TabTableHead m_tableHead;
		List<string> m_values = new List<string>();

		public _TabTableRow( _TabTableHead head )
		{
			m_tableHead = head;
		}

		public bool read( string line )
		{
			m_values.Clear();
			return _TabTableHead.splitField( line, m_values, null );
		}

		public void convertToSection( TabTableSection root )
		{
			TabTableSection subRoot = root.createSection( "item" );
			int index = 0;
			foreach (string value in m_values)
			{
				string key = m_tableHead.index2Name( index );
				string val = value.Length > 0 ? value : m_tableHead.getDefaultValue( index );
				index++;
				TabTableSection section = subRoot.createSection( key );
				section.value = val;
			}
		}
	}
}
