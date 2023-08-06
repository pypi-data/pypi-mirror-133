﻿# Tuxpy

Tuxpy is an API. It is developed to run processes located in Tuxdb with Python Programming Language.

**Install:** `$ pip install tuxpy`

# API

Tuxpy contains 3 modules. These are client, database and collection.

 1. **client**

	**Import Notation:** `import tuxpy.client` 

	 - `class tuxpy.client.Client(host="127.0.0.1", port=6060)`
	 
		It's a constructor method that connects to the Tuxdb. 
		
          | parameters | description |
          |--|--|
          | host: str | This parameter specifies which host address to connect to. Also host parameter must be the same value as tuxdb's server host value. It is set "127.0.0.1" by default.  |
          |	port: int	|  this parameter must be the same value as tuxdb's server port value. It is set 6060 by default. |

		**Client Class Member Functions**

		- `getDatabase(databaseName: str) -> tuxpy.database.Database`
		
			This function returns a database object contained in Tuxdb. If there is no database associated with the databaseName parameter, the function creates a new database with the name specified by the databaseName parameter.
			
          | parameters | description  |
          |--|--|
          | databaseName: str | The name of the database to be accessed. |

		- `getDatabaseNames() -> list`

			This function returns a list of all database names contained in the Tuxdb.
	
2. **database**

	**Import Notation:** `import tuxpy.database` 

	- `class tuxpy.database.Database(client: tuxpy.client.Client, databaseName: str)`

		This is a constructor method that returns a database object if there is database associated with the name specified by databaseName parameter. If there is no database, the constructor method creates a database with the name specified by databaseName parameter and then returns a database object.
		
      | parameters | description |
      |--|--|
      | client: tuxpy.client.Client | It's a Client object connected to the Tuxdb. |
      |	databaseName: str | The name of the database to be accessed. |

		**Database Class Member Functions**

		 - `getCollection(collectionName: str) -> tuxpy.collection.Collection`

			This function returns a collection object found in the currently used database. If there is no collection associated with the collectionName parameter, the function creates a new collection for the used database with the name specified by the collectionName parameter.
	
            | parameters | description |
            |--|--|
            | collectionName: str | The name of the collection in the used database. |
		- `getCollectionNames() -> list`

			This function returns a list of all collections found in the currently used database. 

		- `setDatabaseName(newDatabaseName: str) -> dict`

			This function sets the name of used database. Returns a dict that indicates whether the result of the function was successful.

			
           | parameters | description |
           |--|--|
           | newDatabaseName: str | The new database name instead of the current name of the used database.|


		- `drop() -> dict`

			This function delete the used database from Tuxdb. Returns a dict that indicates whether the result of the function was successful

3. **collection**

	**Import Notation:** `import tuxpy.collection` 

	- `class tuxpy.collection.Collection(client: tuxpy.client.Client, databaseName: str, collectionName: str)`

		This constructor method returns a collection object found in the database. If there is no collection associated with the collectionName parameter, the function creates a new collection for the database with the name specified by the collectionName parameter.

	
       | parameters | description |
       |--|--|
       | client: tuxpy.client.Client | It's a Client object connected to the Tuxdb |
	   | databaseName: str | The name of the database to be accessed. |
	   | collectionName: str | The name of the collection in database to be accessed in the database. |

		**Client Class Member Functions**

		- `setCollectionName(newCollectionName: str) -> dict`

			This function sets the name of used collection. Returns a dict that indicates whether the result of the function was successful.

		
             | parameters | description |
             |--|--|
             | newCollectionName: str | The new collection name instead of the current name of the used collection. |

		- `getAllObjects() -> list`
			
			Returns a list of all objects found in the used collection.

		- `findFromObjectId(objectId: str) -> dict`

			This function returns a dict of the object content found in the used collection. 

		
            | parameters | description |
            |--|--|
            | objectId: str | The ID of object. |
        - `findOne(query: dict) -> dict`

			This function returns a dict of an object associated the the query.

			
            | parameters  | description |
            |--|--|
            | query: dict | The query to catch the object |


		- `find(query: dict) -> list`

			This function returns a list of the objects associated with the query.

           | parameters | description |
           |--|--|
           | query: dict | The query to catch the objects. |

		 - `insert(data: dict) -> dict`

			This function creates a new object into used collection. Returns a dict that indicates whether the result of the function was successful.

           | parameters | description |
           |--|--|
           | data: dict | Content of  new object |

		- `updateFromObjectId(objectId: str, updateData: dict) -> dict`

			This function updates a object content associated with the objectId. Returns a dict that indicates whether the result of the function was successful.
			
           | parameters | description |
           |--|--|
           | objectId: str | The ID of object. |
           | updateData: dict | It contains the names of the elements to be changed and their new values. |

		- `update(query: dict, updateData: dict) -> dict`

			This function updates the objects content associated with the query. Returns a dict that indicates whether the result of the function was successful.

           | parameters | description |
           |--|--|
           | query: dict | The query to catch the objects. |
           | updateData: dict | It contains the names of the elements to be changed and their new values. |

		- `deleteFromObjectId(objectId: str) -> dict`

			This object deletes a object associated with the objectId. Returns a dict that indicates whether the result of the function was successful.

          | parameters | description |
          |--|--|
          | objectId: str | The ID of object. |

		- `delete(query: dict) -> dict`

			This object deletes the objects associated with the query. Returns a dict that indicates whether the result of the function was successful.

          | parameters | description |
          |--|--|
          | query: dict | The query to catch the objects. |

		- `drop() -> dict`
		
			This function deletes the used collection. Returns a dict that indicates whether the result of the function was successful.





			
