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

scanner_schema = {
    'TrimbleVersionID': {'type':'string'},
    'CS_X': {
        'type':'list',
        'schema':{
            'type': 'number'
        }
    },
    'CS_Y': { # Up direction
        'type':'list',
        'schema':{
            'type': 'number'
        }
    },
    'CS_Z': { # camera/look at direction
        'type':'list',
        'schema':{
            'type': 'number'
        }
    },
    'CS_Origin': { # camera position
        'type':'list',
        'schema':{
            'type': 'number'
        }
    },
    'Resolution': {'type': 'number'}
}

scanner_resource = {
    'item_title': 'Scanner',
    'schema': scanner_schema,
    'extra_response_fields':[
        'TrimbleVersionID',
        'CS_X',
        'CS_Y',
        'CS_Z',
        'CS_Origin',
        'Resolution'
        ]
}