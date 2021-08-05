#include <pybind11/pybind11.h>
namespace py = pybind11;


float some_fn(float arg1, float arg2) {
    return arg1 + arg2;
}

PYBIND11_MODULE(test, handle) {
    handle.doc() = "This is the module doc!";
    handle.def("some_fn_python", &some_fn);
}