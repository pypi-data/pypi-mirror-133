from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.language import Language
from ..models.localizable_param import LocalizableParam

T = TypeVar("T", bound="Hsm")


@attr.s(auto_attribs=True)
class Hsm:
    """The containing element for the message content — Indicates that the message is highly structured. Parameters
    contained within provide the structure.

        Example:
            {'element_name': 'hello_world', 'language': {'code': 'en', 'policy': 'deterministic'}, 'localizable_params':
                [{'default': '1234'}], 'namespace': 'business_a_namespace'}

        Attributes:
            element_name (str): The element name that indicates which template to use within the namespace
            language (Language):  Example: {'code': 'en', 'policy': 'deterministic'}.
            localizable_params (List[LocalizableParam]): This field is an array of values to apply to variables in the
                template
            namespace (str): The namespace that will be used
    """

    element_name: str
    language: Language
    localizable_params: List[LocalizableParam]
    namespace: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        element_name = self.element_name
        language = self.language.to_dict()

        localizable_params = []
        for localizable_params_item_data in self.localizable_params:
            localizable_params_item = localizable_params_item_data.to_dict()

            localizable_params.append(localizable_params_item)

        namespace = self.namespace

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "element_name": element_name,
                "language": language,
                "localizable_params": localizable_params,
                "namespace": namespace,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        element_name = d.pop("element_name")

        language = Language.from_dict(d.pop("language"))

        localizable_params = []
        _localizable_params = d.pop("localizable_params")
        for localizable_params_item_data in _localizable_params:
            localizable_params_item = LocalizableParam.from_dict(localizable_params_item_data)

            localizable_params.append(localizable_params_item)

        namespace = d.pop("namespace")

        hsm = cls(
            element_name=element_name,
            language=language,
            localizable_params=localizable_params,
            namespace=namespace,
        )

        hsm.additional_properties = d
        return hsm

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
