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
		public enum eStatus
		{
			ReadHead = 0,
			ReadType = 1,
			ReadDefault = 2,
			ReadBody = 3,
		};

		public static TabTableSection loadFile( string file )
		{
			//Debug.Log( string.Format( "TabTableLoader::loadFile(), {0}", file ) );
			return loadString( Resources.Load( file ).ToString() );
		}
		
		public static TabTableSection loadString(string str)
		{
			return Parse (new StringReader (str));
		}

		public static TabTableSection Parse (TextReader input)
		{
			_TabTableHead tableHead = new _TabTableHead();

			TabTableSection root = new TabTableSection("root");
			_TabTableRow tableRow = new _TabTableRow( tableHead );

			eStatus state = eStatus.ReadHead;

			while (true)
			{
				string row = input.ReadLine();

				if (row == null)
					break;

				if (row.Trim().Length == 0)
					continue;

				char c = row[0];
				if (c == '#' || c == ';')
					continue;  // ignore comment

				switch (state)
				{
				case eStatus.ReadHead:
					tableHead.initHeads( row );
					state = eStatus.ReadType;
					break;

				case eStatus.ReadType:
					tableHead.initTypeDef( row );
					state = eStatus.ReadDefault;
					break;

				case eStatus.ReadDefault:
					tableHead.initDefaultValues( row );
					state = eStatus.ReadBody;
					break;

				case eStatus.ReadBody:
					tableRow.read ( row );
					tableRow.convertToSection( root );
					break;

				default:
					break;
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

		public static bool splitField(string line, List<string> fieldValues, Dictionary<string, int> fieldValue2index, bool stopIfEmpty)
		{
			string[] valueSplits = line.Split(SEPARATOR, System.StringSplitOptions.None);
			int index = 0;
			foreach (string h in valueSplits)
			{
				if (stopIfEmpty && h.Trim().Length == 0)
				{
					//Debug.LogError( string.Format( "_TabTableHead::splitField(), stop field on '{0}'", fieldValues[index - 1] ) );
					return true;
				}

				fieldValues.Add( h );

				if (fieldValue2index != null)
					fieldValue2index[h] = index;
				index++;
			}
			return true;
		}

		public List<string> heads
		{
			get { return m_heads; }
		}

		public bool initHeads(string input)
		{
			return splitField( input, m_heads, m_head2index, true );
		}

		public bool initTypeDef(string input)
		{
			// do something here...
			return true;
		}

		public bool initDefaultValues(string input)
		{
			if (!splitField( input, m_defaultValues, null, false ))
				return false;
			if (m_defaultValues.Count > m_heads.Count)
				m_defaultValues.RemoveRange(m_heads.Count, m_defaultValues.Count - m_heads.Count);
			else if (m_defaultValues.Count < m_heads.Count)
				return false;
			return true;
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
			return _TabTableHead.splitField( line, m_values, null, false );
		}

		public void convertToSection( TabTableSection root )
		{
			TabTableSection subRoot = root.createSection( "item" );
			int index = 0;
			foreach (string key in m_tableHead.heads)
			{
				string val = m_values[index].Length > 0 ? m_values[index] : m_tableHead.getDefaultValue( index );
				index++;
				TabTableSection section = subRoot.createSection( key );
				section.value = val;
			}
		}
	}
}
