from dataclasses import dataclass
from typing import Set, Dict, List


@dataclass
class URLInfo:
    full_url: str
    domain: str
    emails: Set[str]
    links: Set[str]
    is_valid: bool = True

    def __hash__(self):
        return hash(self.full_url)

    def __eq__(self, other):
        if isinstance(other, URLInfo):
            return self.full_url == other.full_url
        if isinstance(other, str):
            return self.full_url == other

    def get_node_to_edge_list_dict_repr(self) -> Dict[str, List[str]]:
        return {self.full_url: list(self.links)}

    def get_node_to_attributes_dict_repr(self) -> Dict[str, List[str]]:
        return {self.full_url: {'emails': list(self.emails), 'domain': self.domain}}
