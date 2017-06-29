#include <Python.h>

int Cfib(int n)
{
	if (n<2)
		return n;
	else
		return Cfib(n-1) + Cfib(n-2);
}

static PyObject* fib(PyObject* self, PyObject* args)
{
	int n;
	if (!PyArg_ParseTuple(args, "i", &n))
		return NULL;
	return Py_BuildValue("i", Cfib(n));
}


static PyObject* version(PyObject* self)
{
	return Py_BuildValue("s", "Version 1.0");
}


// Method Definition
static PyMethodDef myMethods[] = {
	{"fib", fib, METH_VARARGS, "Calculates Fibonacci numbers"},
	{"version", (PyCFunction)version, METH_NOARGS, "Returns the version"},
	{NULL, NULL, 0, NULL}
};


// Module Definition
static struct PyModuleDef myModule = 
{
	PyModuleDef_HEAD_INIT,
	"myModule",
	"Fibonacci Module",
	-1, 
	myMethods
};

//Initializer Function
PyMODINIT_FUNC PyInit_myModule(void)
{
	return PyModule_Create(&myModule);
};
