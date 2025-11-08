from django import template

register = template.Library()

@register.filter(name='currency_cop')
def currency_cop(value):
    """
    Formatea un número como moneda colombiana (COP)
    Ejemplo: 4200000 -> $4.200.000
    """
    try:
        value = float(value)
        # Formatear con separadores de miles (punto en Colombia)
        formatted = f"{value:,.0f}".replace(',', '.')
        return f"${formatted}"
    except (ValueError, TypeError):
        return value

@register.filter(name='currency_cop_no_symbol')
def currency_cop_no_symbol(value):
    """
    Formatea un número como moneda colombiana sin el símbolo $
    Ejemplo: 4200000 -> 4.200.000
    """
    try:
        value = float(value)
        return f"{value:,.0f}".replace(',', '.')
    except (ValueError, TypeError):
        return value
