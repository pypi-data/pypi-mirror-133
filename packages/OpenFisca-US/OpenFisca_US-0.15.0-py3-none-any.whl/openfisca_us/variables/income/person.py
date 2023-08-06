from openfisca_us.model_api import *


class net_income(Variable):
    value_type = float
    entity = Person
    label = "Net income"
    unit = "currency-USD"
    documentation = "Personal disposable income after taxes and transfers"
    definition_period = YEAR


class market_income(Variable):
    value_type = float
    entity = Person
    label = "Market income"
    unit = "currency-USD"
    documentation = "Income from all non-government sources"
    definition_period = YEAR
