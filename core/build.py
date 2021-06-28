#!/usr/bin/env python3
import json

from pathlib import Path
from typing import Dict, List


class Build:
    def __init__(self, project_path_str: str) -> None:
        self._contracts: Dict = {}
        self._project_path: Path = Path(project_path_str).resolve()
        self._build_path: Path = self._project_path.joinpath("build")
        self._load()

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
        if contract_name in self._contracts and build_json["type"] == "interface":
            return
        if build_json["sourcePath"].startswith("interface"):
            # interfaces should generate artifact in /build/interfaces/ not /build/contracts/
            return
        self._contracts[contract_name] = build_json
        if "pcMap" not in build_json:
            # no pcMap means build artifact is for an interface
            return
        if "0" in build_json["pcMap"]:
            build_json["pcMap"] = dict((int(k), v) for k, v in build_json["pcMap"].items())

    def _remove_contract(self, contract_name: str) -> None:
        key = self._stem(contract_name)
        if key in self._contracts:
            del self._contracts[key]

    def get(self, contract_name: str) -> Dict:
        key = self._stem(contract_name)
        return self._contracts[key]

    def items(self) -> List:
        return list(self._contracts.items())

    def contains(self, contract_name: str) -> bool:
        return self._stem(contract_name) in list(self._contracts)

    def _stem(self, contract_name: str) -> str:
        return contract_name.replace(".json", "")
