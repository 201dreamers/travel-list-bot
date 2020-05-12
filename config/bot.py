from collections import namedtuple


TOKEN = '1170050633:AAF-DR1fDX6TyDPUDZOOs5P1xPlQ0l-lt2Y'
TIMEZONE = 'Europe/Kiev'
TIMEZONE_COMMON_NAME = 'Kiev'
COMMANDS_LIST = ('add', 'list', 'reset', 'help')
COMMANDS_DESCRIPTION = (
    {
        'name': 'add',
        'shortcut': 'a',
        'description': 'додати нову локацію'
    },
    {
        'name': 'list',
        'shortcut': 'l',
        'description': 'показати 10 останніх збережених локацій'
    },
    {
        'name': 'reset',
        'shortcut': 'r',
        'description': 'видалити всі додані локації'
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
