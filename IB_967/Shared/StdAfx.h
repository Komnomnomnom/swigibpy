#ifndef DLLEXP
#define DLLEXP __declspec( dllexport )
#endif

#ifdef _MSC_VER

#define assert ASSERT
#define snprintf _snprintf

#include <afxwin.h>

#endif

