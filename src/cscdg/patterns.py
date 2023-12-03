from re import Match, Pattern, compile, RegexFlag


def compile_with_flags(pattern: str) -> Pattern:
    return compile(
        pattern,
        RegexFlag.UNICODE | RegexFlag.DOTALL,
    )


def findall(pattern: Pattern, source: str) -> list[Match[str]]:
    return pattern.findall(source)


# name, body -> classes
namespace_pattern = compile_with_flags(r"namespace\s+([a-zA-Z0-9_.]+)\s*{(.*?)}$")

# annotation, name, _, relations,  body -> properties & methods
class_pattern = compile_with_flags(
    r"(class|interface|abstract\s+class|enum)\s+(\w+)(\s*:\s*(.*?))?\s*{(.*?)}$"
)

# visibility, is_delegate, modifier, return_type, _, name, generic, parameters, body -> has_body
method_pattern = compile_with_flags(
    r"(public|private|protected|internal)?\s*(delegate)?\s*(abstract|static|override|virtual|override\s+sealed|new)?"
    r"\s*(?!new)(?<=\W)([a-zA-Z0-9_]+(<[a-zA-Z0-9_, ]+>)?\??)\s+([a-zA-Z0-9_]+)\s*(<[a-zA-Z0-9_, ]+>)?"
    r"\s*\(([a-zA-Z0-9<,\s>?=_\[\]\'\"]*)\)\s*(where(.*?))?(\s*=>(.*?);|;|(\s*{(.*?)}))"
)

# visibility, static, type, _, name, body -> _
property_pattern = compile_with_flags(
    r"(public|private|protected|internal)?\s*(static)?\s*([a-zA-Z0-9_]+(<[a-zA-Z0-9_, ]+>)?\??)"
    r"\s+([a-zA-Z0-9_]+)\s*{\s*get\s*({(.*?)}|;)\s*set\s*({(.*?)}|;)\s*}"
)

#  modifier, type, name, default -> _
parameters_pattern = compile_with_flags(
    r"\s*(in|out|ref|ref readonly|params)?\s*([a-zA-Z0-9_]+(<[a-zA-Z0-9_<, >]+>|\[\d*\])?\??)"
    r"\s+([a-zA-Z0-9_]+)(\s*=\s*([a-zA-Z0-9_]+))?"
)


__all__ = (
    namespace_pattern,
    class_pattern,
    method_pattern,
    property_pattern,
    parameters_pattern,
    findall,
)
