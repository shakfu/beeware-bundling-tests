import subprocess

"""
This is the beginnings of a possible cmake plugin for briefcase

Will need to verify the installation of the following:

- xcode installed
- commandline tools installed
- cmake installed (correct version of course)


Plan:

- [ ] finish this once proof-of-concept is complete

"""

from briefcase.commands import (
    BuildCommand,
    CreateCommand,
    OpenCommand,
    PackageCommand,
    PublishCommand,
    RunCommand,
    UpdateCommand,
)
from briefcase.config import BaseConfig
from briefcase.exceptions import BriefcaseCommandError
# from briefcase.integrations.xcode import verify_xcode_install
from briefcase.platforms.macOS import macOSMixin, macOSPackageMixin, macOSRunMixin


def ensure_cmake_is_installed(tools: ToolCache, min_version=min_version):
    try:
        tools.subprocess.check_output(
            ["cmake", "--version"],
            stderr=subprocess.STDOUT,
        )    
    except subprocess.CalledProcessError as e:
            raise BriefcaseCommandError(
                """\
    Could not find an Cmake installation.
    To install cmake if you have Homebrew, run:
        $ brew install cmake
    or install cmake directly from kitware.com
    """
            ) from e

def verify_cmake_install(tools: ToolCache, min_version: tuple = None):
    """Verify that Cmake is installed and ready for use.

    We need Cmake, and we also need to ensure that an adequate version 
    is available.
    
    :param tools: ToolCache of available tools
    :param min_version: The minimum allowed version of Xcode, specified as a
        tuple of integers (e.g., (11, 2, 1)). Default: ``None``, meaning there
        is no minimum version.
    """
    # short circuit since already verified and available
    if hasattr(tools, "cmake"):
        return

    ensure_cmake_is_installed(tools, min_version=min_version)
    tools.cmake = True


class macOSCmakeMixin(macOSMixin):
    output_format = "Cmake"

    def verify_tools(self):
        if self.tools.host_os != "Darwin":
            raise BriefcaseCommandError(
                "macOS applications require the Xcode command line tools, "
                "which are only available on macOS."
            )
        # Require XCode 10.0.0. There's no particular reason for this
        # specific version, other than it's a nice round number that's
        # not *that* old at time of writing.
        verify_cmake_install(self.tools, min_version=(10, 0, 0))

        # Verify superclass tools *after* xcode. This ensures we get the
        # git check *after* the xcode check.
        super().verify_tools()

    def project_path(self, app):
        # return self.bundle_path(app) / f"{app.formal_name}.xcodeproj"
        return self.bundle_path(app) / "CMakeList.txt"

    def binary_path(self, app):
        return (
            self.platform_path
            / self.output_format
            / f"{app.formal_name}"
            / "build"
            / "Release"
            / f"{app.formal_name}.app"
        )

    def distribution_path(self, app, packaging_format):
        if packaging_format == "dmg":
            return self.platform_path / f"{app.formal_name}-{app.version}.dmg"
        else:
            return self.binary_path(app)


class macOSXcodeCreateCommand(macOSXcodeMixin, CreateCommand):
    description = "Create and populate a macOS Xcode project."


class macOSXcodeOpenCommand(macOSXcodeMixin, OpenCommand):
    description = "Open a macOS Xcode project."


class macOSXcodeUpdateCommand(macOSXcodeCreateCommand, UpdateCommand):
    description = "Update an existing macOS Xcode project."


class macOSXcodeBuildCommand(macOSXcodeMixin, BuildCommand):
    description = "Build a macOS Xcode project."

    def build_app(self, app: BaseConfig, **kwargs):
        """Build the Xcode project for the application.
        :param app: The application to build
        """
        self.logger.info("Building Cmake project...", prefix=app.app_name)
        with self.input.wait_bar("Building..."):
            try:
                self.tools.subprocess.run(
                    [
                        "xcodebuild",
                        "-project",
                        self.project_path(app),
                        "-quiet",
                        "-configuration",
                        "Release",
                        "build",
                    ],
                    check=True,
                )
                self.logger.info("Build succeeded.")
            except subprocess.CalledProcessError as e:
                raise BriefcaseCommandError(
                    f"Unable to build app {app.app_name}."
                ) from e


class macOSXcodeRunCommand(macOSRunMixin, macOSXcodeMixin, RunCommand):
    description = "Run a macOS app."


class macOSXcodePackageCommand(macOSPackageMixin, macOSXcodeMixin, PackageCommand):
    description = "Package a macOS app for distribution."


class macOSXcodePublishCommand(macOSXcodeMixin, PublishCommand):
    description = "Publish a macOS app."


# Declare the briefcase command bindings
create = macOSXcodeCreateCommand  # noqa
update = macOSXcodeUpdateCommand  # noqa
open = macOSXcodeOpenCommand  # noqa
build = macOSXcodeBuildCommand  # noqa
run = macOSXcodeRunCommand  # noqa
package = macOSXcodePackageCommand  # noqa
publish = macOSXcodePublishCommand  # noqa
