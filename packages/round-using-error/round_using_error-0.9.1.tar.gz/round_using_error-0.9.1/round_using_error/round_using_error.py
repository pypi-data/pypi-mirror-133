def rndwitherr(value, error, errdig=2):
    '''
    This is similar in functionality to the error rounding function of the package
    [sigfig](https://github.com/drakegroup/sigfig). The difference is that it also
    switches between decimal notaton and scientific point notation in a
    automatic manner.
    This is the author's personal opinion of when this switch is done by most students.
    Basically decimal notation is used for numbers in the range 0.1 to
    1000. Outside
    this range the number is provided in scientific notation.

    The `sigfig` package is not used to avoid doing the exponent analysis for the switch
    between decimal and scientific notation twice. This also avoids having
    to convert strings to numbers.

    :param float value: is the value to be rounded.
    :param float error: is the error in the value to be rounded.
    :param int errdig: (default = 2) number of significant figures to keep on the error.
        The value is rounded to the least significant digit in the error.

    :return string valuestr: rounded value.
    :return string errstr: rounded error.
    :return string pwroftenstr: string for scientific notation exponent. Empty string if
        values returned as decimals.
    '''
    import math
    pwroften = math.floor(math.log(value, 10))
    rndto = int(math.floor(math.log(error, 10) - errdig + 1))
    valscaled = value
    errscaled = error
    pwroftenstr = ''
    if (pwroften < -1) or (pwroften > 2):
        valscaled = value * 10 ** (-pwroften)
        errscaled = error * 10 ** (-pwroften)
        rndto = rndto - pwroften
        pwroftenstr = str(pwroften)
    valscaled = round(valscaled, -rndto)
    errscaled = round(errscaled, -rndto)
    precisstr = '%.' + str(-rndto) + 'f'
    valuestr = str(precisstr % valscaled)
    errorstr = str(precisstr % errscaled)
    return valuestr, errorstr, pwroftenstr


def output_rndwitherr(value, error, errdig=2, style='latex'):
    '''
    This method outputs the results of rndwitherr as a string.
    :param float value:
    :param float error:
    :param int errdig: default = 2
    :param string style: default = 'latex', alternative 'text'

    To view in Jupyter latex output in Jupyter use:
    ```
    from IPython.display import Math
    Math(latex_rndwitherr(value, error))
    ```
    '''
    if style not in ('latex', 'text'):
        raise ValueError('style parameter must be either "latex" or "string".')
    valstr, errstr, expstr = rndwitherr(value, error, errdig)
    pwrstr = ''
    lparen = ''
    rparen = ''
    if style == 'latex':
        pm = r'\pm'
    if style == 'text':
        pm = r' +/- '
    if expstr != '':
        lparen = '('
        rparen = ')'
        if style == 'latex':
            pwrstr = r'\times 10^' + expstr
        if style == 'text':
            pwrstr = r' X 10^' + expstr
    return str(r'' + lparen + valstr + pm + errstr + rparen + pwrstr)

def latex_rndwitherr(value, error, errdig=2):
    '''
    This is a convenience function to render the output of `rndwitherr()`
    as a latex string.
    :param float value:
    :param float error:
    :param int errdig:
    :return str: latex representation
    '''
    return output_rndwitherr(value, error, errdig, style='latex')

def text_rndwitherr(value, error, errdig=2):
    '''
    This is a convenience function to render the output of `rndwitherr()`
    as a text string.
    :param float value:
    :param float error:
    :param int errdig:
    :return: string representation
    '''
    return output_rndwitherr(value, error, errdig, style='text')