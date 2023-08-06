import logging
from typing import List, Union, Dict, Optional
from uuid import UUID

from slapp_py.core_classes.division import Division
from slapp_py.helpers.dict_helper import first_key, deserialize_uuids_into_list, serialize_uuids


class DivisionsHandler:
    _divs: Dict[Division, List[UUID]]

    def __init__(self, divs: Optional[Dict[Division, List[UUID]]] = None):
        self._divs = divs or {}

    @property
    def count(self):
        return len(self._divs)

    @property
    def current_div(self):
        """Get the current div by getting the first key. Ideally, this is checked against the source..."""
        from slapp_py.core_classes import division
        return first_key(self._divs, division.Unknown)

    def add(self, incoming: Union[Division, List[Division]], sources: Union[UUID, List[UUID]]):
        if not incoming or not sources:
            return
        if not isinstance(incoming, list):
            incoming = [incoming]

        uuids = deserialize_uuids_into_list(sources)

        for to_add in incoming:
            if to_add.is_unknown:
                continue
            self._divs.setdefault(to_add, []).extend(uuids)

    def filter_to_source(self, source_id: Union[str, UUID]) -> 'DivisionsHandler':
        search_uuid = source_id if isinstance(source_id, UUID) else UUID(source_id)
        return DivisionsHandler(
            divs={k: v for k, v in self._divs if source_id in search_uuid}
        )

    def get_sources_for_division(self, div: Division) -> List[UUID]:
        """Gets UUIDs for the division, or empty if not found."""
        return self._divs.get(div, [])

    def get_sources_flat(self) -> List[UUID]:
        """Gets UUIDs contained in this information."""
        return list(set([result for sublist in self._divs.values() for result in sublist]))

    def get_divs_unordered(self):
        """Get the divisions without the sources."""
        return list(self._divs.keys())

    def get_divs_sourced(self) -> Dict[Division, List[UUID]]:
        """Get the divisions with sources."""
        return {k: v for k, v in self._divs.items()}

    @staticmethod
    def from_dict(obj: dict) -> 'DivisionsHandler':
        assert isinstance(obj, dict)
        try:
            val_dict = obj.get("D")
            result = DivisionsHandler()
            for key, value in val_dict.items():
                result.add(Division(key), value)
            return result
        except Exception as e:
            logging.exception(exc_info=e, msg=f"Exception occurred loading Divisions Handler: {e}, {e.args}")
            raise e

    def to_dict(self) -> dict:
        result = {}
        if len(self._divs) > 0:
            result["D"] = {k.__str__(): serialize_uuids(v) for k, v in self._divs.items()}
        return result

    def __str__(self):
        return f"{self.count} Divs{(f', current={self.current_div}' if self.count > 0 else '')}"
