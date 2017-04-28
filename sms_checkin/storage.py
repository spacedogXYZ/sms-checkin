from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from whitenoise.storage import HelpfulExceptionMixin, CompressedStaticFilesMixin

class NoStrictManifestStaticFilesStorage(ManifestStaticFilesStorage):
    manifest_strict=False

class NoStrictCompressedManifestStaticFilesStorage(
        HelpfulExceptionMixin, CompressedStaticFilesMixin,
        NoStrictManifestStaticFilesStorage):
    pass