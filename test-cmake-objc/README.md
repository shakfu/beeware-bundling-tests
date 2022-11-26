# About this test

Attempt to build a python macOS app bundle using cmake, beeware statically compiled python and c-api entry point.

This is directly derivative of the [beeware macos xcode cookiecutter template](ref).

## Target structure

```text
Demo.app
└── Contents
    ├── MacOS
    ├── Resources
    │ ├── app
    │ │ └── demo
    │ ├── app_packages
    │ └── support
    │     └── python-stdlib
    └── _CodeSignature
```


## TODO

Cmake build script should do the following:

1. Compile source: main.m

2. Link binary with libraries:
	- Appkit.framework
	- Cocoa.framework
	- Foundation.framework
	- Python.xcframework
		- Headers
		- libpython3.10.a

3. Copy bundle resources: (all to Resources)
	- Assets.xcassets
	- app
	- app_packages

4. Copy Python standard library:

	Support -> Resources

5. Sign Python Binary Modules:

	```bash
	set -e
	echo "Signed as $EXPANDED_CODE_SIGN_IDENTITY_NAME ($EXPANDED_CODE_SIGN_IDENTITY)"
	find "$BUILT_PRODUCTS_DIR/$UNLOCALIZED_RESOURCES_FOLDER_PATH/support/python-stdlib/lib-dynload" -name "*.so" -exec /usr/bin/codesign --force --sign "$EXPANDED_CODE_SIGN_IDENTITY" -o runtime --timestamp=none --preserve-metadata=identifier,entitlements,flags --generate-entitlement-der {} \; 
	find "$BUILT_PRODUCTS_DIR/$UNLOCALIZED_RESOURCES_FOLDER_PATH/app_packages" -name "*.so" -exec /usr/bin/codesign --force --sign "$EXPANDED_CODE_SIGN_IDENTITY" -o runtime --timestamp=none --preserve-metadata=identifier,entitlements,flags --generate-entitlement-der {} \; 
	find "$BUILT_PRODUCTS_DIR/$UNLOCALIZED_RESOURCES_FOLDER_PATH/app" -name "*.so" -exec /usr/bin/codesign --force --sign "$EXPANDED_CODE_SIGN_IDENTITY" -o runtime --timestamp=none --preserve-metadata=identifier,entitlements,flags --generate-entitlement-der {} \; 
	```