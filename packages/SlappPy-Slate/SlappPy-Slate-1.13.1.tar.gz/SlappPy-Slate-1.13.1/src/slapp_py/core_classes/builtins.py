from slapp_py.core_classes import source, name, team

UNKNOWN_PLAYER = "(Unnamed Player)"
"""Displayed string for an unknown player."""

UNKNOWN_TEAM = "(Unnamed Team)"
"""Displayed string for an unknown team."""

BuiltinSource = source.Source("builtin")
"""The built-in sources, for use in objects that are pre-defined by the program code."""

ManualSource = source.Source("Manual Entry")
"""The manual entry sources, for use in objects that are defined by manual user entry."""

UnknownPlayerName = name.Name(UNKNOWN_PLAYER, BuiltinSource.guid)
"""The Name for an unknown player."""

UnknownTeamName = name.Name(UNKNOWN_TEAM, BuiltinSource.guid)
"""The Name for an unknown team."""

NoTeam = team.Team(names=[name.Name("(Free Agent)", BuiltinSource.guid)])
UnknownTeam = team.Team(names=[UnknownTeamName])
