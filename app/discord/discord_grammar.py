from pyparsing import alphanums, nums, Word, printables, Combine, Literal, Regex, Optional

_String = Word(printables)

# .steal <a:AScuteNOM:515426299628617728> cute
# .steal <:ShinSmile:498097611450875905> smile
_Emoji = Combine(
    Literal('<') +
    Optional(Word(alphanums, exact=1)) +
    Literal(':') +
    Word(alphanums) +
    Literal(':') +
    Word(nums) +
    Literal('>')
)

_RestOfInput = Regex(r'.*')
_Commands = Literal('help') | Literal('ping') | Literal('pong') | Literal('steal') | Literal('mmr') | Literal('avatar')

_help = Literal('.help')
_help_advanced = Literal('.help') + Optional('.').suppress() + _Commands
_ping = Literal('.ping')
_pong = Literal('.pong')
_steal = Literal('.steal') + _String + _String
_mmr = Literal('.mmr') + _String + _RestOfInput
_avatar = Literal('.avatar') + _RestOfInput

grammar = _help_advanced \
          | _help \
          | _ping \
          | _pong \
          | _steal \
          | _mmr \
          | _avatar
