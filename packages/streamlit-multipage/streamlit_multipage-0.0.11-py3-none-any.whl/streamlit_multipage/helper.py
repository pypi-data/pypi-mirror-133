from collections import defaultdict
from typing import List, Any, Dict
from pathlib import Path

import streamlit as st

try:
    import joblib

    pickling = joblib
except ImportError:
    import pickle

    pickling = pickle


path = Path(__file__).resolve().parent
cache = path / "cache"
cache_file = cache / "data.pkl"


def change_page(page: int) -> None:
    data = load()
    data["global"]["current_page"] = page
    
    _save(data, namespaces=data["namespaces"])


def read_page() -> int:
    data = load()["global"]

    if "current_page" in data:
        return int(data["current_page"])

    return 0


@st.cache(suppress_st_warning=True)
def initialize(initial_page: int) -> None:
    change_page(initial_page)


def _save(data: Dict[str, Any], namespaces) -> None:
    cache.mkdir(parents=True, exist_ok=True)

    temporary = {key:value for key, value in data.items() if key in namespaces}

    pickling.dump(temporary, cache_file)


def load() -> Dict[str, Any]:
    if not cache_file.exists():
        return defaultdict(dict)

    data = pickling.load(cache_file)
    data["global"] = {} 

    return data


def clear_cache(
    variables: Dict[str, Any] = None,
    namespaces: List[str] = None,
    all_variables: bool = False,
) -> None:
    if variables and namespaces:
        data = load()
        for namespace in namespaces:
            for variable in variables:
                print(variable, namespace)
                if variable not in data[namespace]:
                    continue

                del data[namespace][variable]

        _save(data)

    if all_variables:
        cache_file.unlink(missing_ok=True)


def save_state(namespace):
    def decorator(function):
        def wrapper(st):

            old_state = load()

            if "namespaces" not in old_state:
                old_state["namespaces"] = ["namespaces", "global", namespace]
            
            st.session_state.update(old_state)

            function(st)

            old_state = dict(st.session_state).copy()
            
            namespaces = old_state["namespaces"]
            
            function_state = {}

            for key, value in list(st.session_state.items()):
                if key in namespaces or "$$" in key:
                    continue
                
                del st.session_state[key]
                function_state[key] = value
            

            if namespace not in st.session_state:
                st.session_state[namespace] = {}
            
            st.session_state[namespace].update(function_state)
            
            _save(st.session_state, namespaces)

        return wrapper
    return decorator