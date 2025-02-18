#!/usr/bin/python3

from modularcalculator.features.structure.functions import *
from modularcalculator.features.feature import Feature
from modularcalculator.objects.exceptions import *
from modularcalculator.objects.number import *

from functools import partial
import scipy.special
import random
import numpy
import warnings


class SpecialFunctionsFeature(Feature):

    def id():
        return 'numerical.specialfunctions'

    def category():
        return 'Numerical'

    def title():
        return 'Special Functions'

    def desc():
        return 'Special functions'

    def dependencies():
        return ['structure.functions']

    @classmethod
    def install(cls, calculator):
        af = partial(SpecialFunctionsFeature.add_func, calculator)

        # Needed to avoid warning: "ComplexWarning: Casting complex values to real discards the imaginary part"
        warnings.simplefilter("ignore", numpy.exceptions.ComplexWarning)

        af('airy', "Airy functions - Airy functions and their derivatives", ['z'], ['Ai', 'Aip', 'Bi', 'Bip'])
        af('airye', "Airy functions - Exponentially scaled Airy functions and their derivatives", ['z'], ['eAi', 'eAip', 'eBi', 'eBip'])
        af('itairy', "Airy functions - Integrals of Airy functions", ['x'], ['Apt', 'Bpt', 'Ant', 'Bnt'])

        af('ellipj', "Elliptic functions and integrals - Jacobian elliptic functions", ['u', 'm'], ['sn', 'cn', 'dn', 'ph'])
        af('ellipk', "Elliptic functions and integrals - Complete elliptic integral of the first kind", ['m'])
        af('ellipkm1', "Elliptic functions and integrals - Complete elliptic integral of the first kind around m = 1", ['p'])
        af('ellipkinc', "Elliptic functions and integrals - Incomplete elliptic integral of the first kind", ['phi', 'm'])
        af('ellipe', "Elliptic functions and integrals - Complete elliptic integral of the second kind", ['m'])
        af('ellipeinc', "Elliptic functions and integrals - Incomplete elliptic integral of the second kind", ['phi', 'm'])
        af('elliprc', "Elliptic functions and integrals - Degenerate symmetric elliptic integral", ['x', 'y'])
        af('elliprd', "Elliptic functions and integrals - Symmetric elliptic integral of the second kind", ['x', 'y', 'z'])
        af('elliprf', "Elliptic functions and integrals - Completely-symmetric elliptic integral of the first kind", ['x', 'y', 'z'])
        af('elliprg', "Elliptic functions and integrals - Completely-symmetric elliptic integral of the second kind", ['x', 'y', 'z'])
        af('elliprj', "Elliptic functions and integrals - Symmetric elliptic integral of the third kind", ['x', 'y', 'z', 'p'])

        af('jv', "Bessel functions - Bessel function of the first kind of real order and complex argument", ['v', 'z'])
        af('jve', "Bessel functions - Exponentially scaled Bessel function of the first kind of order v", ['v', 'z'])
        af('yn', "Bessel functions - Bessel function of the second kind of integer order and real argument", ['n', 'x'])
        af('yv', "Bessel functions - Bessel function of the second kind of real order and complex argument", ['v', 'z'])
        af('yve', "Bessel functions - Exponentially scaled Bessel function of the second kind of real order", ['v', 'z'])
        af('kn', "Bessel functions - Modified Bessel function of the second kind of integer order n", ['n', 'x'], func=SpecialFunctionsFeature.func_int_params)
        af('kv', "Bessel functions - Modified Bessel function of the second kind of real order v", ['v', 'z'])
        af('kve', "Bessel functions - Exponentially scaled modified Bessel function of the second kind", ['v', 'z'])
        af('iv', "Bessel functions - Modified Bessel function of the first kind of real order", ['v', 'z'])
        af('ive', "Bessel functions - Exponentially scaled modified Bessel function of the first kind", ['v', 'z'])
        af('hankel1', "Bessel functions - Hankel function of the first kind", ['v', 'z'])
        af('hankel1e', "Bessel functions - Exponentially scaled Hankel function of the first kind", ['v', 'z'])
        af('hankel2', "Bessel functions - Hankel function of the second kind", ['v', 'z'])
        af('hankel2e', "Bessel functions - Exponentially scaled Hankel function of the second kind", ['v', 'z'])
        af('wright_bessel', "Bessel functions - Wright's generalized Bessel function", ['a', 'b', 'x'])

        af('itj0y0', "Integrals of Bessel functions - Integrals of Bessel functions of the first kind of order 0", ['x'], ['ij0', 'iy0'])
        af('it2j0y0', "Integrals of Bessel functions - Integrals related to Bessel functions of the first kind of order 0", ['x'], ['ij0', 'iy0'])
        af('iti0k0', "Integrals of Bessel functions - Integrals of modified Bessel functions of order 0", ['x'], ['ii0', 'ik0'])
        af('it2i0k0', "Integrals of Bessel functions - Integrals related to modified Bessel functions of order 0", ['x'], ['ii0', 'ik0'])
        af('besselpoly', "Integrals of Bessel functions - Weighted integral of the Bessel function of the first kind", ['a', 'lmb', 'nu'])

        af('jvp', "Derivatives of Bessel functions - Compute derivatives of Bessel functions of the first kind", ['v', 'z'])
        af('yvp', "Derivatives of Bessel functions - Compute derivatives of Bessel functions of the second kind", ['v', 'z'])
        af('ivp', "Derivatives of Bessel functions - Compute derivatives of modified Bessel functions of the first kind", ['v', 'z'])
        af('h1vp', "Derivatives of Bessel functions - Compute derivatives of Hankel function H1v(z) with respect to z", ['v', 'z'])
        af('h2vp', "Derivatives of Bessel functions - Compute derivatives of Hankel function H2v(z) with respect to z", ['v', 'z'])

        af('bdtrc', "Binomial distribution - Binomial distribution survival function", ['k', 'n', 'p'], func=SpecialFunctionsFeature.func_int_params)
        af('bdtri', "Binomial distribution - Inverse function to bdtr with respect to p", ['k', 'n', 'y'], func=SpecialFunctionsFeature.func_int_params)
        af('bdtrik', "Binomial distribution - Inverse function to bdtr with respect to k", ['y', 'n', 'p'])
        af('bdtrin', "Binomial distribution - Inverse function to bdtr with respect to n", ['k', 'y', 'p'])

        af('btdtria', "Beta distribution - Inverse of btdtr with respect to a", ['p', 'b', 'x'])
        af('btdtrib', "Beta distribution - Inverse of btdtr with respect to b", ['a', 'p', 'x'])

        af('fdtr', "F distribution - F cumulative distribution function", ['dfn', 'dfd', 'x'])
        af('fdtrc', "F distribution - F survival function", ['dfn', 'dfd', 'x'])
        af('fdtri', "F distribution - The p-th quantile of the F-distribution", ['dfn', 'dfd', 'p'])
        af('fdtridfd', "F distribution - Inverse to fdtr vs dfd", ['dfn', 'p', 'x'])

        af('gdtr', "Gamma distribution - Gamma distribution cumulative distribution function", ['a', 'b', 'x'])
        af('gdtrc', "Gamma distribution - Gamma distribution survival function", ['a', 'b', 'x'])
        af('gdtria', "Gamma distribution - Inverse of gdtr vs a", ['p', 'b', 'x'])
        af('gdtrib', "Gamma distribution - Inverse of gdtr vs b", ['a', 'p', 'x'])
        af('gdtrix', "Gamma distribution - Inverse of gdtr vs x", ['a', 'b', 'p'])

        af('nbdtr', "Negative binomial distribution - Negative binomial cumulative distribution function", ['k', 'n', 'p'])
        af('nbdtrc', "Negative binomial distribution - Negative binomial survival function", ['k', 'n', 'p'])
        af('nbdtri', "Negative binomial distribution - Returns the inverse with respect to the parameter p of y = nbdtr(k, n, p), the negative binomial cumulative distribution function", ['k', 'n', 'y'], func=SpecialFunctionsFeature.func_int_params)
        af('nbdtrik', "Negative binomial distribution - Negative binomial percentile function", ['y', 'n', 'p'])
        af('nbdtrin', "Negative binomial distribution - Inverse of nbdtr vs n", ['k', 'y', 'p'])

        af('ncfdtr', "Noncentral F distribution - Cumulative distribution function of the non-central F distribution", ['dfn', 'dfd', 'nc', 'f'])
        af('ncfdtridfd', "Noncentral F distribution - Calculate degrees of freedom (denominator) for the noncentral F-distribution", ['dfn', 'p', 'nc', 'f'])
        af('ncfdtridfn', "Noncentral F distribution - Calculate degrees of freedom (numerator) for the noncentral F-distribution", ['p', 'dfd', 'nc', 'f'])
        af('ncfdtri', "Noncentral F distribution - Inverse with respect to f of the CDF of the non-central F distribution", ['dfn', 'dfd', 'nc', 'p'])
        af('ncfdtrinc', "Noncentral F distribution - Calculate non-centrality parameter for non-central F distribution", ['dfn', 'dfd', 'p', 'f'])

        af('nctdtr', "Noncentral t distribution - Cumulative distribution function of the non-central t distribution", ['df', 'nc', 't'])
        af('nctdtridf', "Noncentral t distribution - Calculate degrees of freedom for non-central t distribution", ['p', 'nc', 't'])
        af('nctdtrit', "Noncentral t distribution - Inverse cumulative distribution function of the non-central t distribution", ['df', 'nc', 'p'])
        af('nctdtrinc', "Noncentral t distribution - Calculate non-centrality parameter for non-central t distribution", ['df', 'p', 't'])

        af('nrdtrimn', "Normal distribution - Calculate mean of normal distribution given other params", ['p', 'x', 'std'])
        af('nrdtrisd', "Normal distribution - Calculate standard deviation of normal distribution given other params", ['p', 'x', 'mn'])
        af('ndtr', "Normal distribution - Cumulative distribution of the standard normal distribution", ['x'])
        af('log_ndtr', "Normal distribution - Logarithm of Gaussian cumulative distribution function", ['x'])
        af('ndtri', "Normal distribution - Inverse of ndtr vs x", ['y'])
        af('ndtri_exp', "Normal distribution - Inverse of log_ndtr vs x", ['y'])

        af('pdtr', "Poisson distribution - Poisson cumulative distribution function", ['k', 'm'])
        af('pdtrc', "Poisson distribution - Poisson survival function", ['k', 'm'])
        af('pdtri', "Poisson distribution - Inverse to pdtr vs m", ['k', 'y'])
        af('pdtrik', "Poisson distribution - Inverse to pdtr vs m", ['p', 'm'])

        af('stdtr', "Student t distribution - Student t distribution cumulative distribution function", ['df', 't'])
        af('stdtridf', "Student t distribution - Inverse of stdtr vs df", ['p', 't'])
        af('stdtrit', "Student t distribution - The p-th quantile of the student t distribution", ['df', 'p'])

        af('chdtr', "Chi square distribution - Chi square cumulative distribution function", ['v', 'x'])
        af('chdtrc', "Chi square distribution - Chi square survival function", ['v', 'x'])
        af('chdtri', "Chi square distribution - Inverse to chdtrc with respect to x", ['v', 'p'])
        af('chdtriv', "Chi square distribution - Inverse to chdtr with respect to v", ['p', 'x'])

        af('chndtr', "Non-central chi square distribution - Non-central chi square cumulative distribution function", ['x', 'df', 'nc'])
        af('chndtridf', "Non-central chi square distribution - Inverse to chndtr vs df", ['x', 'p', 'nc'])
        af('chndtrinc', "Non-central chi square distribution - Inverse to chndtr vs nc", ['x', 'df', 'p'])
        af('chndtrix', "Non-central chi square distribution - Inverse to chndtr vs x", ['p', 'df', 'nc'])

        af('smirnov', "Kolmogorov distribution - Kolmogorov-Smirnov complementary cumulative distribution function", ['n', 'd'])
        af('smirnovi', "Kolmogorov distribution - Inverse to smirnov", ['n', 'p'])
        af('kolmogorov', "Kolmogorov distribution - Complementary cumulative distribution (Survival Function) function of Kolmogorov distribution", ['y'])
        af('kolmogi', "Kolmogorov distribution - Inverse Survival Function of Kolmogorov distribution", ['p'])

        af('boxcox', "Box-Cox transformation - Compute the Box-Cox transformation", ['x', 'lmbda'])
        af('boxcox1p', "Box-Cox transformation - Compute the Box-Cox transformation of 1 + x", ['x', 'lmbda'])
        af('inv_boxcox', "Box-Cox transformation - Compute the inverse of the Box-Cox transformation", ['y', 'lmbda'])
        af('inv_boxcox1p', "Box-Cox transformation - Compute the inverse of the Box-Cox transformation", ['y', 'lmbda'])

        af('logit', "Sigmoidal functions - Logit ufunc for ndarrays", ['x'])
        af('expit', "Sigmoidal functions - Expit (a.k.a", ['x'])
        af('log_expit', "Sigmoidal functions - Logarithm of the logistic sigmoid function", ['x'])

        af('tklmbda', "Miscellaneous - Cumulative distribution function of the Tukey lambda distribution", ['x', 'lmbda'])
        af('owens_t', "Miscellaneous - Owen's T Function", ['h', 'a'])

        af('entr', "Information Theory functions - Elementwise function for computing entropy", ['x'])
        af('rel_entr', "Information Theory functions - Elementwise function for computing relative entropy", ['x', 'y'])
        af('kl_div', "Information Theory functions - Elementwise function for computing Kullback-Leibler divergence", ['x', 'y'])
        af('huber', "Information Theory functions - Huber loss function", ['delta', 'r'])
        af('pseudo_huber', "Information Theory functions - Pseudo-Huber loss function", ['delta', 'r'])

        af('gamma', "Gamma and related functions - gamma function", ['z'])
        af('gammaln', "Gamma and related functions - Logarithm of the absolute value of the gamma function", ['x'])
        af('loggamma', "Gamma and related functions - Principal branch of the logarithm of the gamma function", ['z'])
        af('gammasgn', "Gamma and related functions - Sign of the gamma function", ['x'])
        af('gammainc', "Gamma and related functions - Regularized lower incomplete gamma function", ['a', 'x'])
        af('gammaincinv', "Gamma and related functions - Inverse to the regularized lower incomplete gamma function", ['a', 'y'])
        af('gammaincc', "Gamma and related functions - Regularized upper incomplete gamma function", ['a', 'x'])
        af('gammainccinv', "Gamma and related functions - Inverse of the regularized upper incomplete gamma function", ['a', 'y'])
        af('beta', "Gamma and related functions - Beta function", ['a', 'b'])
        af('betaln', "Gamma and related functions - Natural logarithm of absolute value of beta function", ['a', 'b'])
        af('betainc', "Gamma and related functions - Regularized incomplete beta function", ['a', 'b', 'x'])
        af('betaincc', "Gamma and related functions - Complement of the regularized incomplete beta function", ['a', 'b', 'x'])
        af('betaincinv', "Gamma and related functions - Inverse of the regularized incomplete beta function", ['a', 'b', 'y'])
        af('betainccinv', "Gamma and related functions - Inverse of the complemented regularized incomplete beta function", ['a', 'b', 'y'])
        af('psi', "Gamma and related functions - The digamma function", ['z'])
        af('rgamma', "Gamma and related functions - Reciprocal of the gamma function", ['z'])
        af('polygamma', "Gamma and related functions - Polygamma functions", ['n', 'x'])
        af('digamma', "Gamma and related functions - The digamma function", ['z'])
        af('poch', "Gamma and related functions - Pochhammer symbol", ['z', 'm'])

        af('lpmv', "Legendre functions - Associated Legendre function of integer order and real degree", ['m', 'v', 'x'])

        af('hyp2f1', "Hypergeometric functions - Gauss hypergeometric function 2F1(a, b; c; z)", ['a', 'b', 'c', 'z'])
        af('hyp1f1', "Hypergeometric functions - Confluent hypergeometric function 1F1", ['a', 'b', 'x'])
        af('hyperu', "Hypergeometric functions - Confluent hypergeometric function U", ['a', 'b', 'x'])
        af('hyp0f1', "Hypergeometric functions - Confluent hypergeometric limit function 0F1", ['v', 'z'])

        af('pbdv', "Parabolic cylinder functions - Parabolic cylinder function D", ['v', 'x'], ['d', 'dp'])
        af('pbvv', "Parabolic cylinder functions - Parabolic cylinder function V", ['v', 'x'], ['v', 'vp'])
        af('pbwa', "Parabolic cylinder functions - Parabolic cylinder function W", ['a', 'x'], ['w', 'wp'])

        af('mathieu_a', "Mathieu - Characteristic value of even Mathieu functions", ['m', 'q'])
        af('mathieu_b', "Mathieu - Characteristic value of odd Mathieu functions", ['m', 'q'])

        af('kelvin', "Kelvin functions - Kelvin functions as complex numbers", ['x'], ['Be', 'Ke', 'Bep', 'Kep'])
        af('ber', "Kelvin functions - Kelvin function ber", ['x'])
        af('bei', "Kelvin functions - Kelvin function bei", ['x'])
        af('berp', "Kelvin functions - Derivative of the Kelvin function ber", ['x'])
        af('beip', "Kelvin functions - Derivative of the Kelvin function bei", ['x'])
        af('ker', "Kelvin functions - Kelvin function ker", ['x'])
        af('kei', "Kelvin functions - Kelvin function kei", ['x'])
        af('kerp', "Kelvin functions - Derivative of the Kelvin function ker", ['x'])
        af('keip', "Kelvin functions - Derivative of the Kelvin function kei", ['x'])

        af('lambertw', "Lambert W and related functions - Lambert W function", ['z'])
        af('wrightomega', "Lambert W and related functions - Wright Omega function", ['z'])

        af('agm', "Compute the arithmetic-geometric mean of a and b", ['a', 'b'])
        af('expn', "Generalized exponential integral En", ['n', 'x'])
        af('exp1', "Exponential integral E1", ['z'])
        af('expi', "Exponential integral Ei", ['x'])
        af('shichi', "Hyperbolic sine and cosine integrals", ['x'], ['si', 'ci'])
        af('sici', "Sine and cosine integrals", ['x'], ['si', 'ci'])
        af('zeta', "Riemann or Hurwitz zeta function", ['x'])
        af('zetac', "Riemann zeta function minus 1", ['x'])


    def add_func(calculator, name, desc, params, outs=None, func=None):
        if func is None:
            func = SpecialFunctionsFeature.func_generic
        if outs is not None:
            for i, out in enumerate(outs):
                func_name = SpecialFunctionsFeature.format_func_name(name, out)
                calculator.funcs[func_name] = FunctionDefinition(
                    'Special',
                    func_name,
                    desc + " - " + out,
                    params,
                    partial(func, getattr(scipy.special, name), i),
                    len(params),
                    len(params),
                    'number')
                #SpecialFunctionsFeature.print_test(getattr(scipy.special, name), func_name, len(params), i)
        else:
            func_name = SpecialFunctionsFeature.format_func_name(name)
            calculator.funcs[func_name] = FunctionDefinition(
                'Special',
                func_name,
                desc,
                params,
                partial(func, getattr(scipy.special, name), None),
                len(params),
                len(params),
                'number')
            #SpecialFunctionsFeature.print_test(getattr(scipy.special, name), func_name, len(params))

    def format_func_name(name, out=None):
        r = "sp_" + name
        if out is not None:
            r += "_" + out
        r = r.lower()
        return r

    # Used to auto-generate tests for functions
    def print_test(f, name, params, i=None):
        out = None
        while out is None:
            p = []
            for ii in range(0, params):
                p.append(random.choice([-1, 0, 0.5, 1]))
            try:
                out = f(*p)
                if i is not None:
                    out = out[i]
            except Exception:
                out = None
            if str(out) in ['inf', '-inf', 'nan', '(nan+nanj)']:
                out = None
            else:
                try:
                    out = SpecialFunctionsFeature.cast_numpy(out)
                    out.to_string()
                except Exception:
                    out = None
        print("{{ 'test': r\"{}({})\", 'expected': {} }},".format(name, ', '.join([str(ps) for ps in p]), repr(out)))

    def func_generic(f, o, self, vals, units, refs, flags):
        out = f(*[float(v) for v in vals])
        if o is not None:
            out = out[o]
        return OperationResult(SpecialFunctionsFeature.cast_numpy(out))

    def func_int_params(f, o, self, vals, units, refs, flags):
        out = f(*[int(v) for v in vals])
        if o is not None:
            out = out[o]
        return OperationResult(SpecialFunctionsFeature.cast_numpy(out))

    def cast_numpy(n):
        if type(n) == numpy.ndarray and n.size == 1:
            n = float(n)
        else:
            n = n.astype(float)
        return Number(Decimal(n))
