#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <CoreFoundation/CoreFoundation.h>

#define MAX_CHARS 1024;

int main(int argc, char *argv[]) {

    // int ret = 0;
    // PyStatus status;
    // PyConfig config;
    // char app_module_name[MAX_CHARS];
    // char path[MAX_CHARS];
    // char traceback_str[MAX_CHARS];
    // wchar_t *wtmp_str[MAX_CHARS];
    // const char *app_module_str;
    // const char* nslog_script;
    // PyObject *app_module;
    // PyObject *module;
    // PyObject *module_attr;
    // PyObject *method_args;
    // PyObject *result;
    // PyObject *exc_type;
    // PyObject *exc_value;
    // PyObject *exc_traceback;
    // PyObject *systemExit_code;

    // sets python_home to <bundle>/Resources folder

    

    wchar_t* python_home;
    CFBundleRef app_bundle;   

    CFURLRef resources_url;
    CFURLRef resources_abs_url;
    CFStringRef resources_str;
    const char* resources_path;

    CFURLRef stdlib_url;
    CFStringRef stdlib_str;
    const char* stdlib_path;

    // get main bundle
    app_bundle = CFBundleGetMainBundle();

    // get a reference to the bundle's Resources directory
    resources_url = CFBundleCopyResourcesDirectoryURL(app_bundle);
    // resources_abs_url = CFURLCopyAbsoluteURL(resources_url);
    // resources_str = CFURLCopyFileSystemPath(resources_abs_url, kCFURLPOSIXPathStyle);
    // resources_path = CFStringGetCStringPtr(resources_str, kCFStringEncodingUTF8);

    // get a reference to <name>.app/Contents/Resources/support/python-stdlib
    stdlib_url = CFURLCreateCopyAppendingPathComponent(NULL, resources_url, CFSTR("support/python-stdlib"), 1);
    stdlib_str = CFURLCopyFileSystemPath(stdlib_url, kCFURLPOSIXPathStyle);
    stdlib_path = CFStringGetCStringPtr(stdlib_str, kCFStringEncodingUTF8);

    python_home = Py_DecodeLocale(stdlib_path, NULL);

    CFRelease(stdlib_str);
    CFRelease(stdlib_url);

    // CFRelease(resources_str);
    // CFRelease(resources_abs_url);
    // CFRelease(resources_url);

    if (python_home == NULL) {
        return 1;
    }
    Py_SetPythonHome(python_home);

    (void)argc;
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }
    Py_SetProgramName(program);
    Py_Initialize();
    PyRun_SimpleString(argv[1]);
    if (Py_FinalizeEx() < 0) {
        exit(120);
    }
    PyMem_RawFree(program);
    return 0;
}

