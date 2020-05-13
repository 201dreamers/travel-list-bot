from collections import namedtuple


TOKEN = '1189252346:AAF6RbynV1Xt0tTKbWwB4MAW5Fz3f5dytGI'
TIMEZONE = 'Europe/Kiev'
TIMEZONE_COMMON_NAME = 'Kiev'
COMMANDS_LIST = ('add', 'list', 'reset', 'help')
COMMANDS_DESCRIPTION = (
    {
        'name': 'add',
        'shortcut': 'a',
        'description': 'додати нове місце'
    },
    {
        'name': 'list',
        'shortcut': 'l',
        'description': 'показати 10 останніх місць'
    },
    {
        'name': 'reset',
        'shortcut': 'r',
        'description': 'видалити всі додані місця'
    },
    {
        'name': 'help',
        'shortcut': 'h',
        'description': 'показати доступні команди'
    }
)
Step = namedtuple('Step', 'OFF NAME LOCATION PHOTO COMMENT')
add_step = Step(
    OFF='-1',
    NAME='0',
    LOCATION='1',
    PHOTO='2',
    COMMENT='3'
)
