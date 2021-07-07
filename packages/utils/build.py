import json

from pathlib import Path
from typing import Dict, List


class Build:
    def __init__(self, project_path_str: str) -> None:
        self._contracts: Dict = {}
        self._project_path: Path = Path(project_path_str).resolve()
        self._build_path: Path = self._project_path.joinpath("build")
        self._load()

    def __getitem__(self, contract_name: str) -> Dict:
        return self._contracts[contract_name]

    def _load(self) -> None:
        for path in list(self._build_path.glob("contracts/*.json")):
            try:
                with path.open() as fp:
                    build_json = json.load(fp)
            except json.JSONDecodeError:
                build_json = {}
            if not self._project_path.joinpath(build_json["sourcePath"]).exists():
                path.unlink()
                continue
            self._add_contract(build_json)

    def _add_contract(self, build_json: Dict, alias: str = None) -> None:
        contract_name = alias or build_json["contractName"]
        if build_json["sourcePath"].startswith("interface"):
            # interfaces should generate artifact in /build/interfaces/ not /build/contracts/
            return
        self._contracts[contract_name] = build_json

    def items(self) -> List:
        return list(self._contracts.items())

    def contains(self, contract_name: str) -> bool:
        return contract_name in list(self._contracts)

