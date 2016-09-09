# Author: Dr. Ling Ma
# https://il.linkedin.com/in/cvlingma

entity_schema = {
    'TrimbleVersionID': {'type':'string'},
    'GlobalId': {'type':'string'},
    'IFCType': {'type':'string'},
    'Geometry': {
        'type': 'dict',
        'schema': {
            'Unit':{'type':'string'},
            'Faces': { 
                'type': 'list',
                'schema': {
                    'type':'list',
                    'schema':{
                        'type': 'integer'
                    }
                }
            },
            'Vertices': { 
                'type': 'list',
                'schema': {
                    'type':'list',
                    'schema':{
                        'type': 'number'
                    }
                }
            },
            'OCEBrep': {'type': 'string'}
        }
    },
}

entity_resource = {
    'item_title': 'Entity',
    'schema': entity_schema,
}