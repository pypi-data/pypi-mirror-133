import xmltodict

from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from json import dumps

from easyDataverse.core.uploader import uploadToDataverse
from easyDataverse.core.dataverseBase import DataverseBase


class Dataset(BaseModel):

    metadatablocks: Dict[str, Any] = dict()
    p_id: Optional[str] = None

    def add_metadatablock(
        self,
        metadatablock: DataverseBase
    ) -> None:
        """Adds a metadatablock object to the dataset if it is of 'DataverseBase' type and has a metadatablock name"""

        # Check if the metadatablock is of 'DataverseBase' type
        if issubclass(metadatablock.__class__, DataverseBase) is False:
            raise TypeError(
                f"Expected class of type 'DataverseBase', got '{metadatablock.__class__.__name__}'"
            )

        if hasattr(metadatablock, '_metadatablock_name') is False:
            raise TypeError(
                f"The provided class {metadatablock.__class__.__name__} has no metadatablock name and is thus not compatible with this function."
            )

        # Add the metadatablock to the dataset as a dict
        self.metadatablocks.update(
            {getattr(metadatablock, "_metadatablock_name"): metadatablock}
        )

    def xml(self) -> str:
        """Returns an XML representation of the dataverse object."""

        # Turn all keys to be camelcase
        fields = self._keys_to_camel(
            {"dataset_version": self.dict()}
        )

        return xmltodict.unparse(
            fields,
            pretty=True, indent="    "
        )

    def _keys_to_camel(self, dictionary: dict):
        nu_dict = {}
        for key in dictionary.keys():
            if isinstance(dictionary[key], dict):
                nu_dict[
                    self._snake_to_camel(key)
                ] = self._keys_to_camel(dictionary[key])
            else:
                nu_dict[
                    self._snake_to_camel(key)
                ] = dictionary[key]
        return nu_dict

    @staticmethod
    def _snake_to_camel(word: str) -> str:
        return ''.join(x.capitalize() or '_' for x in word.split('_'))

    def dataverse_json(self, indent: int = 2) -> str:
        """Returns a JSON representation of the dataverse dataset."""

        # Convert all blocks to the appropriate format
        blocks = {}
        for block in self.metadatablocks.values():
            blocks.update(block.dataverse_dict())

        return dumps(
            {
                "datasetVersion": {
                    "metadataBlocks": blocks
                }
            },
            indent=indent
        )

    def upload(self, dataverse_name: str, filenames: List[str] = None) -> str:
        """Uploads the given dataset to the Dataverse installation."""

        return uploadToDataverse(
            json_data=self.dataverse_json(),
            dataverse_name=dataverse_name,
            filenames=filenames
        )
