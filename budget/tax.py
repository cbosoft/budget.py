class TaxBands:

    def __init__(self, bands, rates):
        self.bands_and_rates = [tuple(a) for a in zip(bands, rates)]

    def get_after_tax(self, income):
        tax = 0.0
        for (tax_from, __), (tax_up_to, rate) in zip(self.bands_and_rates, self.bands_and_rates[1:]):
            if income > tax_from:
                taxable = tax_up_to - tax_from if income > tax_up_to else income - tax_from
                tax += rate*taxable
            else:
                break
        return income - tax


# https://www.gov.uk/income-tax-rates
_english_tax_bands = TaxBands(
        bands=[12500, 50000, 150000, float('inf')], # upper limits for the rates given
        rates=[0.0, 0.20, 0.40, 0.45])

# https://www.gov.uk/scottish-income-tax
_scottish_tax_bands = TaxBands(
        bands=[12500, 14585, 25158, 43430, 150000, float('inf')], # upper limits for the rates given
        rates=[0.0, 0.19, 0.20, 0.21, 0.41, 0.46])

def after_tax(income, band='scotland'):

    assert isinstance(band, (str, TaxBands))

    band_obj = band
    if isinstance(band, str):
        if band == 'scotland':
            band_obj = _scottish_tax_bands
        elif band == 'england':
            band_obj = _scottish_tax_bands  # lol why bother?
        else:
            raise Exception(f'Unrecognised band id {band}.')

    return band_obj.get_after_tax(income)
