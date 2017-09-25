INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_EB500 eb500)

FIND_PATH(
    EB500_INCLUDE_DIRS
    NAMES eb500/api.h
    HINTS $ENV{EB500_DIR}/include
        ${PC_EB500_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    EB500_LIBRARIES
    NAMES gnuradio-eb500
    HINTS $ENV{EB500_DIR}/lib
        ${PC_EB500_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(EB500 DEFAULT_MSG EB500_LIBRARIES EB500_INCLUDE_DIRS)
MARK_AS_ADVANCED(EB500_LIBRARIES EB500_INCLUDE_DIRS)

