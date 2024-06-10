"""Banco de Guayaquil's users microservice connection  """

from langchain.tools import BaseTool
from typing import Optional, Type
from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
import requests
from pydantic import BaseModel, Field

external_api = "https://mock-bg-api-1.onrender.com"

class CuentaInput(BaseModel):
    identificacion: str = Field(description="User ID for lookup their accounts")

class CuentasTool(BaseTool):
    name = "cuentas"
    description = " Useful for Retrieving account information for a user based on their identification."
    args_schema: Type[BaseModel] = CuentaInput

    def _run(self, identificacion: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        identificacion = identificacion.replace("-","")
        url = f"{external_api}/cuentas/{identificacion}"
        response = requests.get(url)
        if response.status_code == 200:
            return f"Accounts for ID {identificacion}: {response.json()}"
        else:
            return "No accounts found."

    async def _arun(self, identificacion: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("Asynchronous operation not supported.")

class ClienteInput(BaseModel):
    identificacion: str = Field(description="User ID for lookup users information")

class ClienteTool(BaseTool):
    name = "cliente"
    description = "Useful for Retrieving client information based on their identification."
    args_schema: Type[BaseModel] = ClienteInput

    def _run(self, identificacion: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        identificacion = identificacion.replace("-","")
        url = f"{external_api}/clientes/{identificacion}"
        response = requests.get(url)
        if response.status_code == 200:
            return f"Client data for ID {identificacion}: {response.json()}"
        else:
            return "Client not found."

    async def _arun(self, identificacion: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("Asynchronous operation not supported.")

class MovimientosInput(BaseModel):
    mtcuenta: int = Field(description="Account number to lookup movements")

class MovimientosTool(BaseTool):
    name = "movimientos"
    description = "Useful for Retrieving transaction movements for a specific account number."
    args_schema: Type[BaseModel] = MovimientosInput

    def _run(self, mtcuenta: int, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        url = f"{external_api}/movimientos/{mtcuenta}"
        response = requests.get(url)
        if response.status_code == 200:
            return f"Transactions for account {mtcuenta}: {response.json()}"
        else:
            return "No transactions found."

    async def _arun(self, mtcuenta: int, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("Asynchronous operation not supported.")

class TarjetasInput(BaseModel):
    identificacion: str = Field(description="User ID to retrieve cards information")
    ultimo_cuatro: Optional[str] = Field(default=None, description="Last for digits to lookup a specific card")

class TarjetasTool(BaseTool):
    name = "tarjetas"
    description = "Useful for Retrieving credit card information based on user identification and optionally card number."
    args_schema: Type[BaseModel] = TarjetasInput

    def _run(self, identificacion: str, ultimo_cuatro: Optional[str] = None, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        url = f"{external_api}/tarjetas/{identificacion}"
        if ultimo_cuatro:
            url += f"?ultimo_cuatro={ultimo_cuatro}"
        response = requests.get(url)
        if response.status_code == 200:
            return f"Cards for ID {identificacion}: {response.json()}"
        else:
            return "No cards found."

    async def _arun(self, identificacion: str, ultimo_cuatro: Optional[str] = None, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("Asynchronous operation not supported.")

class SegurosInput(BaseModel):
    identificacion: str = Field(description="Identificación del usuario para buscar seguros")

class SegurosTool(BaseTool):
    name = "seguros"
    description = "Useful for Retrieving insurance information based on user identification."
    args_schema: Type[BaseModel] = SegurosInput

    def _run(self, identificacion: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        url = f"{external_api}/seguros/{identificacion}"
        response = requests.get(url)
        if response.status_code == 200:
            return f"Insurances for ID {identificacion}: {response.json()}"
        else:
            return "No insurances found."

    async def _arun(self, identificacion: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("Asynchronous operation not supported.")
