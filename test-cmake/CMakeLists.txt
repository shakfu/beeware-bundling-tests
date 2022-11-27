set(APP_NAME Demo)

project(${APP_NAME})

cmake_minimum_required(VERSION 3.1)

set(CMAKE_C_STANDARD 11)

# sources
set(PROJ_RESOURCES ${CMAKE_SOURCE_DIR}/resources)
set(PROJ_ICONS ${PROJ_RESOURCES}/icns)

set(DEMO ${CMAKE_SOURCE_DIR}/../test-xcode/Demo)
set(SUPPORT ${DEMO}/Support)
set(PYFRAMEWORK ${SUPPORT}/Python.xcframework/macos-arm64_x86_64)
set(STDLIB ${SUPPORT}/python-stdlib)
set(LIB_DYNLOAD ${STDLIB}/lib-dynload)

# destinations
set(RESOURCES ${APP_NAME}.app/Contents/Resources)


add_executable(${APP_NAME} MACOSX_BUNDLE main.c)

set_source_files_properties(
    ${STDLIB}
    PROPERTIES
    MACOSX_PACKAGE_LOCATION
    Resources
)
file(COPY ${STDLIB} DESTINATION "${RESOURCES}/support")
file(COPY ${DEMO}/Demo/app DESTINATION "${RESOURCES}")
file(COPY ${DEMO}/Demo/app_packages DESTINATION "${RESOURCES}")
file(COPY ${DEMO}/Demo/Assets.xcassets DESTINATION "${RESOURCES}")
file(COPY ${DEMO}/Demo/demo.entitlements DESTINATION "${RESOURCES}")
# file(COPY ${DEMO}/Demo/Info.plist DESTINATION "${RESOURCES}")

set(ICON_NAME "generic_app.icns")
set(ICON_PATH ${PROJ_ICONS}/${ICON_NAME})
set(app_ICON ${ICON_PATH})
set_source_files_properties(${app_ICON} PROPERTIES MACOSX_PACKAGE_LOCATION Resources)
file(COPY ${ICON_PATH} DESTINATION "${APP_NAME}.app/Contents/Resources")

set_target_properties(${APP_NAME} PROPERTIES
    BUNDLE True
    MACOSX_BUNDLE_GUI_IDENTIFIER org.me.${APP_NAME} 
    MACOSX_BUNDLE_BUNDLE_NAME ${APP_NAME}
    MACOSX_BUNDLE_BUNDLE_VERSION "0.1"
    MACOSX_BUNDLE_SHORT_VERSION_STRING "0.1"
    MACOSX_BUNDLE_ICONFILE ${ICON_NAME}
    # this should not be hardcoded (just a hack for now)
    MACOSX_BUNDLE_INFO_PLIST ${DEMO}/Demo/Info.plist    
    #MACOSX_BUNDLE_INFO_PLIST ${CMAKE_SOURCE_DIR}/cmake/customtemplate.plist.in
)

add_library(libpython STATIC IMPORTED)
set_target_properties(libpython PROPERTIES
        IMPORTED_LOCATION ${PYFRAMEWORK}/libPython3.10.a
        INTERFACE_INCLUDE_DIRECTORIES ${PYFRAMEWORK}/Headers
)

target_link_libraries(${APP_NAME}
    libpython
    "-framework CoreFoundation"
)


# Destination paths below are relative to ${CMAKE_INSTALL_PREFIX}
install(TARGETS ${APP_NAME}
    BUNDLE DESTINATION . COMPONENT Runtime
    RUNTIME DESTINATION bin COMPONENT Runtime
    )

set(APPS "\${CMAKE_INSTALL_PREFIX}/${APP_NAME}.app")

set(DIRS ${CMAKE_BINARY_DIR})

install(CODE "include(BundleUtilities)
    fixup_bundle(\"${APPS}\" \"\" \"${DIRS}\")")

set(CPACK_GENERATOR "DRAGNDROP")
include(CPack)

