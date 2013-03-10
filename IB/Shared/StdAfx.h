#ifndef DLLEXP
#define DLLEXP __declspec( dllexport )
#endif

#ifdef _MSC_VER

#define assert ASSERT
#define snprintf _snprintf

#ifdef _MFC_VER
#include <afxwin.h>
#endif

#endif

