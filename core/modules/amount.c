#define Py_LIMITED_API
#include <Python.h>

#ifdef _MSC_VER
typedef __int64 int64_t;
double round(double x) { return floor(x + 0.5); }
int rint(double x) { return (int)round(x); }
#endif

typedef struct {
    PyObject_HEAD
    int64_t ival; /* Value shifted by currency's exponent */
    PyObject *currency; /* a Currency instance */
    PyObject *rval; /* Real value, as a python float instance */
} Amount;

static PyObject *Amount_Type;

#define Amount_Check(v) (Py_TYPE(v) == (PyTypeObject *)Amount_Type)

/* Utility funcs */

static int64_t
get_amount_ival(PyObject *amount)
{
    /* Returns amount's ival if it's an amount, or 0 if it's an int with a value of 0.
       Call check_amount() before using this.
    */
    if (Amount_Check(amount)) {
        return ((Amount *)amount)->ival;
    }
    else { /* it's an int and it *has* to be 0 */
        return 0;
    }
}

static int
get_currency_exponent(PyObject *currency)
{
    /* Returns -1 if there's a problem. */
    PyObject *tmp;
    int r;
    
    tmp = PyObject_GetAttrString(currency, "exponent");
    if (tmp == NULL) {
        return -1;
    }
    r = PyLong_AsLong(tmp);
    Py_DECREF(tmp);
    return r;
}

static int
amounts_are_compatible(PyObject *a, PyObject *b)
{
    /* a and b are either Amount instances or 0 */
    PyObject *tmp1, *tmp2;
    int64_t aval, bval;
    
    aval = get_amount_ival(a);
    bval = get_amount_ival(b);
    
    if (aval && bval) {
        /* None of the values are zero, we must make sure the currencies are the same */
        tmp1 = ((Amount *)a)->currency;
        tmp2 = ((Amount *)b)->currency;
        return PyObject_RichCompareBool(tmp1, tmp2, Py_EQ);
    }
    else {
        return 1;
    }
}

static int
check_amount(PyObject *o)
{
    /* Returns true if o is an amount and false otherwise.
       A valid amount is either an Amount instance or an int instance with the value of 0.
    */
    if (Amount_Check(o)) {
        return 1;
    }
    if (!PyLong_Check(o)) {
        return 0;
    }
    return PyLong_AS_LONG(o) == 0;
}

static int
check_amounts(PyObject *a, PyObject *b, int seterr)
{
    /* Verify that a and b are amounts and compatible together and returns true or false.
       if seterr is true, an appropriate error is set.
    */
    if (!check_amount(a) || !check_amount(b)) {
        if (seterr) {
            PyErr_SetString(PyExc_TypeError, "Amounts can only be compared with other amounts or zero.");
        }
        return 0;
    }
    
    if (!amounts_are_compatible(a, b)) {
        if (seterr) {
            PyErr_SetString(PyExc_ValueError, "Amounts of different currencies can't be compared.");
        }
        return 0;
    }
    
    return 1;
}

static PyObject *
create_amount(int64_t ival, PyObject *currency)
{
    /* Create a new amount in a way that is faster than the normal init */
    Amount *r;
    double dtmp;
    int exponent;
    r = (Amount *)PyType_GenericAlloc((PyTypeObject *)Amount_Type, 0);
    r->ival = ival;
    r->currency = currency;
    Py_INCREF(currency);
    exponent = get_currency_exponent(currency);
    dtmp = (double)ival / pow(10, exponent);
    r->rval = PyFloat_FromDouble(dtmp);
    if (r->rval == NULL) {
        return NULL;
    }
    return (PyObject *)r;
}

/* Methods */

static void
Amount_dealloc(Amount *self)
{
    Py_XDECREF(self->currency);
    Py_XDECREF(self->rval);
    PyObject_Del(self);
}

static PyObject *
Amount_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    Amount *self;
    
    self = (Amount *)PyType_GenericAlloc(type, 0);
    if (self == NULL) {
        return NULL;
    }
    self->currency = Py_None;
    Py_INCREF(self->currency);
    self->rval = PyFloat_FromDouble(0);
    if (self->rval == NULL) {
        Py_DECREF(self);
        return NULL;
    }
    self->ival = 0;
    
    return (PyObject *)self;
}

static int
Amount_init(Amount *self, PyObject *args, PyObject *kwds)
{
    PyObject *amount, *currency, *tmp;
    int exponent;
    double dtmp;
    
    static char *kwlist[] = {"amount", "currency", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|OO", kwlist, &amount, &currency)) {
        return -1;
    }
    
    if (currency) {
        tmp = self->currency;
        Py_INCREF(currency);
        self->currency = currency;
        Py_XDECREF(tmp);
    }
    
    exponent = get_currency_exponent(self->currency);
    if (exponent == -1) {
        return -1;
    }
    
    if (amount) {
        dtmp = PyFloat_AsDouble(amount);
        if (dtmp == -1 && PyErr_Occurred()) {
            return -1;
        }
        self->ival = round(dtmp * pow(10, exponent));
        tmp = self->rval;
        Py_INCREF(amount);
        self->rval = amount;
        Py_XDECREF(tmp);
    }

    return 0;
}

static int
Amount_traverse(Amount *self, visitproc visit, void *arg)
{
    Py_VISIT(self->rval);
    Py_VISIT(self->currency);
    return 0;
}

static int
Amount_clear(Amount *self)
{
    Py_CLEAR(self->rval);
    Py_CLEAR(self->currency);
    return 0;
}

static PyObject *
Amount_copy(PyObject *self)
{
    return create_amount(((Amount *)self)->ival, ((Amount *)self)->currency);
}

static PyObject *
Amount_deepcopy(PyObject *self, PyObject *args, PyObject *kwds)
{
    return Amount_copy(self);
}

static PyObject *
Amount_repr(Amount *self)
{
    int exponent;
    PyObject *r, *fmt, *args;
    
    exponent = get_currency_exponent(self->currency);
    args = Py_BuildValue("(iOO)", exponent, self->rval, self->currency);
    fmt = PyUnicode_FromString("Amount(%.*f, %r)");
    r = PyUnicode_Format(fmt, args);
    Py_DECREF(fmt);
    Py_DECREF(args);
    return r;
}

Py_hash_t
Amount_hash(Amount *self)
{
    PyObject *hash_tuple, *int_value;
    Py_hash_t r;
    
    int_value = PyLong_FromLongLong(self->ival);
    hash_tuple = PyTuple_Pack(2, int_value, self->currency);
    Py_DECREF(int_value);
    r = PyObject_Hash(hash_tuple);
    Py_DECREF(hash_tuple);
    return r;
}

static PyObject *
Amount_richcompare(PyObject *a, PyObject *b, int op)
{
    int64_t aval, bval;
    int r, is_eq_op;
    
    is_eq_op = (op == Py_EQ) || (op == Py_NE);
    
    if (!check_amounts(a, b, !is_eq_op)) {
        if (op == Py_EQ) {
            Py_RETURN_FALSE;
        }
        else if (op == Py_NE) {
            Py_RETURN_TRUE;
        }
        else {
            return NULL; // An error has been set already
        }
    }
    
    /* The comparison is valid, do it */
    r = 0;
    aval = get_amount_ival(a);
    bval = get_amount_ival(b);
    switch (op) {
        case Py_LT: r = aval < bval; break;
        case Py_LE: r = aval <= bval; break;
        case Py_EQ: r = aval == bval; break;
        case Py_NE: r = aval != bval; break;
        case Py_GT: r = aval > bval; break;
        case Py_GE: r = aval >= bval; break;
    }
    if (r) {
        Py_RETURN_TRUE;
    }
    else {
        Py_RETURN_FALSE;
    }
}

static PyObject *
Amount_neg(Amount* self)
{
    return create_amount(-self->ival, self->currency);
}

static int
Amount_bool(Amount *self)
{
    return self->ival != 0;
}

static PyObject *
Amount_abs(Amount* self)
{
    if (self->ival >= 0) {
        Py_INCREF(self);
        return (PyObject *)self;
    }
    else {
        return Amount_neg(self);
    }
}

static PyObject *
Amount_float(Amount* self)
{
    return PyNumber_Float(self->rval);
}

static PyObject *
Amount_add(PyObject *a, PyObject *b)
{
    int64_t aval, bval;
    PyObject *currency;
    
    if (!check_amounts(a, b, 1)) {
        return NULL;
    }
    aval = get_amount_ival(a);
    bval = get_amount_ival(b);
    if (aval && bval) {
        currency = ((Amount *)a)->currency;
        return create_amount(aval + bval, currency);
    }
    else if (aval) {
        /* b is 0, return a */
        Py_INCREF(a);
        return a;
    }
    else {
        /* whether b is 0 or not, we return it */
        Py_INCREF(b);
        return b;
    }
}

static PyObject *
Amount_sub(PyObject *a, PyObject *b)
{
    int64_t aval, bval;
    PyObject *currency;
    
    if (!check_amounts(a, b, 1)) {
        return NULL;
    }
    aval = get_amount_ival(a);
    bval = get_amount_ival(b);
    if (aval && bval) {
        currency = ((Amount *)a)->currency;
        return create_amount(aval - bval, currency);
    }
    else if (aval) {
        /* b is 0, return a */
        Py_INCREF(a);
        return a;
    }
    else if (bval) {
        /* a is 0 but not b, return -b */
        return Amount_neg((Amount *)b);
    }
    else {
        /* both a and b are 0, return any */
        Py_INCREF(a);
        return a;
    }
}

static PyObject *
Amount_mul(PyObject *a, PyObject *b)
{
    double dval;
    int64_t ival;
    
    /* first, for simplicity, handle reverse op */
    if (!Amount_Check(a) && Amount_Check(b)) {
        return Amount_mul(b, a);
    }
    /* it is assumed that a is an amount */
    if (Amount_Check(b)) {
        PyErr_SetString(PyExc_TypeError, "Can't multiply two amounts together");
        return NULL;
    }
    
    dval = PyFloat_AsDouble(b);
    if (dval == -1 && PyErr_Occurred()) {
        return NULL;
    }
    
    if (dval == 0) {
        return PyLong_FromLong(0);
    }
    
    ival = rint(((Amount *)a)->ival * dval);
    return create_amount(ival, ((Amount *)a)->currency);
}

static PyObject *
Amount_true_divide(PyObject *a, PyObject *b)
{
    double dval;
    int64_t ival;
    
    if (!Amount_Check(a)) {
        PyErr_SetString(PyExc_TypeError, "An amount can't divide something else.");
        return NULL;
    }
    
    if (Amount_Check(b)) {
        if (!amounts_are_compatible(a, b)) {
            PyErr_SetString(PyExc_ValueError, "Amounts of different currency can't be divided.");
            return NULL;
        }
        // Return both rval divided together
        return PyNumber_TrueDivide(((Amount *)a)->rval, ((Amount *)b)->rval);
    }
    else {
        dval = PyFloat_AsDouble(b);
        if (dval == -1 && PyErr_Occurred()) {
            return NULL;
        }
    }
    
    if (dval == 0) {
        PyErr_SetString(PyExc_ZeroDivisionError, "");
        return NULL;
    }
    
    ival = rint(((Amount *)a)->ival / dval);
    return create_amount(ival, ((Amount *)a)->currency);
}

static PyObject *
Amount_getcurrency(Amount *self)
{
    Py_INCREF(self->currency);
    return self->currency;
}

static PyObject *
Amount_getvalue(Amount *self)
{
    Py_INCREF(self->rval);
    return self->rval;
}

/* We need both __copy__ and __deepcopy__ methods for amounts to behave correctly in undo_test. */

static PyMethodDef Amount_methods[] = {
    {"__copy__", (PyCFunction)Amount_copy, METH_NOARGS, ""},
    {"__deepcopy__", (PyCFunction)Amount_deepcopy, METH_VARARGS, ""},
    {0, 0, 0, 0},
};

static PyGetSetDef Amount_getseters[] = {
    {"currency", (getter)Amount_getcurrency, NULL, "currency", NULL},
    {"value", (getter)Amount_getvalue, NULL, "value", NULL},
    {0, 0, 0, 0, 0},
};

static PyType_Slot Amount_Slots[] = {
    {Py_tp_new, Amount_new},
    {Py_tp_init, Amount_init},
    {Py_tp_dealloc, Amount_dealloc},
    {Py_tp_repr, Amount_repr},
    {Py_tp_hash, Amount_hash},
    {Py_tp_traverse, Amount_traverse},
    {Py_tp_clear, Amount_clear},
    {Py_tp_richcompare, Amount_richcompare},
    {Py_tp_methods, Amount_methods},
    {Py_tp_getset, Amount_getseters},
    {Py_nb_add, Amount_add},
    {Py_nb_subtract, Amount_sub},
    {Py_nb_multiply, Amount_mul},
    {Py_nb_negative, Amount_neg},
    {Py_nb_absolute, Amount_abs},
    {Py_nb_bool, Amount_bool},
    {Py_nb_float, Amount_float},
    {Py_nb_true_divide, Amount_true_divide},
    {0, 0},
};

static PyType_Spec Amount_Type_Spec = {
    "_amount.Amount",
    sizeof(Amount),
    0,
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    Amount_Slots,
};

static PyMethodDef module_methods[] = {
    {NULL}  /* Sentinel */
};

static struct PyModuleDef AmountDef = {
    PyModuleDef_HEAD_INIT,
    "_amount",
    NULL,
    -1,
    module_methods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyObject *
PyInit__amount(void)
{
    PyObject *m;
    
    Amount_Type = PyType_FromSpec(&Amount_Type_Spec);
    
    m = PyModule_Create(&AmountDef);
    if (m == NULL) {
        return NULL;
    }
    
    PyModule_AddObject(m, "Amount", Amount_Type);
    return m;
}