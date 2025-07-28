from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class BensDividasLink(SQLModel, table=True):
    __tablename__ = "bensdividaslink"

    bens_id: Optional[int] = Field(default=None, foreign_key="bensedireitos.id", primary_key=True)
    divida_id: Optional[int] = Field(default=None, foreign_key="dividaseonus.id", primary_key=True)

class BensEDireitos(SQLModel, table=True):
    __tablename__ = "bensedireitos"

    id: Optional[int] = Field(default=None, primary_key=True)
    ano_calendario: int = Field(index=True)
    rendimentos_tributaveis: float
    rendimentos_isentos: float
    deducoes_previdenciarias_totais: float
    imposto_devido: float
    bens_e_direitos: float

    capital_estado_id: Optional[int] = Field(default=None, foreign_key="capitalestadoresidencialdeclarante.id")
    capital: Optional["CapitalEstadoResidencialDeclarante"] = Relationship(back_populates="bens")

    dividas: List["DividasEOnus"] = Relationship(
        back_populates="bens",
        link_model=BensDividasLink
    )

class FaixaBaseCalculoAnual(SQLModel, table=True):
    __tablename__ = "faixabasecalculoanual"

    id: Optional[int] = Field(default=None, primary_key=True)
    ano_calendario: int = Field(index=True)
    tipo_declaracao: str
    faixa_rendimento: str
    quantidade_declaraveis: int
    rendimentos_tributaveis: float
    rendimentos_isentos: float

    rendimentos_isentos_id: Optional[int] = Field(default=None, foreign_key="rendimentosisentosnaotributaveis.id")

class RendimentosIsentosNaoTributaveis(SQLModel, table=True):
    __tablename__ = "rendimentosisentosnaotributaveis"

    id: Optional[int] = Field(default=None, primary_key=True)
    ano_calendario: int = Field(index=True)
    faixa_salarios_minimos: str
    bolsas_estudo_pesquisa: float
    indenizacoes_trabalho_fgts: float
    ganho_capital_imoveis: float
    lucros_dividendos_recebidos: float
    aposentadoria_pensionistas_65_anos: float
    transferencias_patrimoniais: float

class CapitalEstadoResidencialDeclarante(SQLModel, table=True):
    __tablename__ = "capitalestadoresidencialdeclarante"

    id: Optional[int]  = Field(default=None, primary_key=True)
    ano_calendario: int = Field(index=True)
    capital_estado: str
    quantidade_declarantes: int
    rendimentos_tributaveis: float
    rendimentos_isentos: float
    imposto_devido: float
    imposto_pago: float
    bens_e_direitos: float

    bens: List[BensEDireitos] = Relationship(back_populates="capital")

class DividasEOnus(SQLModel, table=True):
    __tablename__ = "dividaseonus"

    id: Optional[int] = Field(default=None, primary_key=True)
    ano_calendario: int = Field(index=True)
    emprestimos_exterior: float
    estabelecimento_bancario_comercial: float
    outras_dividas_onus_reais: float
    outras_pessoas_juridicas: float
    pessoas_fisicas: float
    sociedade_credito_financeiro_investimento: float    
    outros: float

    bens: List[BensEDireitos] = Relationship(
        back_populates="dividas",
        link_model=BensDividasLink
    )
