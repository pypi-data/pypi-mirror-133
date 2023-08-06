""""""
import semver


def bump_major(version="1.2.3-pre.2+build.4"):
    version = semver.VersionInfo.parse(version)
    changes_major = version.bump_major()

    return changes_major


def bump_minor(version="1.2.3-pre.2+build.4"):
    version = semver.VersionInfo.parse(version)
    changes_monior = version.bump_minor()

    return changes_monior


def bump_path(version="1.2.3-pre.2+build.4"):
    version = semver.VersionInfo.parse(version)
    changes_patch = version.bump_patch()

    return changes_patch


def bump_pre(version="1.2.3-pre.2+build.4"):
    version = semver.VersionInfo.parse(version)
    changes_pre = version.bump_prerelease()

    return changes_pre


def bump_build(version="1.2.3-pre.2+build.4"):
    version = semver.VersionInfo.parse(version)
    changes_build = version.bump_build()

    return changes_build
