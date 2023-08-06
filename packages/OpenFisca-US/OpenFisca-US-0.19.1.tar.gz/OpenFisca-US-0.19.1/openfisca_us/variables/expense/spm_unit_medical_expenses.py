from openfisca_us.model_api import *


class spm_unit_medical_expenses(Variable):
    value_type = float
    entity = SPMUnit
    label = u"SPM unit medical expenses"
    definition_period = YEAR
    unit = "currency-USD"
