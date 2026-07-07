from dataclasses import dataclass
from typing import Any
import yaml

class configError(Exception):
    pass
@dataclass
class leetCodeConfig:
    session : str
@dataclass
class gitConfig:
    repo : str
    localpath : str
@dataclass
class layoutConfig:
    baseDir : str
@dataclass
class retryConfig:
    maxAttempt : int
@dataclass
class config:
    leetCode : leetCodeConfig
    github : gitConfig
    layout : layoutConfig
    retry : retryConfig

def _get(data : dict[str, Any], section: str, key : str, expType : type):
    if section not in data : raise configError
    if not isinstance(data[section], dict): raise configError
    if key not in data[section] : raise configError
    val = data[section][key]
    if expType is int :
        if not isinstance(val, int) or isinstance(val, bool) :
            raise configError
    elif not isinstance(val, expType) :
        raise configError
    return val

def loadConfig(path : str) -> config: 
    # validate the config 
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError as e:
        raise configError from e
    except yaml.YAMLError as e:
        raise configError from e
    if not isinstance(data, dict):
        raise configError

    return config(
        leetCode=leetCodeConfig(
            session=_get(data, "leetcode", "session", str),
        ),
        github=gitConfig(
            repo=_get(data, "github", "repository", str),
            localpath=_get(data, "github", "local_path", str),
        ),
        layout=layoutConfig(
            baseDir=_get(data, "layout", "base_directory", str),
        ),
        retry=retryConfig(
            maxAttempt=_get(data, "retry", "max_attempts", int),
        ),
    )